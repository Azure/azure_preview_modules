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
module: azure_rm_devtestlabsdisk
version_added: "2.8"
short_description: Manage Disk instance.
description:
    - Create, update and delete instance of Disk.

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
            - The name of the user profile.
        required: True
    name:
        description:
            - The name of the I(disk).
        required: True
    disk:
        description:
            - A Disk.
        required: True
        suboptions:
            location:
                description:
                    - The location of the resource.
            disk_type:
                description:
                    - The storage type for the disk (i.e. C(standard), C(premium)).
                choices:
                    - 'standard'
                    - 'premium'
            disk_size_gi_b:
                description:
                    - The size of the disk in GibiBytes.
            leased_by_lab_vm_id:
                description:
                    - The resource ID of the VM to which this disk is leased.
            disk_blob_name:
                description:
                    - When backed by a blob, the name of the VHD blob without extension.
            disk_uri:
                description:
                    - When backed by a blob, the URI of underlying blob.
            host_caching:
                description:
                    - The host caching policy of the disk (i.e. None, ReadOnly, ReadWrite).
            managed_disk_id:
                description:
                    - When backed by managed disk, this is the ID of the compute disk resource.
            unique_identifier:
                description:
                    - The unique immutable identifier of a resource (Guid).
    state:
      description:
        - Assert the state of the Disk.
        - Use 'present' to create or update an Disk and 'absent' to delete it.
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
  - name: Create (or update) Disk
    azure_rm_devtestlabsdisk:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
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


class AzureRMDisks(AzureRMModuleBase):
    """Configuration class for an Azure RM Disk resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            disk=dict(
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
        self.lab_name = None
        self.name = None
        self.name = None
        self.disk = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDisks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.disk["location"] = kwargs[key]
                elif key == "disk_type":
                    self.disk["disk_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "disk_size_gi_b":
                    self.disk["disk_size_gi_b"] = kwargs[key]
                elif key == "leased_by_lab_vm_id":
                    self.disk["leased_by_lab_vm_id"] = kwargs[key]
                elif key == "disk_blob_name":
                    self.disk["disk_blob_name"] = kwargs[key]
                elif key == "disk_uri":
                    self.disk["disk_uri"] = kwargs[key]
                elif key == "host_caching":
                    self.disk["host_caching"] = kwargs[key]
                elif key == "managed_disk_id":
                    self.disk["managed_disk_id"] = kwargs[key]
                elif key == "unique_identifier":
                    self.disk["unique_identifier"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_disk()

        if not old_response:
            self.log("Disk instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Disk instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', {
                       })):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Disk instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_disk()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Disk instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_disk()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_disk():
                time.sleep(20)
        else:
            self.log("Disk instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_disk(self):
        '''
        Creates or updates Disk with the specified configuration.

        :return: deserialized Disk instance state dictionary
        '''
        self.log("Creating / Updating the Disk instance {0}".format(self.name))

        try:
            response = self.mgmt_client.disks.create_or_update(resource_group_name=self.resource_group,
                                                               lab_name=self.lab_name,
                                                               user_name=self.name,
                                                               name=self.name,
                                                               disk=self.disk)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Disk instance.')
            self.fail("Error creating the Disk instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_disk(self):
        '''
        Deletes specified Disk instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Disk instance {0}".format(self.name))
        try:
            response = self.mgmt_client.disks.delete(resource_group_name=self.resource_group,
                                                     lab_name=self.lab_name,
                                                     user_name=self.name,
                                                     name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Disk instance.')
            self.fail("Error deleting the Disk instance: {0}".format(str(e)))

        return True

    def get_disk(self):
        '''
        Gets the properties of the specified Disk.

        :return: deserialized Disk instance state dictionary
        '''
        self.log("Checking if the Disk instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.disks.get(resource_group_name=self.resource_group,
                                                  lab_name=self.lab_name,
                                                  user_name=self.name,
                                                  name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Disk instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Disk instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMDisks()


if __name__ == '__main__':
    main()
