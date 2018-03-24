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
module: azure_rm_mysqldatabase_facts
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
        choices: [ "advisor",
                   "analysisservices",
                   "apimanagement",
                   "insights",
                   "authorization",
                   "automation",
                   "commerce",
                   "fabric.admin",
                   "infrastructureinsights.admin",
                   "azurestack",
                   "batch",
                   "batchai",
                   "billing",
                   "cdn",
                   "cognitiveservices",
                   "resources",
                   "compute",
                   "containerservice",
                   "consumption",
                   "containerinstance",
                   "containerregistry",
                   "documentdb",
                   "customerinsights",
                   "databricks",
                   "datacatalog",
                   "datafactory",
                   "datalakeanalytics",
                   "datalakestore",
                   "datamigration",
                   "devices",
                   "devtestlab",
                   "network",
                   "aad",
                   "eventgrid",
                   "eventhub",
                   "hanaonazure",
                   "hdinsight",
                   "keyvault",
                   "locationbasedservices",
                   "logic",
                   "machinelearning",
                   "machinelearningcompute",
                   "machinelearningexperimentation",
                   "marketplaceordering",
                   "media",
                   "migrate",
                   "mobileengagement",
                   "insights",
                   "managedidentity",
                   "dbformysql",
                   "compute",
                   "notificationhubs",
                   "operationalinsights",
                   "operationsmanagement",
                   "policyinsights",
                   "dbforpostgresql",
                   "powerbidedicated",
                   "powerbi",
                   "recoveryservices",
                   "cache",
                   "relay",
                   "capacity",
                   "resourcehealth",
                   "features",
                   "solutions",
                   "scheduler",
                   "search",
                   "servermanagement",
                   "servicebus",
                   "servicefabric",
                   "sql",
                   "storage",
                   "importexport",
                   "storsimple",
                   "streamanalytics",
                   "timeseriesinsights",
                   "visualstudio",
                   "certificateregistration",
                   "domainregistration",
                   "web",
                   "web.admin"
                   ]
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
                required=False,
                choices=[ "advisor",
                   "analysisservices",
                   "apimanagement",
                   "insights",
                   "authorization",
                   "automation",
                   "commerce",
                   "fabric.admin",
                   "infrastructureinsights.admin",
                   "azurestack",
                   "batch",
                   "batchai",
                   "billing",
                   "cdn",
                   "cognitiveservices",
                   "resources",
                   "compute",
                   "containerservice",
                   "consumption",
                   "containerinstance",
                   "containerregistry",
                   "documentdb",
                   "customerinsights",
                   "databricks",
                   "datacatalog",
                   "datafactory",
                   "datalakeanalytics",
                   "datalakestore",
                   "datamigration",
                   "devices",
                   "devtestlab",
                   "network",
                   "aad",
                   "eventgrid",
                   "eventhub",
                   "hanaonazure",
                   "hdinsight",
                   "keyvault",
                   "locationbasedservices",
                   "logic",
                   "machinelearning",
                   "machinelearningcompute",
                   "machinelearningexperimentation",
                   "marketplaceordering",
                   "media",
                   "migrate",
                   "mobileengagement",
                   "insights",
                   "managedidentity",
                   "dbformysql",
                   "compute",
                   "notificationhubs",
                   "operationalinsights",
                   "operationsmanagement",
                   "policyinsights",
                   "dbforpostgresql",
                   "powerbidedicated",
                   "powerbi",
                   "recoveryservices",
                   "cache",
                   "relay",
                   "capacity",
                   "resourcehealth",
                   "features",
                   "solutions",
                   "scheduler",
                   "search",
                   "servermanagement",
                   "servicebus",
                   "servicefabric",
                   "sql",
                   "storage",
                   "importexport",
                   "storsimple",
                   "streamanalytics",
                   "timeseriesinsights",
                   "visualstudio",
                   "certificateregistration",
                   "domainregistration",
                   "web",
                   "web.admin"
                   ]
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
            method=dict(
                type='str',
                default='GET',
                choices=[ "GET", "PUT", "POST", "HEAD", "PATCH", "DELETE", "MERGE" ]
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
        self.method = None
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
            
            if self.api_version is None:
                self.api_version = self.get_latest_version(self.provider, self.resource_type)

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

        response = self.mgmt_client.query(self.url, self.method, query_parameters, header_parameters, self.body, self.status_code)
        return json.loads(response.text)

    def get_latest_version(self, provider, operations):
        if provider =='advisor':
            if operations =='generaterecommendations':
                return '2017-04-19'
            elif operations =='recommendations':
                return '2017-04-19'
            elif operations =='suppressions':
                return '2017-04-19'
            elif operations =='configurations':
                return '2017-04-19'
        elif provider =='analysisservices':
            if operations =='servers':
                return '2017-08-01-beta'
            elif operations =='skus':
                return '2017-08-01-beta'
            elif operations =='locations':
                return '2017-08-01-beta'
        elif provider =='apimanagement':
            if operations =='service':
                return '2018-01-01'
            elif operations =='checknameavailability':
                return '2018-01-01'
        elif provider =='insights':
            if operations =='components':
                return '2015-05-01'
            elif operations =='webtests':
                return '2015-05-01'
        elif provider =='authorization':
            if operations =='classicadministrators':
                return '2015-07-01'
            elif operations =='permissions':
                return '2018-01-01-preview'
            elif operations =='roleassignments':
                return '2018-01-01-preview'
            elif operations =='policyassignments':
                return '2017-06-01-preview'
            elif operations =='policyassignments':
                return '2016-04-01'
            elif operations =='policydefinitions':
                return '2016-04-01'
            elif operations =='policysetdefinitions':
                return '2017-06-01-preview'
            elif operations =='locks':
                return '2016-09-01'
            elif operations =='policydefinitions':
                return '2016-12-01'
        elif provider =='automation':
            if operations =='automationaccounts':
                return '2017-05-15-preview'
        elif provider =='commerce':
            if operations =='subscriberusageaggregates':
                return '2015-06-01-preview'
            elif operations =='usageaggregates':
                return '2015-06-01-preview'
            elif operations =='ratecard':
                return '2015-06-01-preview'
        elif provider =='fabric.admin':
            if operations =='fabriclocations':
                return '2016-05-01'
        elif provider =='infrastructureinsights.admin':
            if operations =='regionhealths':
                return '2016-05-01'
        elif provider =='azurestack':
            if operations =='registrations':
                return '2017-06-01'
        elif provider =='batch':
            if operations =='batchaccounts':
                return '2017-09-01'
            elif operations =='locations':
                return '2017-09-01'
        elif provider =='batchai':
            if operations =='clusters':
                return '2018-03-01'
            elif operations =='jobs':
                return '2018-03-01'
            elif operations =='fileservers':
                return '2018-03-01'
            elif operations =='locations':
                return '2018-03-01'
        elif provider =='billing':
            if operations =='invoices':
                return '2018-03-01-preview'
            elif operations =='billingperiods':
                return '2018-03-31'
        elif provider =='cdn':
            if operations =='profiles':
                return '2017-10-12'
            elif operations =='checkresourceusage':
                return '2017-10-12'
            elif operations =='validateprobe':
                return '2017-10-12'
            elif operations =='checknameavailability':
                return '2017-10-12'
        elif provider =='cognitiveservices':
            if operations =='accounts':
                return '2017-04-18'
            elif operations =='locations':
                return '2017-04-18'
        elif provider =='resources':
            if operations =='deployments':
                return '2018-02-01'
            elif operations =='links':
                return '2016-09-01'
        elif provider =='compute':
            if operations =='availabilitysets':
                return '2017-12-01'
            elif operations =='locations':
                return '2017-12-01'
            elif operations =='virtualmachines':
                return '2017-12-01'
            elif operations =='images':
                return '2017-12-01'
            elif operations =='virtualmachinescalesets':
                return '2017-12-01'
            elif operations =='disks':
                return '2018-04-01'
            elif operations =='snapshots':
                return '2018-04-01'
            elif operations =='skus':
                return '2017-09-01'
        elif provider =='containerservice':
            if operations =='containerservices':
                return '2017-07-01'
            elif operations =='managedclusters':
                return '2017-08-31'
            elif operations =='locations':
                return '2017-09-30'
        elif provider =='consumption':
            if operations =='budgets':
                return '2018-03-31'
            elif operations =='usagedetails':
                return '2018-03-31'
            elif operations =='marketplaces':
                return '2018-03-31'
            elif operations =='pricesheets':
                return '2018-03-31'
            elif operations =='reservationrecommendations':
                return '2018-03-31'
        elif provider =='containerinstance':
            if operations =='containergroups':
                return '2018-02-01-preview'
            elif operations =='locations':
                return '2018-02-01-preview'
        elif provider =='containerregistry':
            if operations =='checknameavailability':
                return '2017-10-01'
            elif operations =='registries':
                return '2017-10-01'
        elif provider =='documentdb':
            if operations =='databaseaccounts':
                return '2015-04-08'
        elif provider =='customerinsights':
            if operations =='hubs':
                return '2017-04-26'
        elif provider =='databricks':
            if operations =='workspaces':
                return '2018-04-01'
        elif provider =='datacatalog':
            if operations =='catalogs':
                return '2016-03-30'
        elif provider =='datafactory':
            if operations =='factories':
                return '2017-09-01-preview'
        elif provider =='datalakeanalytics':
            if operations =='accounts':
                return '2016-11-01'
            elif operations =='locations':
                return '2016-11-01'
        elif provider =='datalakestore':
            if operations =='accounts':
                return '2016-11-01'
            elif operations =='locations':
                return '2016-11-01'
        elif provider =='datamigration':
            if operations =='skus':
                return '2018-03-15-preview'
            elif operations =='services':
                return '2018-03-15-preview'
            elif operations =='locations':
                return '2018-03-15-preview'
        elif provider =='devices':
            if operations =='provisioningservices':
                return '2018-01-22'
            elif operations =='checkprovisioningservicenameavailability':
                return '2018-01-22'
            elif operations =='iothubs':
                return '2018-01-22'
            elif operations =='checknameavailability':
                return '2018-01-22'
        elif provider =='devtestlab':
            if operations =='labs':
                return '2016-05-15'
            elif operations =='locations':
                return '2016-05-15'
            elif operations =='schedules':
                return '2016-05-15'
        elif provider =='network':
            if operations =='dnszones':
                return '2018-03-01-preview'
            elif operations =='dnszones':
                return '2018-03-01-preview'
            elif operations =='applicationgateways':
                return '2018-01-01'
            elif operations =='expressroutecircuits':
                return '2018-01-01'
            elif operations =='expressrouteserviceproviders':
                return '2018-01-01'
            elif operations =='loadbalancers':
                return '2018-01-01'
            elif operations =='localnetworkgateways':
                return '2018-01-01'
            elif operations =='networkinterfaces':
                return '2018-01-01'
            elif operations =='routetables':
                return '2018-01-01'
            elif operations =='networksecuritygroups':
                return '2018-01-01'
            elif operations =='publicipaddresses':
                return '2018-01-01'
            elif operations =='virtualnetworks':
                return '2015-06-15'
            elif operations =='locations':
                return '2018-01-01'
            elif operations =='connections':
                return '2018-01-01'
            elif operations =='virtualnetworkgateways':
                return '2015-05-01-preview'
            elif operations =='virtualnetworkgateways':
                return '2018-01-01'
            elif operations =='virtualnetworks':
                return '2018-01-01'
            elif operations =='networkwatchers':
                return '2018-01-01'
            elif operations =='routefilters':
                return '2018-01-01'
            elif operations =='bgpservicecommunities':
                return '2018-01-01'
            elif operations =='applicationgatewayavailablewafrulesets':
                return '2018-01-01'
            elif operations =='applicationgatewayavailablessloptions':
                return '2018-01-01'
            elif operations =='applicationsecuritygroups':
                return '2018-01-01'
            elif operations =='trafficmanagerprofiles':
                return '2017-09-01-preview'
            elif operations =='trafficmanagerusermetricskeys':
                return '2017-09-01-preview'
        elif provider =='aad':
            if operations =='domainservices':
                return '2017-06-01'
        elif provider =='eventgrid':
            if operations =='eventsubscriptions':
                return '2018-01-01'
            elif operations =='topictypes':
                return '2018-01-01'
            elif operations =='locations':
                return '2018-01-01'
            elif operations =='topics':
                return '2018-01-01'
        elif provider =='eventhub':
            if operations =='clusters':
                return '2018-01-01-preview'
            elif operations =='checknameavailability':
                return '2017-04-01'
            elif operations =='checknamespaceavailability':
                return '2014-09-01'
            elif operations =='namespaces':
                return '2017-04-01'
            elif operations =='sku':
                return '2017-04-01'
        elif provider =='hanaonazure':
            if operations =='hanainstances':
                return '2017-11-03-preview'
        elif provider =='hdinsight':
            if operations =='clusters':
                return '2015-03-01-preview'
            elif operations =='locations':
                return '2015-03-01-preview'
        elif provider =='keyvault':
            if operations =='vaults':
                return '2016-10-01'
            elif operations =='deletedvaults':
                return '2016-10-01'
            elif operations =='locations':
                return '2016-10-01'
            elif operations =='checknameavailability':
                return '2016-10-01'
        elif provider =='locationbasedservices':
            if operations =='accounts':
                return '2017-01-01-preview'
        elif provider =='logic':
            if operations =='workflows':
                return '2016-06-01'
            elif operations =='integrationaccounts':
                return '2016-06-01'
            elif operations =='locations':
                return '2016-06-01'
        elif provider =='machinelearning':
            if operations =='skus':
                return '2016-05-01-preview'
            elif operations =='commitmentplans':
                return '2016-05-01-preview'
            elif operations =='webservices':
                return '2017-01-01'
            elif operations =='workspaces':
                return '2016-04-01'
        elif provider =='machinelearningcompute':
            if operations =='operationalizationclusters':
                return '2017-08-01-preview'
        elif provider =='machinelearningexperimentation':
            if operations =='accounts':
                return '2017-05-01-preview'
        elif provider =='marketplaceordering':
            if operations =='offertypes':
                return '2015-06-01'
        elif provider =='media':
            if operations =='checknameavailability':
                return '2015-10-01'
            elif operations =='mediaservices':
                return '2015-10-01'
        elif provider =='migrate':
            if operations =='projects':
                return '2018-02-02'
        elif provider =='mobileengagement':
            if operations =='appcollections':
                return '2014-12-01'
            elif operations =='appcollections':
                return '2014-12-01'
            elif operations =='supportedplatforms':
                return '2014-12-01'
            elif operations =='checkappcollectionnameavailability':
                return '2014-12-01'
        elif provider =='managedidentity':
            if operations =='userassignedidentities':
                return '2015-08-31-preview'
        elif provider =='dbformysql':
            if operations =='servers':
                return '2017-12-01-preview'
            elif operations =='performancetiers':
                return '2017-04-30-preview'
            elif operations =='locations':
                return '2017-12-01-preview'
            elif operations =='checknameavailability':
                return '2017-12-01-preview'
        elif provider =='notificationhubs':
            if operations =='checknamespaceavailability':
                return '2017-04-01'
            elif operations =='namespaces':
                return '2017-04-01'
            elif operations =='checknameavailability':
                return '2017-04-01'
        elif provider =='operationalinsights':
            if operations =='workspaces':
                return '2015-11-01-preview'
            elif operations =='linktargets':
                return '2015-03-20'
        elif provider =='operationsmanagement':
            if operations =='solutions':
                return '2015-11-01-preview'
            elif operations =='managementassociations':
                return '2015-11-01-preview'
            elif operations =='managementconfigurations':
                return '2015-11-01-preview'
        elif provider =='policyinsights':
            if operations =='policyevents':
                return '2017-12-12-preview'
            elif operations =='policystates':
                return '2017-12-12-preview'
        elif provider =='dbforpostgresql':
            if operations =='servers':
                return '2017-12-01-preview'
            elif operations =='performancetiers':
                return '2017-04-30-preview'
            elif operations =='locations':
                return '2017-12-01-preview'
            elif operations =='checknameavailability':
                return '2017-12-01-preview'
        elif provider =='powerbidedicated':
            if operations =='capacities':
                return '2017-10-01'
            elif operations =='skus':
                return '2017-10-01'
        elif provider =='powerbi':
            if operations =='workspacecollections':
                return '2016-01-29'
            elif operations =='locations':
                return '2016-01-29'
        elif provider =='recoveryservices':
            if operations =='vaults':
                return '2016-06-01'
        elif provider =='cache':
            if operations =='redis':
                return '2018-03-01'
            elif operations =='checknameavailability':
                return '2018-03-01'
        elif provider =='relay':
            if operations =='checknameavailability':
                return '2016-07-01'
            elif operations =='namespaces':
                return '2016-07-01'
            elif operations =='namespaces':
                return '2017-04-01'
            elif operations =='checknameavailability':
                return '2017-04-01'
        elif provider =='capacity':
            if operations =='catalogs':
                return '2017-11-01'
            elif operations =='appliedreservations':
                return '2017-11-01'
        elif provider =='resourcehealth':
            if operations =='availabilitystatuses':
                return '2017-07-01'
        elif provider =='features':
            if operations =='features':
                return '2015-12-01'
            elif operations =='undefined':
                return '2015-12-01'
        elif provider =='solutions':
            if operations =='appliances':
                return '2016-09-01-preview'
            elif operations =='appliancedefinitions':
                return '2016-09-01-preview'
            elif operations =='applications':
                return '2017-09-01'
            elif operations =='applicationdefinitions':
                return '2017-09-01'
        elif provider =='scheduler':
            if operations =='jobcollections':
                return '2016-03-01'
        elif provider =='search':
            if operations =='searchservices':
                return '2015-08-19'
            elif operations =='checknameavailability':
                return '2015-08-19'
        elif provider =='servermanagement':
            if operations =='gateways':
                return '2016-07-01-preview'
            elif operations =='nodes':
                return '2016-07-01-preview'
        elif provider =='servicebus':
            if operations =='checknameavailability':
                return '2017-04-01'
            elif operations =='checknamespaceavailability':
                return '2014-09-01'
            elif operations =='namespaces':
                return '2017-04-01'
            elif operations =='sku':
                return '2017-04-01'
            elif operations =='premiummessagingregions':
                return '2017-04-01'
        elif provider =='servicefabric':
            if operations =='clusters':
                return '2017-07-01-preview'
            elif operations =='locations':
                return '2017-07-01-preview'
        elif provider =='sql':
            if operations =='servers':
                return '2017-10-01-preview'
            elif operations =='locations':
                return '2017-03-01-preview'
            elif operations =='checknameavailability':
                return '2014-04-01'
        elif provider =='storage':
            if operations =='checknameavailability':
                return '2017-10-01'
            elif operations =='storageaccounts':
                return '2017-10-01'
            elif operations =='usages':
                return '2017-10-01'
            elif operations =='skus':
                return '2017-10-01'
        elif provider =='importexport':
            if operations =='jobs':
                return '2016-11-01'
        elif provider =='storsimple':
            if operations =='managers':
                return '2017-06-01'
        elif provider =='streamanalytics':
            if operations =='streamingjobs':
                return '2016-03-01'
            elif operations =='locations':
                return '2016-03-01'
        elif provider =='timeseriesinsights':
            if operations =='environments':
                return '2017-11-15'
        elif provider =='certificateregistration':
            if operations =='certificateorders':
                return '2015-08-01'
            elif operations =='validatecertificateregistrationinformation':
                return '2015-08-01'
        elif provider =='domainregistration':
            if operations =='checkdomainavailability':
                return '2015-08-01'
            elif operations =='domains':
                return '2015-08-01'
            elif operations =='generatessorequest':
                return '2015-08-01'
            elif operations =='listdomainrecommendations':
                return '2015-08-01'
            elif operations =='topleveldomains':
                return '2015-08-01'
            elif operations =='validatedomainregistrationinformation':
                return '2015-08-01'
        elif provider =='web':
            if operations =='locations':
                return '2015-08-01-preview'
            elif operations =='connections':
                return '2015-08-01-preview'
            elif operations =='certificates':
                return '2016-03-01'
            elif operations =='csrs':
                return '2015-08-01'
            elif operations =='classicmobileservices':
                return '2015-08-01'
            elif operations =='publishingcredentials':
                return '2015-08-01'
            elif operations =='georegions':
                return '2016-03-01'
            elif operations =='serverfarms':
                return '2016-09-01'
            elif operations =='sites':
                return '2016-08-01'
            elif operations =='hostingenvironments':
                return '2016-09-01'
            elif operations =='managedhostingenvironments':
                return '2015-08-01'
            elif operations =='premieraddonoffers':
                return '2016-03-01'
            elif operations =='ishostingenvironmentnameavailable':
                return '2015-08-01'
            elif operations =='checknameavailability':
                return '2016-03-01'
            elif operations =='recommendations':
                return '2016-03-01'
            elif operations =='deletedsites':
                return '2016-03-01'
            elif operations =='availablestacks':
                return '2016-03-01'
            elif operations =='resourcehealthmetadata':
                return '2016-03-01'
            elif operations =='deploymentlocations':
                return '2016-03-01'
            elif operations =='listsitesassignedtohostname':
                return '2016-03-01'
            elif operations =='skus':
                return '2016-03-01'
            elif operations =='verifyhostingenvironmentvnet':
                return '2016-03-01'
            elif operations =='validate':
                return '2016-03-01'
        elif provider =='web.admin':
            if operations =='environments':
                return '2015-08-01'
        return None;

def main():
    AzureRMGenericRest()
if __name__ == '__main__':
    main()
