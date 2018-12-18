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
module: azure_rm_roleassignment
version_added: "2.8"
short_description: Manage Azure Role Assignment.
description:
    - Create and delete instance of Azure Role Assignment.

options:
    name:
        description:
            - Unique name of role assignment.
        required: True
    principal_id:
        description:
            - The principal id assigned to the role. This maps to the ID inside the Active Directory. It can point to a user, service principal or security group.
    role_definition_id:
        description:
            -  The role definition id used in the role assignment.
    scope:
        description:
            - "The scope of the role assignment to create. For example, use /subscriptions/{subscription-id}/ for a subscription,
              /subscriptions/{subscription-id}/resourceGroups/{resource-group-name} for a resource group,
              and /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name} for a resource."
    state:
      description:
        - Assert the state of the role assignment.
        - Use 'present' to create or update a role assignment and 'absent' to delete it.
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
    - name: Create a role assignment
      azure_rm_roleassignment:
        name: myTestRole
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        principal_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        role_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

'''

RETURN = '''
id:
    description: Id of current role assignment.
    returned: always
    type: str
    sample: {
        "id": "roleAssignmentId=/subscriptions/<subs_id>/providers/Microsoft.Authorization/roleAssignments/<roleassignment_id>"
    }
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.serialization import Model
    from azure.mgmt.authorization import AuthorizationManagementClient
    from azure.mgmt.authorization.models import RoleAssignmentCreateParameters

except ImportError:
    # This is handled in azure_rm_common
    pass


def roleassignment_to_dict(assignment):
    return dict(
        id=assignment.id,
        name=assignment.name,
        type=assignment.type,
        principal_id=assignment.principal_id
        role_definition_id=assignment.role_definition_id,
        scope=assignment.scope
    )


class AzureRMRoleAssignment(AzureRMModuleBase):
    """Configuration class for an Azure RM Role Assignment"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            scope=dict(
                type='str'
            ),
            principal_id=dict(
                type='str',
                required=True
            ),
            role_definition_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.name = None
        self.scope = None
        self.principal_id = None
        self.role_definition_id = None

        self.results = dict(
            changed=False,
            id=None,
        )
        self.state = None

        self._client = None

        super(AzureRMRoleAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None
        to_be_updated = False

        # get management client
        self._client = self.get_mgmt_svc_client(AuthorizationManagementClient,
                                                base_url=self._cloud_environment.endpoints.resource_manager)

        # build cope
        self.scope = build_scope()

        # get existing role assignment
        old_response = self.get_roleassignment()

        if old_response:
            self.results['id'] = old_response['id']

        if self.state == 'present':
            # check if the role assignment exists
            if not old_response:
                self.log("Role definition doesn't exist in this scope")

                self.results['changed'] = True

                if self.check_mode:
                    return self.results
                response = self.create_roleassignment()
                self.results['id'] = response['id']

            else:
                self.log("Role assignment already exists, not updatable")
                self.log('Result: {0}'.format(old_response))

        elif self.state == 'absent':
            if old_response:
                self.log("Delete role assignment")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_roleassignment()

                self.log('role definition deleted')

            else:
                self.fail("role assignment {0} not exists.".format(self.name))

        return self.results

    # build scope
    def build_scope(self):
        subscription_scope = '/subscription/' + self.subscription_id
        if self.scope is None:
            return subscription_scope
        return self.scope

    def create_roleassignment(self):
        '''
        Creates role assignment.

        :return: deserialized role assignment
        '''
        self.log("Creating role assignment {0}".format(self.name))

        try:
            parameters = RoleAssignmentCreateParameters(role_definition_id=self.role_definition_id, principal_id=self.principal_id)
            response = self._client.role_assignments.create(scope=self.scope,
                                                            name=self.name,
                                                            parameters=parameters)

        except CloudError as exc:
            self.log('Error attempting to create role assignment.')
            self.fail("Error creating role assignment: {0}".format(str(exc)))
        return roleassignment_to_dict(response)

    def delete_roleassignment(self):
        '''
        Deletes specified role assignment.

        :return: True
        '''
        self.log("Deleting the role assignment {0}".format(self.name))
        scope = 
        try:
            response = self._client.role_assignments.delete(name=self.name,
                                                            scope=self.scope)
        except CloudError as e:
            self.log('Error attempting to delete the role assignment.')
            self.fail("Error deleting the role assignment: {0}".format(str(e)))

        return True

    def get_roleassignment(self):
        '''
        Gets the properties of the specified role assignment.

        :return: deserialized role assignment dictionary
        '''
        self.log("Checking if the role assignment {0} is present".format(self.name))

        response = None

        try:
            response = list(self._client.role_assignments.get(scope=self.scope, role_assignment_name=self.name))

            return roleassignment_to_dict(response)

        except CloudError as ex:
            self.log("Didn't find role assignment {0} in scope {1}".format(self.name, self.scope))

        return False


def main():
    """Main execution"""
    AzureRMRoleAssignment()


if __name__ == '__main__':
    main()