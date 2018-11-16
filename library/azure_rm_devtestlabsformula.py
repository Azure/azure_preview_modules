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
module: azure_rm_devtestlabsformula
version_added: "2.8"
short_description: Manage Formula instance.
description:
    - Create, update and delete instance of Formula.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the lab.
        required: True
    name:
        description:
            - The name of the I(formula).
        required: True
    formula:
        description:
            - A formula for creating a VM, specifying an image base and other parameters
        required: True
        suboptions:
            location:
                description:
                    - The location of the resource.
            description:
                description:
                    - The description of the formula.
            author:
                description:
                    - The author of the formula.
            os_type:
                description:
                    - The OS type of the formula.
            formula_content:
                description:
                    - The content of the formula.
                suboptions:
                    bulk_creation_parameters:
                        description:
                            - The number of virtual machine instances to create.
                        suboptions:
                            instance_count:
                                description:
                                    - The number of virtual machine instances to create.
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
                            status:
                                description:
                                    - The status of the artifact.
                            deployment_status_message:
                                description:
                                    - The I(status) message from the deployment.
                            vm_extension_status_message:
                                description:
                                    - The I(status) message from the virtual machine extension.
                            install_time:
                                description:
                                    - The time that the artifact starts to install on the virtual machine.
                    artifact_deployment_status:
                        description:
                            - The artifact deployment status for the virtual machine.
                        suboptions:
                            deployment_status:
                                description:
                                    - The deployment status of the artifact.
                            artifacts_applied:
                                description:
                                    - The total count of the artifacts that were successfully applied.
                            total_artifacts:
                                description:
                                    - The total count of the artifacts that were tentatively applied.
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
                    compute_vm:
                        description:
                            - The compute virtual machine properties.
                        suboptions:
                            statuses:
                                description:
                                    - Gets the statuses of the virtual machine.
                                type: list
                                suboptions:
                                    code:
                                        description:
                                            - Gets the status Code.
                                    display_status:
                                        description:
                                            - Gets the short localizable label for the status.
                                    message:
                                        description:
                                            - Gets the message associated with the status.
                            os_type:
                                description:
                                    - Gets the OS type of the virtual machine.
                            vm_size:
                                description:
                                    - Gets the size of the virtual machine.
                            network_interface_id:
                                description:
                                    - Gets the network interface ID of the virtual machine.
                            os_disk_id:
                                description:
                                    - Gets OS disk blob uri for the virtual machine.
                            data_disk_ids:
                                description:
                                    - Gets data disks blob uri for the virtual machine.
                                type: list
                            data_disks:
                                description:
                                    - Gets all data disks attached to the virtual machine.
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - Gets data disk name.
                                    disk_uri:
                                        description:
                                            - When backed by a blob, the URI of underlying blob.
                                    managed_disk_id:
                                        description:
                                            - When backed by managed disk, this is the ID of the compute disk resource.
                                    disk_size_gi_b:
                                        description:
                                            - Gets data disk size in GiB.
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
                                    - "The RdpAuthority property is a server DNS host name or IP address followed by the service port number for RDP (Remote
                                       Desktop Protocol)."
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
                                                    - "The external endpoint port of the inbound connection. Possible values range between 1 and 65535,
                                                       inclusive. If unspecified, a value will be allocated automatically."
                                            backend_port:
                                                description:
                                                    - The port to which the external traffic will be redirected.
                    applicable_schedule:
                        description:
                            - The applicable schedule for the virtual machine.
                        suboptions:
                            location:
                                description:
                                    - The location of the resource.
                            lab_vms_shutdown:
                                description:
                                    - The auto-shutdown schedule, if one has been set at the lab or lab resource level.
                                suboptions:
                                    location:
                                        description:
                                            - The location of the resource.
                                    status:
                                        description:
                                            - The status of the schedule (i.e. C(enabled), C(disabled)).
                                        choices:
                                            - 'enabled'
                                            - 'disabled'
                                    task_type:
                                        description:
                                            - The task type of the schedule (e.g. LabVmsShutdownTask, LabVmAutoStart).
                                    weekly_recurrence:
                                        description:
                                            - If the schedule will occur only some days of the week, specify the weekly recurrence.
                                        suboptions:
                                            weekdays:
                                                description:
                                                    - The days of the week for which the schedule is set (e.g. Sunday, Monday, Tuesday, etc.).
                                                type: list
                                            time:
                                                description:
                                                    - The time of the day the schedule will occur.
                                    daily_recurrence:
                                        description:
                                            - If the schedule will occur once each day of the week, specify the daily recurrence.
                                        suboptions:
                                            time:
                                                description:
                                                    - The time of day the schedule will occur.
                                    hourly_recurrence:
                                        description:
                                            - If the schedule will occur multiple times a day, specify the hourly recurrence.
                                        suboptions:
                                            minute:
                                                description:
                                                    - Minutes of the hour the schedule will run.
                                    time_zone_id:
                                        description:
                                            - The time zone ID (e.g. Pacific Standard time).
                                    notification_settings:
                                        description:
                                            - Notification settings.
                                        suboptions:
                                            status:
                                                description:
                                                    - If notifications are C(enabled) for this schedule (i.e. C(enabled), C(disabled)).
                                                choices:
                                                    - 'disabled'
                                                    - 'enabled'
                                            time_in_minutes:
                                                description:
                                                    - Time in minutes before event at which notification will be sent.
                                            webhook_url:
                                                description:
                                                    - The webhook URL to which the notification will be sent.
                                    target_resource_id:
                                        description:
                                            - The resource ID to which the schedule belongs
                                    unique_identifier:
                                        description:
                                            - The unique immutable identifier of a resource (Guid).
                            lab_vms_startup:
                                description:
                                    - The auto-startup schedule, if one has been set at the lab or lab resource level.
                                suboptions:
                                    location:
                                        description:
                                            - The location of the resource.
                                    status:
                                        description:
                                            - The status of the schedule (i.e. C(enabled), C(disabled)).
                                        choices:
                                            - 'enabled'
                                            - 'disabled'
                                    task_type:
                                        description:
                                            - The task type of the schedule (e.g. LabVmsShutdownTask, LabVmAutoStart).
                                    weekly_recurrence:
                                        description:
                                            - If the schedule will occur only some days of the week, specify the weekly recurrence.
                                        suboptions:
                                            weekdays:
                                                description:
                                                    - The days of the week for which the schedule is set (e.g. Sunday, Monday, Tuesday, etc.).
                                                type: list
                                            time:
                                                description:
                                                    - The time of the day the schedule will occur.
                                    daily_recurrence:
                                        description:
                                            - If the schedule will occur once each day of the week, specify the daily recurrence.
                                        suboptions:
                                            time:
                                                description:
                                                    - The time of day the schedule will occur.
                                    hourly_recurrence:
                                        description:
                                            - If the schedule will occur multiple times a day, specify the hourly recurrence.
                                        suboptions:
                                            minute:
                                                description:
                                                    - Minutes of the hour the schedule will run.
                                    time_zone_id:
                                        description:
                                            - The time zone ID (e.g. Pacific Standard time).
                                    notification_settings:
                                        description:
                                            - Notification settings.
                                        suboptions:
                                            status:
                                                description:
                                                    - If notifications are C(enabled) for this schedule (i.e. C(enabled), C(disabled)).
                                                choices:
                                                    - 'disabled'
                                                    - 'enabled'
                                            time_in_minutes:
                                                description:
                                                    - Time in minutes before event at which notification will be sent.
                                            webhook_url:
                                                description:
                                                    - The webhook URL to which the notification will be sent.
                                    target_resource_id:
                                        description:
                                            - The resource ID to which the schedule belongs
                                    unique_identifier:
                                        description:
                                            - The unique immutable identifier of a resource (Guid).
                    expiration_date:
                        description:
                            - The expiration date for VM.
                    allow_claim:
                        description:
                            - Indicates whether another user can take ownership of the virtual machine
                    storage_type:
                        description:
                            - Storage type to use for virtual machine (i.e. Standard, Premium).
                    virtual_machine_creation_source:
                        description:
                            - Tells source of creation of lab virtual machine. Output property only.
                        choices:
                            - 'from_custom_image'
                            - 'from_gallery_image'
                    environment_id:
                        description:
                            - The resource ID of the environment that contains this virtual machine, if any.
                    unique_identifier:
                        description:
                            - The unique immutable identifier of a resource (Guid).
                    name:
                        description:
                            - The name of the virtual machine or environment
                    location:
                        description:
                            - The location of the new virtual machine or environment
            vm:
                description:
                    - Information about a VM from which a formula is to be created.
                suboptions:
                    lab_vm_id:
                        description:
                            - The identifier of the VM from which a formula is to be created.
            unique_identifier:
                description:
                    - The unique immutable identifier of a resource (Guid).
    state:
      description:
        - Assert the state of the Formula.
        - Use 'present' to create or update an Formula and 'absent' to delete it.
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
  - name: Create (or update) Formula
    azure_rm_devtestlabsformula:
      resource_group: NOT FOUND
      name: NOT FOUND
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


class AzureRMFormulas(AzureRMModuleBase):
    """Configuration class for an Azure RM Formula resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            formula=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.name = None
        self.formula = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFormulas, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.formula["location"] = kwargs[key]
                elif key == "description":
                    self.formula["description"] = kwargs[key]
                elif key == "author":
                    self.formula["author"] = kwargs[key]
                elif key == "os_type":
                    self.formula["os_type"] = kwargs[key]
                elif key == "formula_content":
                    ev = kwargs[key]
                    if 'virtual_machine_creation_source' in ev:
                        if ev['virtual_machine_creation_source'] == 'from_custom_image':
                            ev['virtual_machine_creation_source'] = 'FromCustomImage'
                        elif ev['virtual_machine_creation_source'] == 'from_gallery_image':
                            ev['virtual_machine_creation_source'] = 'FromGalleryImage'
                    self.formula["formula_content"] = ev
                elif key == "vm":
                    self.formula["vm"] = kwargs[key]
                elif key == "unique_identifier":
                    self.formula["unique_identifier"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_formula()

        if not old_response:
            self.log("Formula instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Formula instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', {
                       })):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Formula instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_formula()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Formula instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_formula()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_formula():
                time.sleep(20)
        else:
            self.log("Formula instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_formula(self):
        '''
        Creates or updates Formula with the specified configuration.

        :return: deserialized Formula instance state dictionary
        '''
        self.log("Creating / Updating the Formula instance {0}".format(self.name))

        try:
            response = self.mgmt_client.formulas.create_or_update(resource_group_name=self.resource_group,
                                                                  lab_name=self.name,
                                                                  name=self.name,
                                                                  formula=self.formula)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Formula instance.')
            self.fail("Error creating the Formula instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_formula(self):
        '''
        Deletes specified Formula instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Formula instance {0}".format(self.name))
        try:
            response = self.mgmt_client.formulas.delete(resource_group_name=self.resource_group,
                                                        lab_name=self.name,
                                                        name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Formula instance.')
            self.fail("Error deleting the Formula instance: {0}".format(str(e)))

        return True

    def get_formula(self):
        '''
        Gets the properties of the specified Formula.

        :return: deserialized Formula instance state dictionary
        '''
        self.log("Checking if the Formula instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.formulas.get(resource_group_name=self.resource_group,
                                                     lab_name=self.name,
                                                     name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Formula instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Formula instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def main():
    """Main execution"""
    AzureRMFormulas()


if __name__ == '__main__':
    main()
