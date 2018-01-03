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
module: azure_rm_containerinstance_facts
version_added: "2.5"
short_description: Get ContainerGroups facts.
description:
    - Get facts of ContainerGroups.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    container_group_name:
        description:
            - The name of the container group.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of ContainerGroups
    azure_rm_containerinstance_facts:
      resource_group: resource_group_name
      container_group_name: container_group_name

  - name: List instances of ContainerGroups
    azure_rm_containerinstance_facts:
      resource_group: resource_group_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerinstance import ContainerInstanceManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerGroupsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            container_group_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict()
        )
        self.mgmt_client = None
        self.resource_group = None
        self.container_group_name = None
        super(AzureRMContainerGroupsFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ContainerInstanceManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.container_group_name is not None):
            self.results['ansible_facts']['get'] = self.get()
        elif (self.resource_group is not None):
            self.results['ansible_facts']['list_by_resource_group'] = self.list_by_resource_group()
        return self.results

    def get(self):
        '''
        Gets facts of the specified ContainerGroups.

        :return: deserialized ContainerGroupsinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.container_groups.get(resource_group_name=self.resource_group,
                                                             container_group_name=self.container_group_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ContainerGroups.')

        if response is not None:
            results = response.as_dict()

        return results

    def list_by_resource_group(self):
        '''
        Gets facts of the specified ContainerGroups.

        :return: deserialized ContainerGroupsinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.container_groups.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ContainerGroups.')

        if response is not None:
            results = []
            for item in response:
                results.append(item.as_dict())

        return results


def main():
    AzureRMContainerGroupsFacts()
if __name__ == '__main__':
    main()