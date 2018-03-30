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
module: azure_rm_resource_facts
version_added: "2.6"
short_description: Generic facts of Azure resources.
description:
  - Obtain facts of any resource using Azure REST API.

options:
  url:
    description:
      - Azure RM Resource URL.
  provider:
    description:
      - Provider type, should be specified in no URL is given
  resource_group:
    description:
      - Resource group to be used, should be specified if needed and URL is not specified
  resource_type:
    description:
      - Resource type, should be valid for specified provider
  resource_name:
    description:
      - Resource name, should be specified if needed and URL is not specified
  subresource_type:
    description:
      - Sub-resource type, should be specified if needed and not specified via URL
  subresource_name:
    description:
      - Resource name, should be specified if needed and not specified via URL
  body:
    description:
      - The body of the http request/response to the web service.

  status_code:
    description:
      - A valid, numeric, HTTP status code that signifies success of the
        request. Can also be comma separated list of status codes.
    default: 200
  state:
    description:
      - Assert the state of the resource. Use C(present) to create or update resource or C(absent) to delete resource.
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
  - name: Get scaleset info
    azure_rm_resource_facts:
      resource_group: "{{ resource_group }}"
      provider: compute
      resource_type: virtualmachinescalesets
      resource_name: "{{ scaleset_name }}"
      api_version: "2017-12-01"
'''

RETURN = '''
response:
    description: Response specific to resource type.
    returned: always
    type: dict
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.azure_rm_common_rest import GenericRestClient
from msrestazure.tools import resource_id, is_valid_resource_id

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure import AzureConfiguration
    from msrest.service_client import ServiceClient
    import json

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMResourceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            url=dict(
                type='str',
                required=False
            ),
            provider=dict(
                type='str',
                required=False
            ),
            resource_group=dict(
                type='str',
                required=False
            ),
            resource_type=dict(
                type='str',
                required=False
            ),
            resource_name=dict(
                type='str',
                required=False
            ),
            subresource_type=dict(
                type='str',
                required=False
            ),
            subresource_name=dict(
                type='str',
                required=False
            ),
            api_version=dict(
                type='str'
            ),
            status_code=dict(
                type='list',
                default=[200]
            )
        )
        # store the results of the module operation
        self.results = dict(
            response=None
        )
        self.mgmt_client = None
        self.url = None
        self.api_version = None
        self.provider = None
        self.resource_group = None
        self.resource_type = None
        self.resource_name = None
        self.subresource_type = None
        self.subresource_name = None
        self.status_code = []
        super(AzureRMResourceFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.url is None:
            self.url = resource_id(subscription_id=self.subscription_id,
                                   resource_group=self.resource_group,
                                   namespace="microsoft." + self.provider,
                                   type=self.resource_type,
                                   name=self.resource_name,
                                   child_type_0=self.subresource_type,
                                   child_name_0=self.subresource_name)

        self.results['response'] = self.query()

        return self.results

    def query(self):

        query_parameters = {}
        query_parameters['api-version'] = self.api_version

        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        response = self.mgmt_client.query(self.url, "GET", query_parameters, header_parameters, None, self.status_code)
        return json.loads(response.text)


def main():
    AzureRMResourceFacts()
if __name__ == '__main__':
    main()
