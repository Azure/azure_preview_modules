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
module: azure_rm_appgwroute_facts
version_added: "2.5"
short_description: Get Route facts.
description:
    - Get facts of Route.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    route_table_name:
        description:
            - The name of the route table.
        required: True
    route_name:
        description:
            - The name of the route.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Route
    azure_rm_appgwroute_facts:
      resource_group: resource_group_name
      route_table_name: route_table_name
      route_name: route_name
'''

RETURN = '''
routes:
    description: A list of dict results where the key is the name of the Route and the values are the facts for that Route.
    returned: always
    type: complex
    contains:
        route_name:
            description: The key is the name of the server that the values relate to.
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/routeTables/testrt/routes/route1
                name:
                    description:
                        - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                    returned: always
                    type: str
                    sample: route1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRoutesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            route_table_name=dict(
                type='str',
                required=True
            ),
            route_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict()
        )
        self.mgmt_client = None
        self.resource_group = None
        self.route_table_name = None
        self.route_name = None
        super(AzureRMRoutesFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.route_table_name is not None and
                self.route_name is not None):
            self.results['routes'] = self.get()
        return self.results

    def get(self):
        '''
        Gets facts of the specified Route.

        :return: deserialized Routeinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.mgmt_client.routes.get(resource_group_name=self.resource_group,
                                                   route_table_name=self.route_table_name,
                                                   route_name=self.route_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Routes.')

        if response is not None:
            results[response.name] = response.as_dict()

        return results


def main():
    AzureRMRoutesFacts()
if __name__ == '__main__':
    main()
