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
module: azure_rm_sqlelasticpool_facts
version_added: "2.5"
short_description: Get SQL Elastic Pool facts.
description:
    - Get facts of SQL Elastic Pool.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    elastic_pool_name:
        description:
            - The name of the elastic pool to be retrieved.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of SQL Elastic Pool
    azure_rm_sqlelasticpool_facts:
      resource_group: resource_group_name
      server_name: server_name
      elastic_pool_name: elastic_pool_name

  - name: List instances of SQL Elastic Pool
    azure_rm_sqlelasticpool_facts:
      resource_group: resource_group_name
      server_name: server_name
'''

RETURN = '''
elastic_pools:
    description: A list of dict results where the key is the name of the SQL Elastic Pool and the values are the facts for that SQL Elastic Pool.
    returned: always
    type: complex
    contains:
        sqlelasticpool_name:
            description: The key is the name of the server that the values relate to.
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-2369/providers/Microsoft.Sql/servers/sqlcrudtest-
                            8069/elasticPools/sqlcrudtest-8102"
                name:
                    description:
                        - Resource name.
                    returned: always
                    type: str
                    sample: sqlcrudtest-8102
                type:
                    description:
                        - Resource type.
                    returned: always
                    type: str
                    sample: Microsoft.Sql/servers/elasticPools
                location:
                    description:
                        - Resource location.
                    returned: always
                    type: str
                    sample: Japan East
                state:
                    description:
                        - "The state of the elastic pool. Possible values include: 'Creating', 'Ready', 'Disabled'"
                    returned: always
                    type: str
                    sample: Ready
                edition:
                    description:
                        - "The edition of the elastic pool. Possible values include: 'Basic', 'Standard', 'Premium'"
                    returned: always
                    type: str
                    sample: Basic
                dtu:
                    description:
                        - The total shared DTU for the database elastic pool.
                    returned: always
                    type: int
                    sample: 50
                kind:
                    description:
                        - Kind of elastic pool.  This is metadata used for the Azure portal experience.
                    returned:
                    type: str
                    sample: kind
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMElasticPoolsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            elastic_pool_name=dict(
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
        self.server_name = None
        self.elastic_pool_name = None
        super(AzureRMElasticPoolsFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.server_name is not None and
                self.elastic_pool_name is not None):
            self.results['elastic_pools'] = self.get()
        elif (self.resource_group is not None and
              self.server_name is not None):
            self.results['elastic_pools'] = self.list_by_server()
        return self.results

    def get(self):
        '''
        Gets facts of the specified SQL Elastic Pool.

        :return: deserialized SQL Elastic Poolinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.mgmt_client.elastic_pools.get(resource_group_name=self.resource_group,
                                                          server_name=self.server_name,
                                                          elastic_pool_name=self.elastic_pool_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ElasticPools.')

        if response is not None:
            results[response.name] = response.as_dict()

        return results

    def list_by_server(self):
        '''
        Gets facts of the specified SQL Elastic Pool.

        :return: deserialized SQL Elastic Poolinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.mgmt_client.elastic_pools.list_by_server(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ElasticPools.')

        if response is not None:
            for item in response:
                results[item.name] = item.as_dict()

        return results


def main():
    AzureRMElasticPoolsFacts()
if __name__ == '__main__':
    main()
