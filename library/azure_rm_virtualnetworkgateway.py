#!/usr/bin/python
#
# Copyright (c) 2018 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_virtualnetworkgateway
version_added: "2.8"
short_description: Manage Azure Virtual Network Gateway instance.
description:
    - Create, update and delete instance of Azure Virtual Network Gateway.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the virtual network gateway.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    ip_configurations:
        description:
            - IP configurations for virtual network gateway.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            private_ip_allocation_method:
                description:
                    - "The private IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
                choices:
                    - 'static'
                    - 'dynamic'
            subnet:
                description:
                    - The reference of the subnet resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            public_ip_address:
                description:
                    - The reference of the public IP resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    gateway_type:
        description:
            - "The type of this virtual network gateway. Possible values are: 'C(vpn)' and 'C(express_route)'."
        choices:
            - 'vpn'
            - 'express_route'
    vpn_type:
        description:
            - "The type of this virtual network gateway. Possible values are: 'C(policy_based)' and 'C(route_based)'."
        choices:
            - 'policy_based'
            - 'route_based'
    enable_bgp:
        description:
            - Whether BGP is enabled for this virtual network gateway or not.
    active_active:
        description:
            - ActiveActive flag
    gateway_default_site:
        description:
            - "The reference of the LocalNetworkGateway resource which represents local network site having default routes. Assign Null value in case of
               removing existing default site setting."
        suboptions:
            id:
                description:
                    - Resource ID.
    sku:
        description:
            - The reference of the VirtualNetworkGatewaySku resource which represents the SKU selected for Virtual network gateway.
        suboptions:
            name:
                description:
                    - Gateway SKU name.
                choices:
                    - 'basic'
                    - 'high_performance'
                    - 'standard'
                    - 'ultra_performance'
                    - 'vpn_gw1'
                    - 'vpn_gw2'
                    - 'vpn_gw3'
            tier:
                description:
                    - Gateway SKU tier.
                choices:
                    - 'basic'
                    - 'high_performance'
                    - 'standard'
                    - 'ultra_performance'
                    - 'vpn_gw1'
                    - 'vpn_gw2'
                    - 'vpn_gw3'
            capacity:
                description:
                    - The capacity.
    vpn_client_configuration:
        description:
            - The reference of the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        suboptions:
            vpn_client_address_pool:
                description:
                    - The reference of the address space resource which represents Address space for P2S VpnClient.
                suboptions:
                    address_prefixes:
                        description:
                            - A list of address blocks reserved for this virtual network in CIDR notation.
                        type: list
            vpn_client_root_certificates:
                description:
                    - VpnClientRootCertificate for virtual network gateway.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    public_cert_data:
                        description:
                            - The certificate public data.
                            - Required when C(state) is I(present).
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            vpn_client_revoked_certificates:
                description:
                    - VpnClientRevokedCertificate for Virtual network gateway.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    thumbprint:
                        description:
                            - The revoked VPN client certificate thumbprint.
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            vpn_client_protocols:
                description:
                    - VpnClientProtocols for Virtual network gateway.
                type: list
            radius_server_address:
                description:
                    - The radius server address property of the VirtualNetworkGateway resource for vpn client connection.
            radius_server_secret:
                description:
                    - The radius secret property of the VirtualNetworkGateway resource for vpn client connection.
    bgp_settings:
        description:
            - "Virtual network gateway's BGP speaker settings."
        suboptions:
            asn:
                description:
                    - "The BGP speaker's ASN."
            bgp_peering_address:
                description:
                    - The BGP peering address and BGP identifier of this BGP speaker.
            peer_weight:
                description:
                    - The weight added to routes learned from this BGP speaker.
    resource_guid:
        description:
            - The resource GUID property of the VirtualNetworkGateway resource.
    state:
      description:
        - Assert the state of the Virtual Network Gateway.
        - Use 'present' to create or update an Virtual Network Gateway and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Virtual Network Gateway
    azure_rm_virtualnetworkgateway:
      resource_group: NOT FOUND
      name: NOT FOUND
      location: eastus
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualNetworkGateway(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network Gateway resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            ip_configurations=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    private_ip_allocation_method=dict(
                        type='str',
                        choices=['static',
                                 'dynamic']
                    ),
                    subnet=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    public_ip_address=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            gateway_type=dict(
                type='str',
                choices=['vpn',
                         'express_route']
            ),
            vpn_type=dict(
                type='str',
                choices=['policy_based',
                         'route_based']
            ),
            enable_bgp=dict(
                type='str'
            ),
            active_active=dict(
                type='str'
            ),
            gateway_default_site=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['basic',
                                 'high_performance',
                                 'standard',
                                 'ultra_performance',
                                 'vpn_gw1',
                                 'vpn_gw2',
                                 'vpn_gw3']
                    ),
                    tier=dict(
                        type='str',
                        choices=['basic',
                                 'high_performance',
                                 'standard',
                                 'ultra_performance',
                                 'vpn_gw1',
                                 'vpn_gw2',
                                 'vpn_gw3']
                    ),
                    capacity=dict(
                        type='int'
                    )
                )
            ),
            vpn_client_configuration=dict(
                type='dict',
                options=dict(
                    vpn_client_address_pool=dict(
                        type='dict',
                        options=dict(
                            address_prefixes=dict(
                                type='list'
                            )
                        )
                    ),
                    vpn_client_root_certificates=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            public_cert_data=dict(
                                type='str'
                            ),
                            name=dict(
                                type='str'
                            )
                        )
                    ),
                    vpn_client_revoked_certificates=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            thumbprint=dict(
                                type='str'
                            ),
                            name=dict(
                                type='str'
                            )
                        )
                    ),
                    vpn_client_protocols=dict(
                        type='list'
                    ),
                    radius_server_address=dict(
                        type='str'
                    ),
                    radius_server_secret=dict(
                        type='str'
                    )
                )
            ),
            bgp_settings=dict(
                type='dict',
                options=dict(
                    asn=dict(
                        type='int'
                    ),
                    bgp_peering_address=dict(
                        type='str'
                    ),
                    peer_weight=dict(
                        type='int'
                    )
                )
            ),
            resource_guid=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualNetworkGateway, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['ip_configurations', 'private_ip_allocation_method'], True)
        dict_resource_id(self.parameters, ['ip_configurations', 'subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['ip_configurations', 'public_ip_address', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['gateway_type'], True)
        dict_camelize(self.parameters, ['vpn_type'], True)
        dict_resource_id(self.parameters, ['gateway_default_site', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_camelize(self.parameters, ['sku', 'tier'], True)
        dict_resource_id(self.parameters, ['vpn_client_configuration', 'vpn_client_root_certificates', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['vpn_client_configuration', 'vpn_client_revoked_certificates', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualnetworkgateway()

        if not old_response:
            self.log("Virtual Network Gateway instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network Gateway instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Gateway instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkgateway()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network Gateway instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkgateway()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Network Gateway instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualnetworkgateway(self):
        '''
        Creates or updates Virtual Network Gateway with the specified configuration.

        :return: deserialized Virtual Network Gateway instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Gateway instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_network_gateways.create_or_update(resource_group_name=self.resource_group,
                                                                                  virtual_network_gateway_name=self.name,
                                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network Gateway instance.')
            self.fail("Error creating the Virtual Network Gateway instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkgateway(self):
        '''
        Deletes specified Virtual Network Gateway instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_network_gateways.delete(resource_group_name=self.resource_group,
                                                                        virtual_network_gateway_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Gateway instance.')
            self.fail("Error deleting the Virtual Network Gateway instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkgateway(self):
        '''
        Gets the properties of the specified Virtual Network Gateway.

        :return: deserialized Virtual Network Gateway instance state dictionary
        '''
        self.log("Checking if the Virtual Network Gateway instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_gateways.get(resource_group_name=self.resource_group,
                                                                     virtual_network_gateway_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Gateway instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Gateway instance.')
        if found is True:
            return response.as_dict()

        return False


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            else:
                key = list(old[0])[0]
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMVirtualNetworkGateway()


if __name__ == '__main__':
    main()
