#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_virtualmachinescalesetextension

version_added: "2.8"

short_description: Managed Azure Virtual Machine Scale Set extension

description:
    - Create, update and delete Azure Virtual Machine Extension

options:
    resource_group:
        description:
            - Name of a resource group where the VMSS extension exists or will be created.
        required: true
    name:
        description:
            - Name of the VMSS extension
        required: true
    location:
        description:
            - Valid azure location. Defaults to location of the resource group.
    vmss_name:
        description:
            - The name of the virtual machine where the extension should be create or updated.
    publisher:
        description:
            - The name of the extension handler publisher.
    type:
        description:
            - The type of the extension handler.
    type_handler_version:
        description:
            - The type version of the extension handler.
    settings:
        description:
            - Json formatted public settings for the extension.
    protected_settings:
        description:
            - Json formatted protected settings for the extension.
    auto_upgrade_minor_version:
        description:
            - Whether the extension handler should be automatically upgraded across minor versions.
        type: bool
    state:
        description:
            - Assert the state of the SQL server. Use 'present' to create or update a server and
              'absent' to delete a server.
        default: present
        choices:
            - absent
            - present


extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"
'''

EXAMPLES = '''
    - name: Create VMSS Extension
      azure_rm_virtualmachinescalesetextension:
        name: myvmssextension
        location: eastus
        resource_group: Testing
        vmss_name: myvm
        publisher: Microsoft.Azure.Extensions
        type: CustomScript
        type_handler_version: 2.0
        settings: '{"commandToExecute": "hostname"}'
        auto_upgrade_minor_version: true

    - name: Delete VMSS Extension
      azure_rm_virtualmachinescalesetextension:
        name: myvmssextension
        location: eastus
        resource_group: Testing
        vmss_name: myvm
        state: absent
'''

RETURN = '''
state:
    description: Current state of the VMSS extension
    returned: always
    type: dict
changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVMSSExtension(AzureRMModuleBase):

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
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str'
            ),
            vmss_name=dict(
                type='str'
            ),
            publisher=dict(
                type='str'
            ),
            type=dict(
                type='str'
            ),
            type_handler_version=dict(
                type='str'
            ),
            auto_upgrade_minor_version=dict(
                type='bool'
            ),
            settings=dict(
                type='dict'
            ),
            protected_settings=dict(
                type='dict'
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.publisher = None
        self.type = None
        self.type_handler_version = None
        self.auto_upgrade_minor_version = None
        self.settings = None
        self.protected_settings = None
        self.state = None

        self.results = dict(changed=False, state=dict())

        super(AzureRMVMSSExtension, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=False,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        resource_group = None
        response = None
        to_be_updated = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        if self.state == 'present':
            response = self.get_vmssextension()
            if not response:
                to_be_updated = True
            else:
                if self.settings is not None and response.get('settings') != self.settings:
                    response['settings'] = self.settings
                    to_be_updated = True

                if self.protected_settings is not None and response.get('protected_settings') != self.protected_settings:
                    response['protected_settings'] = self.protected_settings
                    to_be_updated = True

            if to_be_updated:
                self.results['changed'] = True
                self.results['state'] = self.create_or_update_vmssextension()
        elif self.state == 'absent':
            self.delete_vmssextension()
            self.results['changed'] = True

        return self.results

    def create_or_update_vmssextension(self):
        self.log("Creating VMSS extension {0}".format(self.name))
        try:
            params = self.compute_models.VirtualMachineScaleSetExtension(
                location=self.location,
                publisher=self.publisher,
                type=self.type,
                type_handler_version=self.type_handler_version,
                auto_upgrade_minor_version=self.auto_upgrade_minor_version,
                settings=self.settings,
                protected_settings=self.protected_settings
            )
            poller = self.compute_client.virtual_machine_scale_set_extensions.create_or_update(resource_group_name=self.resource_group,
                                                                                               vm_scale_set_name=self.vmss_name,
                                                                                               vmss_extension_name=self.name,
                                                                                               extension_parameters=params)
            response = self.get_poller_result(poller)
            return response.as_dict()

        except CloudError as e:
            self.log('Error attempting to create the VMSS extension.')
            self.fail("Error creating the VMSS extension: {0}".format(str(e)))

    def delete_vmssextension(self):
        self.log("Deleting vmextension {0}".format(self.name))
        try:
            poller = self.compute_client.virtual_machine_scale_set_extensions.delete(resource_group_name=self.resource_group,
                                                                                     vm_scale_set_name=self.vmss_name,
                                                                                     vmss_extension_name=self.name)
            self.get_poller_result(poller)
        except CloudError as e:
            self.log('Error attempting to delete the vmextension.')
            self.fail("Error deleting the vmextension: {0}".format(str(e)))

    def get_vmssextension(self):
        self.log("Checking if the VMSS extension {0} is present".format(self.name))
        found = False
        try:
            response = self.compute_client.virtual_machine_scale_set_extensions.get(self.resource_group, self.vmss_name, self.name)
            found = True
        except CloudError as e:
            self.log('Did not find VMSS extension')
        if found:
            return response.as_dict()
        else:
            return False


def main():
    AzureRMVMSSExtension()


if __name__ == '__main__':
    main()
