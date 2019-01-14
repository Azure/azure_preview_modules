#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_devtestlabslab
version_added: "2.8"
short_description: Manage Azure DevTest Lab instance.
description:
    - Create, update and delete instance of Azure DevTest Lab.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the lab.
        required: True
    location:
        description:
            - The location of the resource.
    lab_storage_type:
        description:
            - Type of storage used by the lab. It can be either C(premium) or C(standard). Default is C(premium).
        choices:
            - 'standard'
            - 'premium'
        default: premium
    premium_data_disks:
        description:
            - "Allow creation of C(premium) data disks."
        type: bool
    state:
      description:
        - Assert the state of the DevTest Lab.
        - Use 'present' to create or update an DevTest Lab and 'absent' to delete it.
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
  - name: Create (or update) DevTest Lab
    azure_rm_devtestlabslab:
      resource_group: testrg
      name: mylab
      lab_storage_type: standard
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


class AzureRMDevTestLab(AzureRMModuleBase):
    """Configuration class for an Azure RM DevTest Lab resource"""

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
            location=dict(
                type='str'
            ),
            lab_storage_type=dict(
                type='str',
                choices=['standard',
                         'premium'],
                default='premium'
            ),
            premium_data_disks=dict(
                type='bool'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.lab = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDevTestLab, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.lab[key] = kwargs[key]

        dict_camelize(self.lab, ['lab_storage_type'], True)
        dict_map(self.lab, ['premium_data_disks'], {True: 'Enabled', False: 'Disabled'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_devtestlab()

        if not old_response:
            self.log("DevTest Lab instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("DevTest Lab instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.lab, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the DevTest Lab instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_devtestlab()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("DevTest Lab instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_devtestlab()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("DevTest Lab instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_devtestlab(self):
        '''
        Creates or updates DevTest Lab with the specified configuration.

        :return: deserialized DevTest Lab instance state dictionary
        '''
        self.log("Creating / Updating the DevTest Lab instance {0}".format(self.name))

        try:
            response = self.mgmt_client.labs.create_or_update(resource_group_name=self.resource_group,
                                                              name=self.name,
                                                              lab=self.lab)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the DevTest Lab instance.')
            self.fail("Error creating the DevTest Lab instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_devtestlab(self):
        '''
        Deletes specified DevTest Lab instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the DevTest Lab instance {0}".format(self.name))
        try:
            response = self.mgmt_client.labs.delete(resource_group_name=self.resource_group,
                                                    name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the DevTest Lab instance.')
            self.fail("Error deleting the DevTest Lab instance: {0}".format(str(e)))

        return True

    def get_devtestlab(self):
        '''
        Gets the properties of the specified DevTest Lab.

        :return: deserialized DevTest Lab instance state dictionary
        '''
        self.log("Checking if the DevTest Lab instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.labs.get(resource_group_name=self.resource_group,
                                                 name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("DevTest Lab instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the DevTest Lab instance.')
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def main():
    """Main execution"""
    AzureRMDevTestLab()


if __name__ == '__main__':
    main()
