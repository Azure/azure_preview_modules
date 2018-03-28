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
module: azure_rm_resource
version_added: "2.6"
short_description: Create any Azure resource.
description:
  - Create any Azure resource using Azure REST API.

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
  method:
    description:
      - The HTTP method of the request or response. It MUST be uppercase.
        choices: [ "GET", "PUT", "POST", "HEAD", "PATCH", "DELETE", "MERGE" ]
        default: "GET"
  provider:
    description:
      - The HTTP method of the request or response. It MUST be uppercase.
        choices: [ "GET", "PUT", "POST", "HEAD", "PATCH", "DELETE", "MERGE" ]
        default: "GET"
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
  - name: Update scaleset info using azure_rm_resource
    azure_rm_resource:
      resource_group: "{{ resource_group }}"
      provider: compute
      resource_type: virtualmachinescalesets
      resource_name: "{{ scaleset_name }}"
      api_version: "2017-12-01"
      body: "{{ body }}"
'''

RETURN = '''
response:
    description: Response specific to resource type.
    returned: always
    type: dict
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure import AzureConfiguration
    from msrest.service_client import ServiceClient
    import json

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMResource(AzureRMModuleBase):
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
                type='str',
                required=True
            ),
            method=dict(
                type='str',
                default='PUT',
                choices=[ "GET", "PUT", "POST", "HEAD", "PATCH", "DELETE", "MERGE" ]
            ),
            body=dict(
                type='raw'
            ),
            status_code=dict(
                type='list',
                default=[200, 202]
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
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
        self.method = None
        self.status_code = []
        self.state = None
        super(AzureRMResource, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.state == 'absent':
            self.method = 'DELETE'

        if self.url is not None:
            # check if subscription id is empty
            # check if anything else is empty
            # check if url is short?
            self.url = self.url
        else:
            # URL is None, so we should construct URL from scratch
            self.url = '/subscriptions/' + self.subscription_id

            if self.resource_group is not None:
                self.url += '/resourcegroups/' + self.resource_group

            if self.provider is not None:
                self.url += '/providers/Microsoft.' + self.provider

            if self.resource_type is not None:
                self.url += '/' + self.resource_type
                if self.resource_name is not None:
                    self.url += '/' + self.resource_name
                    if self.subresource_type is not None:
                        self.url += '/' + self.subresource_type
                        if self.subresource_name is not None:
                            self.url += '/' + self.subresource_name
            
        self.results['response'] = self.query()
        self.results['changed'] = True

        return self.results

    def query(self):

        query_parameters = {}
        query_parameters['api-version'] = self.api_version

        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        response = self.mgmt_client.query(self.url, self.method, query_parameters, header_parameters, self.body, self.status_code)

        try:
            return json.loads(response.text)
        except:
            return response.text


class GenericRestClientConfiguration(AzureConfiguration):

    def __init__(self, credentials, subscription_id, base_url=None):

        if credentials is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        if subscription_id is None:
            raise ValueError("Parameter 'subscription_id' must not be None.")
        if not base_url:
            base_url = 'https://management.azure.com'

        super(GenericRestClientConfiguration, self).__init__(base_url)

        self.add_user_agent('genericrestclient/1.0')
        self.add_user_agent('Azure-SDK-For-Python')

        self.credentials = credentials
        self.subscription_id = subscription_id


class GenericRestClient(object):

    def __init__(self, credentials, subscription_id, base_url=None):
        self.config = GenericRestClientConfiguration(credentials, subscription_id, base_url)
        self._client = ServiceClient(self.config.credentials, self.config)
        self.models = None

    def query(self, url, method, query_parameters, header_parameters, body, expected_status_codes):
        # Construct and send request
        operation_config = {}

        if method=='GET':
            request = self._client.get(url, query_parameters)
        elif method=='PUT':
            request = self._client.put(url, query_parameters)
        elif method=='POST':
            request = self._client.post(url, query_parameters)
        elif method=='HEAD':
            request = self._client.head(url, query_parameters)
        elif method=='PATCH':
            request = self._client.patch(url, query_parameters)
        elif method=='DELETE':
            request = self._client.delete(url, query_parameters)
        elif method=='MERGE':
            request = self._client.merge(url, query_parameters)
        response = self._client.send(request, header_parameters, body, **operation_config)

        if response.status_code not in expected_status_codes:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        return response
        

def main():
    AzureRMResource()
if __name__ == '__main__':
    main()
