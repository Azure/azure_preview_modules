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
module: azure_rm_devtestlabspolicy_facts
version_added: "2.8"
short_description: Get Azure Policy facts.
description:
    - Get facts of Azure Policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    lab_name:
        description:
            - The name of the lab.
        required: True
    name:
        description:
            - The name of the policy set.
        required: True
    name:
        description:
            - The name of the policy.
        required: True
    expand:
        description:
            - "Specify the $expand query. Example: 'properties($select=description)'"
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Policy
    azure_rm_devtestlabspolicy_facts:
      resource_group: resource_group_name
      lab_name: lab_name
      name: policy_set_name
      name: name
      expand: expand
'''

RETURN = '''
policies:
    description: A list of dictionaries containing facts for Policy.
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
                - "The status of the policy. Possible values include: 'Enabled', 'Disabled'"
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


class AzureRMPoliciesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            lab_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            expand=dict(
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
        self.lab_name = None
        self.name = None
        self.name = None
        self.expand = None
        self.tags = None
        super(AzureRMPoliciesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['policies'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.policies.get(resource_group_name=self.resource_group,
                                                     lab_name=self.lab_name,
                                                     policy_set_name=self.name,
                                                     name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Policies.')

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
    AzureRMPoliciesFacts()


if __name__ == '__main__':
    main()
