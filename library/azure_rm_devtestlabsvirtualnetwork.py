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
module: azure_rm_devtestlabsvirtualnetwork
version_added: "2.8"
short_description: Manage Azure Virtual Network instance.
description:
    - Create, update and delete instance of Azure Virtual Network.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    lab_name:
        description:
            - The name of the lab.
        required: True
    name:
        description:
            - The name of the virtual network.
        required: True
    location:
        description:
            - The location of the resource.
    description:
        description:
            - The description of the virtual network.
    external_provider_resource_id:
        description:
            - The Microsoft.Network resource identifier of the virtual network.
    subnet_overrides:
        description:
            - The subnet overrides of the virtual network.
        type: list
        suboptions:
            resource_id:
                description:
                    - The resource ID of the subnet.
            lab_subnet_name:
                description:
                    - The name given to the subnet within the lab.
            use_in_vm_creation_permission:
                description:
                    - Indicates whether this subnet can be used during virtual machine creation (i.e. C(C(allow)), C(C(deny))).
                choices:
                    - 'default'
                    - 'deny'
                    - 'allow'
            use_public_ip_address_permission:
                description:
                    - Indicates whether public IP addresses can be assigned to virtual machines on this subnet (i.e. C(C(allow)), C(C(deny))).
                choices:
                    - 'default'
                    - 'deny'
                    - 'allow'
            shared_public_ip_address_configuration:
                description:
                    - Properties that virtual machines on this subnet will share.
                suboptions:
                    allowed_ports:
                        description:
                            - Backend ports that virtual machines on this subnet are allowed to expose
                        type: list
                        suboptions:
                            transport_protocol:
                                description:
                                    - Protocol type of the port.
                                choices:
                                    - 'tcp'
                                    - 'udp'
                            backend_port:
                                description:
                                    - Backend port of the target virtual machine.
            virtual_network_pool_name:
                description:
                    - The virtual network pool associated with this subnet.
    state:
      description:
        - Assert the state of the Virtual Network.
        - Use 'present' to create or update an Virtual Network and 'absent' to delete it.
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
  - name: Create (or update) Virtual Network
    azure_rm_devtestlabsvirtualnetwork:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The identifier of the resource.
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
    from azure.mgmt.devtestlabs import DevTestLabsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualNetwork(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            lab_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            external_provider_resource_id=dict(
                type='str'
            ),
            subnet_overrides=dict(
                type='list',
                options=dict(
                    resource_id=dict(
                        type='str'
                    ),
                    lab_subnet_name=dict(
                        type='str'
                    ),
                    use_in_vm_creation_permission=dict(
                        type='str',
                        choices=['default',
                                 'deny',
                                 'allow']
                    ),
                    use_public_ip_address_permission=dict(
                        type='str',
                        choices=['default',
                                 'deny',
                                 'allow']
                    ),
                    shared_public_ip_address_configuration=dict(
                        type='dict',
                        options=dict(
                            allowed_ports=dict(
                                type='list',
                                options=dict(
                                    transport_protocol=dict(
                                        type='str',
                                        choices=['tcp',
                                                 'udp']
                                    ),
                                    backend_port=dict(
                                        type='int'
                                    )
                                )
                            )
                        )
                    ),
                    virtual_network_pool_name=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.lab_name = None
        self.name = None
        self.virtual_network = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualNetwork, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.virtual_network[key] = kwargs[key]

        dict_resource_id(self.virtual_network, ['external_provider_resource_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.virtual_network, ['subnet_overrides', 'resource_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.virtual_network, ['subnet_overrides', 'use_in_vm_creation_permission'], True)
        dict_camelize(self.virtual_network, ['subnet_overrides', 'use_public_ip_address_permission'], True)
        dict_camelize(self.virtual_network, ['subnet_overrides', 'shared_public_ip_address_configuration', 'allowed_ports', 'transport_protocol'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_virtualnetwork()

        if not old_response:
            self.log("Virtual Network instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.virtual_network, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetwork()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetwork()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Network instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualnetwork(self):
        '''
        Creates or updates Virtual Network with the specified configuration.

        :return: deserialized Virtual Network instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_networks.create_or_update(resource_group_name=self.resource_group,
                                                                          lab_name=self.lab_name,
                                                                          name=self.name,
                                                                          virtual_network=self.virtual_network)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network instance.')
            self.fail("Error creating the Virtual Network instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetwork(self):
        '''
        Deletes specified Virtual Network instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_networks.delete(resource_group_name=self.resource_group,
                                                                lab_name=self.lab_name,
                                                                name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network instance.')
            self.fail("Error deleting the Virtual Network instance: {0}".format(str(e)))

        return True

    def get_virtualnetwork(self):
        '''
        Gets the properties of the specified Virtual Network.

        :return: deserialized Virtual Network instance state dictionary
        '''
        self.log("Checking if the Virtual Network instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_networks.get(resource_group_name=self.resource_group,
                                                             lab_name=self.lab_name,
                                                             name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network instance.')
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
    AzureRMVirtualNetwork()


if __name__ == '__main__':
    main()
