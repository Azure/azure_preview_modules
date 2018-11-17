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
module: azure_rm_mariadbserver_facts
version_added: "2.8"
short_description: Get Azure Server facts.
description:
    - Get facts of Azure Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the server.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Server
    azure_rm_mariadbserver_facts:
      resource_group: resource_group_name
      name: server_name

  - name: List instances of Server
    azure_rm_mariadbserver_facts:
      resource_group: resource_group_name
'''

RETURN = '''
servers:
    description: A list of dictionaries containing facts for Server.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID
            returned: always
            type: str
            sample: /subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/testrg/providers/Microsoft.DBforMariaDB/servers/mariadbtestsvc4
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: mariadbtestsvc4
        location:
            description:
                - The location the resource resides in.
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Application-specific metadata in the form of key-value pairs.
            returned: always
            type: complex
            sample: "{\n  'ElasticServer': '1'\n}"
        sku:
            description:
                - The SKU (pricing tier) of the server.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - The name of the sku, typically, tier + family + cores, e.g. B_Gen4_1, GP_Gen5_8.
                    returned: always
                    type: str
                    sample: GP_Gen5_2
                tier:
                    description:
                        - "The tier of the particular SKU, e.g. Basic. Possible values include: 'Basic', 'GeneralPurpose', 'MemoryOptimized'"
                    returned: always
                    type: str
                    sample: GeneralPurpose
                capacity:
                    description:
                        - "The scale up/out capacity, representing server's compute units."
                    returned: always
                    type: int
                    sample: 2
                family:
                    description:
                        - The family of hardware.
                    returned: always
                    type: str
                    sample: Gen5
        version:
            description:
                - "Server version. Possible values include: '5.6', '5.7'"
            returned: always
            type: str
            sample: 5.7
        user_visible_state:
            description:
                - "A state of a server that is visible to user. Possible values include: 'Ready', 'Dropping', 'Disabled'"
            returned: always
            type: str
            sample: user_visible_state
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of a server.
            returned: always
            type: str
            sample: fully_qualified_domain_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.rdbms.mariadb import MariaDBManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.tags = None
        super(AzureRMServersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MariaDBManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['servers'] = self.get()
        else:
            self.results['servers'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.servers.get(resource_group_name=self.resource_group,
                                                    server_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Servers.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.servers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Servers.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None),
                'capacity': d.get('sku', {}).get('capacity', None),
                'family': d.get('sku', {}).get('family', None)
            },
            'version': d.get('version', None),
            'user_visible_state': d.get('user_visible_state', None),
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None)
        }
        return d


def main():
    AzureRMServersFacts()


if __name__ == '__main__':
    main()
