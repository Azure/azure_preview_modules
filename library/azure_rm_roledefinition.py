#!/usr/bin/python
#
# Copyright (c) 2018 Yunge Zhu, (@yungezz)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_roledefinition
version_added: "2.8"
short_description: Manage Azure Role Definition.
description:
    - Create, update and delete instance of Azure Role Definition.

options:
    name:
        description:
            - Unique name of role definition.
        required: True
    permissions:
        description:
            - Set of role definition peremissions.
            - See U(https://docs.microsoft.com/en-us/azure/app-service/app-service-web-overview) for more info.
        suboptions:
            actions:
                description:
                    - List of allowed actions.
                type: list
            not_actions:
                description:
                    - List of denied actions.
                type: list
            data_actions:
                description:
                    - List of allowed data actions.
                type: list
            not_data_actions:
                description:
                    - List of denied data actions.
                type: list
    assignable_scopes:
        description: List of assignable scope of this definition.
    scope:
        description: The scope of the role definition.
    description:
        description:
            - The role definition description.
    state:
      description:
        - Assert the state of the role definition.
        - Use 'present' to create or update a role definition and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Yunge Zhu(@yungezz)"

'''

EXAMPLES = '''
    - name: Create a role definition
      azure_rm_roledefinition:
        name: myTestRole
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myresourceGroup
        permissions:
            actions:
                - "Microsoft.Compute/read"
                - "Microsoft.Storage/read"
            data_actions:
                - "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write"
        assignable_scopes:
            - "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
'''

RETURN = '''
id:
    description: Id of current role definition.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleDefinitions/roleDefinitionId"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.serialization import Model
    from azure.mgmt.authorization import AuthorizationManagementClient
    from azure.mgmt.authorization.model import { RoleDefinition, Permission }

except ImportError:
    # This is handled in azure_rm_common
    pass


permission_spec = dict(
    actions=dict(
        type='list',
        options=dict(type='str')
    ),
    not_actions=dict(
        type='list',
        options=dict(type='str')
    ),
    data_actions=dict(
        type='list',
        options=dict(type='str')
    ),
    not_data_actions=dict(
        type='list',
        options=dict(type='str')
    ),
)


def roledefinition_to_dict(role):
    result = dict(
        id=role.id,
        name=role.name,
        type=role.kind,
        assignable_scopes=role.assignable_scopes,
        description=role.description,
    )
    if role.permissions:
        result.permissions = [dict(
            actions=p.actions,
            not_actions=p.not_actions,
            data_actions=p.data_actions,
            not_data_actions=p.not_data_actions
        ) for p in role.permissions]
    return result


class Actions:
    NoAction, CreateOrUpdate, Delete = range(3)


class AzureRMRoleDefinition(AzureRMModuleBase):
    """Configuration class for an Azure RM Role definition resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            scope=dict(
                type='str'
            ),
            permissions=dict(
                type='list',
                elements='dict',
                options=permission_spec
            ),
            assignable_scopes=dict(
                type='list',
                elements='str'
            ),
            description=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.name = None
        self.scope = None
        self.permissions = None
        self.description = None
        self.assignable_scopes = None

        self.results = dict(
            changed=False,
            id=None,
        )
        self.state = None
        self.to_do = Actions.NoAction

        self._client = None

        super(AzureRMRoleDefinition, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        # get management client
        self._client = self.get_mgmt_svc_client(AuthorizationManagementClient,
                                                base_url=self._cloud_environment.endpoints.resource_manager)

        # build cope
        self.scope = self.build_scope()

        # get existing role definition
        old_response = self.get_roledefinition()

        if old_response:
            self.results['id'] = old_response['id']

        if self.state == 'present':
            # check if the role definition exists
            if not old_response:
                self.log("Role definition doesn't exist in this scope")

                self.to_do = Actions.CreateOrUpdate

            else:
                # existing role definition, do update
                self.log("Role definition already exists")
                self.log('Result: {0}'.format(old_response))

                # compare if role definition changed
                if self.check_update(old_response):
                    self.to_do = Actions.CreateOrUpdate

        elif self.state == 'absent':
            if old_response:
                self.log("Delete role defintion")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_roledefinition()

                self.log('role definition deleted')

            else:
                self.fail("role definition {0} not exists.".format(self.name))

        if self.to_do == Actions.CreateOrUpdate:
            self.log('Need to Create/Update role definition')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            response = self.create_update_roledefinition()
            self.results['id'] = response['id']

        return self.results

    # build scope
    def build_scope(self):
        subscription_scope = '/subscription/' + self.subscription_id
        if self.scope is None:
            return subscription_scope
        return self.scope

    # check update
    def check_update(self, old_definition):
        if self.description and self.description != old_definition['properties']['description']:
            return True
        if self.permissions and self.permissions != old_definition['permissions']:
            return True
        if self.assignable_scopes and self.assignable_scopes != old_definition['assignment_scopes']:
            return True
        return False

    def create_update_roledefinition(self):
        '''
        Creates or updates role definition.

        :return: deserialized role definition
        '''
        self.log("Creating / Updating role definition {0}".format(self.name))

        try:
            permissions = None
            if self.permissions:
                permissions = [Permission(
                    actions=p.actions,
                    not_actions=p.not_actions,
                    data_actions=p.data_actions,
                    not_data_actions=p.not_data_actions
                ) for p in self.permissions]
            role_definition = RoleDefinition(name=self.name,
                                             type=self.type,
                                             description=self.description,
                                             permissions=permissions,
                                             role_type='CustomRole')
            response = self._client.role_definitions.create_or_update(role_definition_id=role_id,
                                                                      scope=self.scope,
                                                                      role_definition=role_definition)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create role definition.')
            self.fail(
                "Error creating role definition: {0}".format(str(exc)))
        return roledefinition_to_dict(response)

    def delete_roledefinition(self):
        '''
        Deletes specified role definition.

        :return: True
        '''
        self.log("Deleting the role definition {0}".format(self.name))
        scope = 
        try:
            response = self._client.role_definitions.delete(name=self.name,
                                                            scope=self.scope)
        except CloudError as e:
            self.log('Error attempting to delete the role definition.')
            self.fail("Error deleting the role definition: {0}".format(str(e)))

        return True

    def get_roledefinition(self):
        '''
        Gets the properties of the specified role definition.

        :return: deserialized role definition state dictionary
        '''
        self.log("Checking if the role definition {0} is present".format(self.name))

        response = None

        try:
            response = list(self._client.role_definitions.list(scope=self.scope))

            if response.length > 0:
                self.log("Response : {0}".format(response))
                roles = []
                for r in response:
                    if r.name == name or r.role_name == name:
                        roles.append(r)

                if roles.length == 1:
                    self.log("role definition : {0} found".format(self.name))
                    return roledefinition_to_dict(roles[0])
                if roles.length > 1:
                    self.fail("Found multiple role definitions: {0}".format(roles))

        except CloudError as ex:
            self.log("Didn't find role definition {0} in resource group {1}".format(
                self.name, self.resource_group))

        return False


def main():
    """Main execution"""
    AzureRMRoleDefinition()


if __name__ == '__main__':
    main()