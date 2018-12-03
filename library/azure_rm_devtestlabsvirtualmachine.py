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
module: azure_rm_devtestlabsvirtualmachine
version_added: "2.8"
short_description: Manage Azure Virtual Machine instance.
description:
    - Create, update and delete instance of Azure Virtual Machine.

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
            - The name of the virtual machine.
        required: True
    location:
        description:
            - The location of the resource.
    notes:
        description:
            - The notes of the virtual machine.
    owner_object_id:
        description:
            - The object identifier of the owner of the virtual machine.
    owner_user_principal_name:
        description:
            - The user principal name of the virtual machine owner.
    created_by_user_id:
        description:
            - The object identifier of the creator of the virtual machine.
    created_by_user:
        description:
            - The email address of creator of the virtual machine.
    created_date:
        description:
            - The creation date of the virtual machine.
    custom_image_id:
        description:
            - The custom image identifier of the virtual machine.
    os_type:
        description:
            - The OS type of the virtual machine.
    size:
        description:
            - The size of the virtual machine.
    user_name:
        description:
            - The user name of the virtual machine.
    password:
        description:
            - The password of the virtual machine administrator.
    ssh_key:
        description:
            - The SSH key of the virtual machine administrator.
    is_authentication_with_ssh_key:
        description:
            - Indicates whether this virtual machine uses an SSH key for authentication.
    fqdn:
        description:
            - The fully-qualified domain name of the virtual machine.
    lab_subnet_name:
        description:
            - The lab subnet name of the virtual machine.
    lab_virtual_network_id:
        description:
            - The lab virtual network identifier of the virtual machine.
    disallow_public_ip_address:
        description:
            - Indicates whether the virtual machine is to be created without a public IP address.
    artifacts:
        description:
            - The artifacts to be installed on the virtual machine.
        type: list
        suboptions:
            artifact_id:
                description:
                    - "The artifact's identifier."
            parameters:
                description:
                    - The parameters of the artifact.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the artifact parameter.
                    value:
                        description:
                            - The value of the artifact parameter.
    gallery_image_reference:
        description:
            - The Microsoft Azure Marketplace image reference of the virtual machine.
        suboptions:
            offer:
                description:
                    - The offer of the gallery image.
            publisher:
                description:
                    - The publisher of the gallery image.
            sku:
                description:
                    - The SKU of the gallery image.
            os_type:
                description:
                    - The OS type of the gallery image.
            version:
                description:
                    - The version of the gallery image.
    network_interface:
        description:
            - The network interface properties.
        suboptions:
            virtual_network_id:
                description:
                    - The resource ID of the virtual network.
            subnet_id:
                description:
                    - The resource ID of the sub net.
            public_ip_address_id:
                description:
                    - The resource ID of the public IP address.
            public_ip_address:
                description:
                    - The public IP address.
            private_ip_address:
                description:
                    - The private IP address.
            dns_name:
                description:
                    - The DNS name.
            rdp_authority:
                description:
                    - The RdpAuthority property is a server DNS host name or IP address followed by the service port number for RDP (Remote Desktop Protocol).
            ssh_authority:
                description:
                    - The SshAuthority property is a server DNS host name or IP address followed by the service port number for SSH.
            shared_public_ip_address_configuration:
                description:
                    - The configuration for sharing a public IP address across multiple virtual machines.
                suboptions:
                    inbound_nat_rules:
                        description:
                            - The incoming NAT rules
                        type: list
                        suboptions:
                            transport_protocol:
                                description:
                                    - The transport protocol for the endpoint.
                                choices:
                                    - 'tcp'
                                    - 'udp'
                            frontend_port:
                                description:
                                    - "The external endpoint port of the inbound connection. Possible values range between 1 and 65535, inclusive. If
                                       unspecified, a value will be allocated automatically."
                            backend_port:
                                description:
                                    - The port to which the external traffic will be redirected.
    expiration_date:
        description:
            - The expiration date for VM.
    allow_claim:
        description:
            - Indicates whether another user can take ownership of the virtual machine
    storage_type:
        description:
            - Storage type to use for virtual machine (i.e. Standard, Premium).
    environment_id:
        description:
            - The resource ID of the environment that contains this virtual machine, if any.
    state:
      description:
        - Assert the state of the Virtual Machine.
        - Use 'present' to create or update an Virtual Machine and 'absent' to delete it.
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
  - name: Create (or update) Virtual Machine
    azure_rm_devtestlabsvirtualmachine:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
      name: NOT FOUND
      applicable_schedule:
        lab_vms_shutdown:
          status: status
          notification_settings:
            status: status
        lab_vms_startup:
          status: status
          notification_settings:
            status: status
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


class AzureRMVirtualMachine(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine resource"""

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
            notes=dict(
                type='str'
            ),
            owner_object_id=dict(
                type='str'
            ),
            owner_user_principal_name=dict(
                type='str'
            ),
            created_by_user_id=dict(
                type='str'
            ),
            created_by_user=dict(
                type='str'
            ),
            created_date=dict(
                type='datetime'
            ),
            custom_image_id=dict(
                type='str'
            ),
            os_type=dict(
                type='str'
            ),
            size=dict(
                type='str'
            ),
            user_name=dict(
                type='str'
            ),
            password=dict(
                type='str',
                no_log=True
            ),
            ssh_key=dict(
                type='str'
            ),
            is_authentication_with_ssh_key=dict(
                type='str'
            ),
            fqdn=dict(
                type='str'
            ),
            lab_subnet_name=dict(
                type='str'
            ),
            lab_virtual_network_id=dict(
                type='str'
            ),
            disallow_public_ip_address=dict(
                type='str'
            ),
            artifacts=dict(
                type='list',
                options=dict(
                    artifact_id=dict(
                        type='str'
                    ),
                    parameters=dict(
                        type='list',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            value=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            gallery_image_reference=dict(
                type='dict',
                options=dict(
                    offer=dict(
                        type='str'
                    ),
                    publisher=dict(
                        type='str'
                    ),
                    sku=dict(
                        type='str'
                    ),
                    os_type=dict(
                        type='str'
                    ),
                    version=dict(
                        type='str'
                    )
                )
            ),
            network_interface=dict(
                type='dict',
                options=dict(
                    virtual_network_id=dict(
                        type='str'
                    ),
                    subnet_id=dict(
                        type='str'
                    ),
                    public_ip_address_id=dict(
                        type='str'
                    ),
                    public_ip_address=dict(
                        type='str'
                    ),
                    private_ip_address=dict(
                        type='str'
                    ),
                    dns_name=dict(
                        type='str'
                    ),
                    rdp_authority=dict(
                        type='str'
                    ),
                    ssh_authority=dict(
                        type='str'
                    ),
                    shared_public_ip_address_configuration=dict(
                        type='dict',
                        options=dict(
                            inbound_nat_rules=dict(
                                type='list',
                                options=dict(
                                    transport_protocol=dict(
                                        type='str',
                                        choices=['tcp',
                                                 'udp']
                                    ),
                                    frontend_port=dict(
                                        type='int'
                                    ),
                                    backend_port=dict(
                                        type='int'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            expiration_date=dict(
                type='datetime'
            ),
            allow_claim=dict(
                type='str'
            ),
            storage_type=dict(
                type='str'
            ),
            environment_id=dict(
                type='str'
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
        self.lab_virtual_machine = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualMachine, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.lab_virtual_machine[key] = kwargs[key]

        dict_resource_id(self.lab_virtual_machine, ['owner_object_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['created_by_user_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['custom_image_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['lab_virtual_network_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['artifacts', 'artifact_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['network_interface', 'virtual_network_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['network_interface', 'subnet_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.lab_virtual_machine, ['network_interface', 'public_ip_address_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.lab_virtual_machine, ['network_interface', 'shared_public_ip_address_configuration', 'inbound_nat_rules', 'transport_protocol'], True)
        dict_resource_id(self.lab_virtual_machine, ['environment_id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_virtualmachine()

        if not old_response:
            self.log("Virtual Machine instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Machine instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.lab_virtual_machine, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachine()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachine()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Machine instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualmachine(self):
        '''
        Creates or updates Virtual Machine with the specified configuration.

        :return: deserialized Virtual Machine instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_machines.create_or_update(resource_group_name=self.resource_group,
                                                                          lab_name=self.lab_name,
                                                                          name=self.name,
                                                                          lab_virtual_machine=self.lab_virtual_machine)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Machine instance.')
            self.fail("Error creating the Virtual Machine instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualmachine(self):
        '''
        Deletes specified Virtual Machine instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Machine instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_machines.delete(resource_group_name=self.resource_group,
                                                                lab_name=self.lab_name,
                                                                name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine instance.')
            self.fail("Error deleting the Virtual Machine instance: {0}".format(str(e)))

        return True

    def get_virtualmachine(self):
        '''
        Gets the properties of the specified Virtual Machine.

        :return: deserialized Virtual Machine instance state dictionary
        '''
        self.log("Checking if the Virtual Machine instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_machines.get(resource_group_name=self.resource_group,
                                                             lab_name=self.lab_name,
                                                             name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine instance.')
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
    AzureRMVirtualMachine()


if __name__ == '__main__':
    main()
