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
module: azure_rm_devtestlabsglobalschedule_facts
version_added: "2.8"
short_description: Get Azure Global Schedule facts.
description:
    - Get facts of Azure Global Schedule.

options:
    resource_group:
        description:
            - The name of the resource group.
    expand:
        description:
            - "Specify the $expand query. Example: 'properties($select=status)'"
    filter:
        description:
            - The filter to apply to the operation.
    top:
        description:
            - The maximum number of resources to return from the operation.
    orderby:
        description:
            - The ordering expression for the results, using OData notation.
    name:
        description:
            - The name of the schedule.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Global Schedule
    azure_rm_devtestlabsglobalschedule_facts:
      resource_group: resource_group_name
      expand: expand
      filter: filter
      top: top
      orderby: orderby

  - name: List instances of Global Schedule
    azure_rm_devtestlabsglobalschedule_facts:
      expand: expand
      filter: filter
      top: top
      orderby: orderby

  - name: Get instance of Global Schedule
    azure_rm_devtestlabsglobalschedule_facts:
      resource_group: resource_group_name
      name: name
      expand: expand
'''

RETURN = '''
global_schedules:
    description: A list of dictionaries containing facts for Global Schedule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The identifier of the resource.
            returned: always
            type: str
            sample: id
        tags:
            description:
                - The tags of the resource.
            returned: always
            type: complex
            sample: tags
        status:
            description:
                - "The status of the schedule (i.e. Enabled, Disabled). Possible values include: 'Enabled', 'Disabled'"
            returned: always
            type: str
            sample: status
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.devtestlabs import DevTestLabsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMGlobalSchedulesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            expand=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            orderby=dict(
                type='str'
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
        self.expand = None
        self.filter = None
        self.top = None
        self.orderby = None
        self.name = None
        self.tags = None
        super(AzureRMGlobalSchedulesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['global_schedules'] = self.list_by_resource_group()
        else:
            self.results['global_schedules'] = self.list_by_subscription()
        elif (self.resource_group is not None and
                self.name is not None):
            self.results['global_schedules'] = self.get()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.global_schedules.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for GlobalSchedules.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.global_schedules.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for GlobalSchedules.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.global_schedules.get(resource_group_name=self.resource_group,
                                                             name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for GlobalSchedules.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'tags': d.get('tags', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMGlobalSchedulesFacts()


if __name__ == '__main__':
    main()
