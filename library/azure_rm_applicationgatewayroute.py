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
module: azure_rm_applicationgatewayroute
version_added: "2.5"
short_description: Manage Routes instance.
description:
    - Create, update and delete instance of Routes.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    route_table_name:
        description:
            - The name of the route table.
        required: True
    route_name:
        description:
            - The name of the route.
        required: True
    id:
        description:
            - Resource ID.
    address_prefix:
        description:
            - The destination CIDR to which the route applies.
    next_hop_type:
        description:
            - "The type of Azure hop the packet should be sent to. Possible values are: C(VirtualNetworkGateway), C(VnetLocal), C(Internet), C(VirtualApplian
               ce), and C(None). Possible values include: C(VirtualNetworkGateway), C(VnetLocal), C(Internet), C(VirtualAppliance), C(None)"
        choices: ['virtual_network_gateway', 'vnet_local', 'internet', 'virtual_appliance', 'none']
    next_hop_ip_address:
        description:
            - The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
    provisioning_state:
        description:
            - The provisioning state of the resource. Possible values are: C(Updating), C(Deleting), and C(Failed).
    name:
        description:
            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    etag:
        description:
            - A unique read-only string that changes whenever the resource is updated.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Routes
    azure_rm_applicationgatewayroute:
      resource_group: rg1
      route_table_name: testrt
      route_name: route1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRoutes(AzureRMModuleBase):
    """Configuration class for an Azure RM Routes resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            route_table_name=dict(
                type='str',
                required=True
            ),
            route_name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            address_prefix=dict(
                type='str'
            ),
            next_hop_type=dict(
                type='str',
                choices=['virtual_network_gateway', 'vnet_local', 'internet', 'virtual_appliance', 'none']
            ),
            next_hop_ip_address=dict(
                type='str'
            ),
            provisioning_state=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            etag=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.route_table_name = None
        self.route_name = None
        self.route_parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRoutes, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "id":
                    self.route_parameters["id"] = kwargs[key]
                elif key == "address_prefix":
                    self.route_parameters["address_prefix"] = kwargs[key]
                elif key == "next_hop_type":
                    ev = kwargs[key]
                    if ev == 'virtual_network_gateway':
                        ev = 'VirtualNetworkGateway'
                    elif ev == 'vnet_local':
                        ev = 'VnetLocal'
                    elif ev == 'internet':
                        ev = 'Internet'
                    elif ev == 'virtual_appliance':
                        ev = 'VirtualAppliance'
                    elif ev == 'none':
                        ev = 'None'
                    self.route_parameters["next_hop_type"] = ev
                elif key == "next_hop_ip_address":
                    self.route_parameters["next_hop_ip_address"] = kwargs[key]
                elif key == "provisioning_state":
                    self.route_parameters["provisioning_state"] = kwargs[key]
                elif key == "name":
                    self.route_parameters["name"] = kwargs[key]
                elif key == "etag":
                    self.route_parameters["etag"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_routes()

        if not old_response:
            self.log("Routes instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Routes instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Routes instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Routes instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_routes()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Routes instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_routes()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_routes():
                time.sleep(20)
        else:
            self.log("Routes instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_routes(self):
        '''
        Creates or updates Routes with the specified configuration.

        :return: deserialized Routes instance state dictionary
        '''
        self.log("Creating / Updating the Routes instance {0}".format(self.route_name))

        try:
            response = self.mgmt_client.routes.create_or_update(resource_group_name=self.resource_group,
                                                                route_table_name=self.route_table_name,
                                                                route_name=self.route_name,
                                                                route_parameters=self.route_parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Routes instance.')
            self.fail("Error creating the Routes instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_routes(self):
        '''
        Deletes specified Routes instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Routes instance {0}".format(self.route_name))
        try:
            response = self.mgmt_client.routes.delete(resource_group_name=self.resource_group,
                                                      route_table_name=self.route_table_name,
                                                      route_name=self.route_name)
        except CloudError as e:
            self.log('Error attempting to delete the Routes instance.')
            self.fail("Error deleting the Routes instance: {0}".format(str(e)))

        return True

    def get_routes(self):
        '''
        Gets the properties of the specified Routes.

        :return: deserialized Routes instance state dictionary
        '''
        self.log("Checking if the Routes instance {0} is present".format(self.route_name))
        found = False
        try:
            response = self.mgmt_client.routes.get(resource_group_name=self.resource_group,
                                                   route_table_name=self.route_table_name,
                                                   route_name=self.route_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Routes instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Routes instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMRoutes()

if __name__ == '__main__':
    main()
