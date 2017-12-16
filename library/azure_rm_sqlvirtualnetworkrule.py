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
module: azure_rm_sqlvirtualnetworkrule
version_added: "2.5"
short_description: Manage VirtualNetworkRules instance
description:
    - Create, update and delete instance of VirtualNetworkRules

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    virtual_network_rule_name:
        description:
            - The name of the virtual network rule.
        required: True
    virtual_network_subnet_id:
        description:
            - The ARM resource id of the virtual network subnet.
        required: True
    ignore_missing_vnet_service_endpoint:
        description:
            - Create firewall rule before the virtual network has vnet service endpoint enabled.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) VirtualNetworkRules
    azure_rm_sqlvirtualnetworkrule:
      resource_group: Default
      server_name: vnet-test-svr
      virtual_network_rule_name: vnet-firewall-rule
      virtual_network_subnet_id: NOT FOUND
      ignore_missing_vnet_service_endpoint: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
state:
    description:
        - "Virtual Network Rule State. Possible values include: 'Initializing', 'InProgress', 'Ready', 'Deleting', 'Unknown'"
    returned: always
    type: str
    sample: state
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualNetworkRules(AzureRMModuleBase):
    """Configuration class for an Azure RM VirtualNetworkRules resource"""

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
            virtual_network_rule_name=dict(
                type='str',
                required=True
            ),
            virtual_network_subnet_id=dict(
                type='str',
                required=True
            ),
            ignore_missing_vnet_service_endpoint=dict(
                type='str',
                required=False
            ),
            state=dict(
                type='str',
                required=False,
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.virtual_network_rule_name = None
        self.virtual_network_subnet_id = None
        self.ignore_missing_vnet_service_endpoint = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualNetworkRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_virtualnetworkrules()

        if not old_response:
            self.log("VirtualNetworkRules instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("VirtualNetworkRules instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if VirtualNetworkRules instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the VirtualNetworkRules instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkrules()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("VirtualNetworkRules instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkrules()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_virtualnetworkrules():
                time.sleep(20)
        else:
            self.log("VirtualNetworkRules instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]
            self.results["state"] = response["state"]

        return self.results

    def create_update_virtualnetworkrules(self):
        '''
        Creates or updates VirtualNetworkRules with the specified configuration.

        :return: deserialized VirtualNetworkRules instance state dictionary
        '''
        self.log("Creating / Updating the VirtualNetworkRules instance {0}".format(self.virtual_network_rule_name))

        try:
            response = self.mgmt_client.virtual_network_rules.create_or_update(self.resource_group,
                                                                               self.server_name,
                                                                               self.virtual_network_rule_name,
                                                                               self.virtual_network_subnet_id)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the VirtualNetworkRules instance.')
            self.fail("Error creating the VirtualNetworkRules instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkrules(self):
        '''
        Deletes specified VirtualNetworkRules instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the VirtualNetworkRules instance {0}".format(self.virtual_network_rule_name))
        try:
            response = self.mgmt_client.virtual_network_rules.delete(self.resource_group,
                                                                     self.server_name,
                                                                     self.virtual_network_rule_name)
        except CloudError as e:
            self.log('Error attempting to delete the VirtualNetworkRules instance.')
            self.fail("Error deleting the VirtualNetworkRules instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkrules(self):
        '''
        Gets the properties of the specified VirtualNetworkRules.

        :return: deserialized VirtualNetworkRules instance state dictionary
        '''
        self.log("Checking if the VirtualNetworkRules instance {0} is present".format(self.virtual_network_rule_name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_rules.get(self.resource_group,
                                                                  self.server_name,
                                                                  self.virtual_network_rule_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("VirtualNetworkRules instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the VirtualNetworkRules instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMVirtualNetworkRules()

if __name__ == '__main__':
    main()
