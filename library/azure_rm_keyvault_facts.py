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
module: azure_rm_keyvault_facts
version_added: "2.5"
short_description: Get Vault facts.
description:
    - Get facts of Vault.

options:
    resource_group:
        description:
            - The name of the Resource Group to which the vault belongs.
        required: True
    vault_name:
        description:
            - The name of the vault.
    top:
        description:
            - Maximum number of results to return.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Vault
    azure_rm_keyvault_facts:
      resource_group: resource_group_name
      vault_name: vault_name

  - name: List instances of Vault
    azure_rm_keyvault_facts:
      resource_group: resource_group_name
      top: top
'''

RETURN = '''
vaults:
    description: A list of dict results where the key is the name of the Vault and the values are the facts for that Vault.
    returned: always
    type: complex
    contains:
        vault_name:
            description: The key is the name of the server that the values relate to.
            type: complex
            contains:
                id:
                    description:
                        - The Azure Resource Manager resource ID for the key vault.
                    returned: always
                    type: str
                    sample: id
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVaultsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vault_name=dict(
                type='str'
            ),
            top=dict(
                type='int'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict()
        )
        self.mgmt_client = None
        self.resource_group = None
        self.vault_name = None
        self.top = None
        super(AzureRMVaultsFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(KeyVaultManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.vault_name is not None):
            self.results['vaults'] = self.get()
        elif (self.resource_group is not None):
            self.results['vaults'] = self.list_by_resource_group()
        return self.results

    def get(self):
        '''
        Gets facts of the specified Vault.

        :return: deserialized Vaultinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.mgmt_client.vaults.get(resource_group_name=self.resource_group,
                                                   vault_name=self.vault_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Vaults.')

        if response is not None:
            results[response.name] = response.as_dict()

        return results

    def list_by_resource_group(self):
        '''
        Gets facts of the specified Vault.

        :return: deserialized Vaultinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.mgmt_client.vaults.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Vaults.')

        if response is not None:
            for item in response:
                results[item.name] = item.as_dict()

        return results


def main():
    AzureRMVaultsFacts()
if __name__ == '__main__':
    main()
