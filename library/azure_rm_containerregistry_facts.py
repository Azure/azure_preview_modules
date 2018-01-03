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
module: azure_rm_containerregistry_facts
version_added: "2.5"
short_description: Get Registries facts.
description:
    - Get facts of Registries.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        required: True
    registry_name:
        description:
            - The name of the container registry.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Registries
    azure_rm_containerregistry_facts:
      resource_group: resource_group_name
      registry_name: registry_name

  - name: List instances of Registries
    azure_rm_containerregistry_facts:
      resource_group: resource_group_name
      registry_name: registry_name

  - name: List instances of Registries
    azure_rm_containerregistry_facts:
      resource_group: resource_group_name
      registry_name: registry_name

  - name: List instances of Registries
    azure_rm_containerregistry_facts:
      resource_group: resource_group_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerregistry import ContainerRegistryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRegistriesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registry_name=dict(
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
        self.registry_name = None
        super(AzureRMRegistriesFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.registry_name is not None):
            self.results['ansible_facts']['get'] = self.get()
        elif (self.resource_group is not None and
              self.registry_name is not None):
            self.results['ansible_facts']['list_credentials'] = self.list_credentials()
        elif (self.resource_group is not None and
              self.registry_name is not None):
            self.results['ansible_facts']['list_usages'] = self.list_usages()
        elif (self.resource_group is not None):
            self.results['ansible_facts']['list_by_resource_group'] = self.list_by_resource_group()
        return self.results

    def get(self):
        '''
        Gets facts of the specified Registries.

        :return: deserialized Registriesinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.registries.get(resource_group_name=self.resource_group,
                                                       registry_name=self.registry_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registries.')

        if response is not None:
            results = response.as_dict()

        return results

    def list_credentials(self):
        '''
        Gets facts of the specified Registries.

        :return: deserialized Registriesinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.registries.list_credentials(resource_group_name=self.resource_group,
                                                                    registry_name=self.registry_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registries.')

        if response is not None:
            results = []
            for item in response:
                results.append(item.as_dict())

        return results

    def list_usages(self):
        '''
        Gets facts of the specified Registries.

        :return: deserialized Registriesinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.registries.list_usages(resource_group_name=self.resource_group,
                                                               registry_name=self.registry_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registries.')

        if response is not None:
            results = []
            for item in response:
                results.append(item.as_dict())

        return results

    def list_by_resource_group(self):
        '''
        Gets facts of the specified Registries.

        :return: deserialized Registriesinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.registries.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registries.')

        if response is not None:
            results = []
            for item in response:
                results.append(item.as_dict())

        return results


def main():
    AzureRMRegistriesFacts()
if __name__ == '__main__':
    main()
