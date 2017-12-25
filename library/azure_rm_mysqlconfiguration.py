#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_mysqlconfiguration
version_added: "2.5"
short_description: Manage Configurations instance.
description:
    - Create, update and delete instance of Configurations.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the server configuration.
        required: True
    parameters:
        description:
            - The required parameters for updating a server configuration.
    value:
        description:
            - Value of the configuration.
    source:
        description:
            - Source of the configuration.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Configurations
    azure_rm_mysqlconfiguration:
      resource_group: TestGroup
      server_name: testserver
      name: event_scheduler
      parameters: parameters
'''

RETURN = '''
id:
    description:
        - Resource ID
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.rdbms.mysql import MySQLManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConfigurations(AzureRMModuleBase):
    """Configuration class for an Azure RM Configurations resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            parameters=dict(
                type='dict'
            ),
            value=dict(
                type='str'
            ),
            source=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.value = None
        self.source = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConfigurations, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MySQLManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_configurations()

        if not old_response:
            self.log("Configurations instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Configurations instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Configurations instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Configurations instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_configurations()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Configurations instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_configurations()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_configurations():
                time.sleep(20)
        else:
            self.log("Configurations instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_configurations(self):
        '''
        Creates or updates Configurations with the specified configuration.

        :return: deserialized Configurations instance state dictionary
        '''
        self.log("Creating / Updating the Configurations instance {0}".format(self.name))

        try:
            response = self.mgmt_client.configurations.create_or_update(self.resource_group,
                                                                        self.server_name,
                                                                        self.name,
                                                                        self.value,
                                                                        self.source)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Configurations instance.')
            self.fail("Error creating the Configurations instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_configurations(self):
        '''
        Deletes specified Configurations instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Configurations instance {0}".format(self.name))
        try:
            response = self.mgmt_client.configurations.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Configurations instance.')
            self.fail("Error deleting the Configurations instance: {0}".format(str(e)))

        return True

    def get_configurations(self):
        '''
        Gets the properties of the specified Configurations.

        :return: deserialized Configurations instance state dictionary
        '''
        self.log("Checking if the Configurations instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.configurations.get(self.resource_group,
                                                           self.server_name,
                                                           self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Configurations instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Configurations instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMConfigurations()

if __name__ == '__main__':
    main()
