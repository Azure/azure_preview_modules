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
module: azure_rm_resource_facts
version_added: "2.5"
short_description: Call Azure RM REST API.
description:
  - Call Azure RM REST API.

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

extends_documentation_fragment:
  - azure

author:
  - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of MySQL Database
    azure_rm_mysqldatabase_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name

  - name: List instances of MySQL Database
    azure_rm_mysqldatabase_facts:
      resource_group: resource_group_name
      server_name: server_name
'''

RETURN = '''
xxxxxx:
    description: A list of dict results where the key is the name of the MySQL Database and the values are the facts for that MySQL Database.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.serialization import Model
    from msrestazure import AzureConfiguration
    from msrest.service_client import ServiceClient
    from msrest.pipeline import ClientRawResponse
    import json

except ImportError:
    # This is handled in azure_rm_common
    pass

class GenericRestClientConfiguration(AzureConfiguration):
    """Configuration for SqlManagementClient
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The subscription ID that identifies an Azure
     subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

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
    """The Azure SQL Database management API provides a RESTful set of web services that interact with Azure SQL Database services to manage your databases. The API enables you to create, retrieve, update, and delete databases.

    :ivar config: Configuration for client.
    :vartype config: SqlManagementClientConfiguration
    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The subscription ID that identifies an Azure
     subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        self.config = GenericRestClientConfiguration(credentials, subscription_id, base_url)
        self._client = ServiceClient(self.config.credentials, self.config)
        self.models = None

    def query(self, url, method, query_parameters, header_parameters, body, expected_status_codes):
        # Construct and send request
        operation_config = {}

        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, body, **operation_config)

        if response.status_code not in expected_status_codes:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        return response
        

class AzureRMGenericRest(AzureRMModuleBase):
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
            body=dict(
                type='raw'
            ),
            status_code=dict(
                type='list',
                default=[200]
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict()
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
        super(AzureRMGenericRest, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

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

        return self.results

    def query(self):

        query_parameters = {}
        query_parameters['api-version'] = self.api_version

        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        #if self.config.generate_client_request_id:
        #    header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        #if custom_headers:
        #    header_parameters.update(custom_headers)
        #if self.config.accept_language is not None:
        #    header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        response = self.mgmt_client.query(self.url, "get", query_parameters, header_parameters, self.body, self.status_code)
        return json.loads(response.text)


def main():
    AzureRMGenericRest()
if __name__ == '__main__':
    main()
