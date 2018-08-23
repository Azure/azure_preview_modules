#!/usr/bin/python
#
# Copyright (c) 2018 Hai Cao, <t-haicao@microsoft.com>, Yunge Zhu <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: azure_rm_trafficmanagerendpoint_facts

version_added: "2.7"

short_description: Get Azure Traffic Manager endpoint facts

description:
    - Get facts for a specific Traffic Manager endpoints or all endpoints  in a Traffic Manager profile

options:
    name:
        description:
            - Limit results to a specific Traffic Manager profile.
    resource_group:
        description:
            - The resource group to search for the desired Traffic Manager profile
        required: True
    profile_name:
        description:
            - Name of Traffic Manager Profile
        required: True
    type:
        description:
            - Type of endpoint.
        choices:
            - azureEndpoints
            - externalEndpoints
            - nestedEndpoints

extends_documentation_fragment:
    - azure

author:
    - "Hai Cao <t-haicao@microsoft.com>"
    - "Yunge Zhu <yungez@microsoft.com>"
'''

EXAMPLES = '''
    - name: Get facts for one Traffic Manager profile
      azure_rm_trafficmanager_facts:
        name: Testing
        resource_group: TestRG

    - name: Get facts for all Traffic Manager profiles
      azure_rm_trafficmanager_facts:

    - name: Get facts by tags
      azure_rm_trafficmanager_facts:
        tags:
          - Environment:Test
'''

RETURN = '''
tms:
    description: List of Traffic Manager profiles.
    returned: always
    type: complex
    contains:
        resource_group:
            description:
                - Name of a resource group where the Traffic Manager profile exists.
            returned: always
            type: str
            sample: testGroup
        name:
            description:
                - Name of the Traffic Manager profile.
            returned: always
            type: str
            sample: testTm
        state:
            description:
                - The state of the Traffic Manager profile.
            type: str
            sample: present
        location:
            description:
                - Location of the Traffic Manager profile.
            type: str
            sample: global
        profile_status:
            description:
                - The status of the Traffic Manager profile.
            type: str
            sample: Enabled
        traffic_routing_method:
            description:
                - The traffic routing method of the Traffic Manager profile.
            type: str
            sample: Performance
        dns_config:
            description:
                - The DNS settings of the Traffic Manager profile.
            type: complex
            sample:
                relative_name: testTm
                fqdn: testTm.trafficmanager.net
                ttl: 60
        monitor_config:
            description:
                - The endpoint monitoring settings of the Traffic Manager profile.
            type: complex
            contains:
                protocol:
                    description:
                        - The protocol (HTTP, HTTPS or TCP) used to probe for endpoint health.
                    type: str
                    sample: HTTP
                port:
                    description:
                        - The TCP port used to probe for endpoint health.
                    type: int
                    sample: 80
                path:
                    description:
                        - The path relative to the endpoint domain name used to probe for endpoint health.
                    type: str
                    sample: /
                interval_in_seconds:
                    description:
                        - The monitor interval for endpoints in this profile.
                    type: int
                    sample: 10
                timeout_in_seconds:
                    description:
                        - The monitor timeout for endpoints in this profile.
                    type: int
                    sample: 30
                tolerated_number_of_failures:
                    description:
                        - The number of consecutive failed health check before declaring an endpoint Degraded after the next failed health check.
                    type: int
                    sample: 3
        endpoints:
            description:
                - The list of endpoints in the Traffic Manager profile.
            type: list
            element: complex
            contains:
                id:
                    description:
                        - Fully qualified resource Id for the resource.
                    type: str
                    sample: /subscriptions/XXXXXX...XXXXXXXXX/resourceGroups/tmt/providers/Microsoft.Network/trafficManagerProfiles/tmtest/externalEndpoints/e1
                name:
                    description:
                        - The name of the endpoint.
                    type: str
                    sample: e1
                type:
                    description:
                        - The type of the endpoint. Ex- Microsoft.network/TrafficManagerProfiles/ExternalEndpoints.
                    type: str
                    sample: Microsoft.Network/trafficManagerProfiles/externalEndpoints
                target_resource_id:
                    description:
                        - The Azure Resource URI of the of the endpoint.
                    type: str
                    sample: /subscriptions/XXXXXX...XXXXXXXXX/resourceGroups/vscjavaci/providers/Microsoft.ClassicCompute/domainNames/vscjavaci
                target:
                    description:
                        - The fully-qualified DNS name of the endpoint.
                    type: str
                    sample: 8.8.8.8
                endpoint_status:
                    description:
                        - The status of the endpoint.
                    type: str
                    sample: Enabled
                weight:
                    description:
                        - The weight of this endpoint when using the 'Weighted' traffic routing method.
                    type: int
                    sample: 10
                priority:
                    description:
                        - The priority of this endpoint when using the 'Priority' traffic routing method.
                    type: str
                    sample: 3
                endpoint_location:
                    description:
                        - The location of the external or nested endpoints when using the 'Performance' traffic routing method.
                    type: str
                    sample: East US
                min_child_endpoints:
                    description:
                        - The minimum number of endpoints that must be available in the child profile to make the parent profile available.
                    type: int
                    sample: 3
                geo_mapping:
                    description:
                        - The list of countries/regions mapped to this endpoint when using the 'Geographic' traffic routing method.
                    type: list
                    sample: [
                        "GEO-NA",
                        "GEO-AS"
                    ]
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureHttpError
except:
    # handled in azure_rm_common
    pass

import re

AZURE_OBJECT_CLASS = 'TrafficManagerEndpoints'


def serialize_endpoint(endpoint):
    return dict(
        id=endpoint.id,
        name=endpoint.name,
        type=endpoint.type,
        target_resource_id=endpoint.target_resource_id,
        target=endpoint.target,
        endpoint_status=endpoint.endpoint_status,
        weight=endpoint.weight,
        priority=endpoint.priority,
        endpoint_location=endpoint.endpoint_location,
        min_child_endpoints=endpoint.min_child_endpoints,
        geo_mapping=endpoint.geo_mapping,
    )


class AzureRMTrafficManagerEndpointFacts(AzureRMModuleBase):
    """Utility class to get Azure Traffic Manager Endpoint facts"""

    def __init__(self):

        self.module_args = dict(
            profile_name=dict(
                type='str',
                required=True),
            resource_group=dict(
                type='str',
                required=True),
            name=dict(type='str'),
            type=dict(
                type='str',
                choices=[
                    'azureEndpoints',
                    'externalEndpoints',
                    'nestedEndpoints'
                ])
        )

        self.results = dict(
            changed=False,
            endpoints=[]
        )

        self.profile_name = None
        self.name = None
        self.resource_group = None
        self.type = None

        super(AzureRMTrafficManagerEndpointFacts, self).__init__(
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        if self.name:
            self.results['tms'] = self.get_item()
        elif self.resource_group:
            self.results['tms'] = self.list_resource_group()
        else:
            self.results['tms'] = self.list_all()

        return self.results

    def get_item(self):
        """Get a single Azure Traffic Manager"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.traffic_manager_management_client.endpoints.get(
                self.resource_group, self.profile_name, self.type, self.name)
        except CloudError:
            pass

        if item and self.has_tags(item.tags, self.tags):
            result = [self.serialize_tm(item)]

        return result

    def list_by_profile(self):
        """Get all Azure Traffic Manager endpoints of a profile"""

        self.log('List all endpoints belongs to a Traffic Manager profile')

        try:
            response = self.traffic_manager_management_client.profiles.get(self.resource_group, self.profile_name)
        except AzureHttpError as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if item.endpoints:
                for endpoint in item.endpoints:
                    results.append(serialize_endpoint(endpoint))

        return results

    def list_by_type(self):
        """Get all Azure Traffic Managers endpoints of a profile by type"""
        self.log('List all Traffic Manager endpoints of a profile by type')
        try:
            response = self.traffic_manager_management_client.profiles.get(self.resource_group, self.profile_name)
        except AzureHttpError as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if item.endpoints:
                for endpoint in item.endpoints:
                    if endpoint.type == self.type:
                        results.append(serialize_endpoint(endpoint))
        return results


def main():
    """Main module execution code path"""

    AzureRMTrafficManagerEndpointFacts()


if __name__ == '__main__':
    main()
