#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_virtualmachinescalesetinstance
version_added: "2.8"
short_description: Get Azure Virtual Machine Scale Set Instance facts.
description:
    - Get facts of Azure Virtual Machine Scale Set VMs.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    vmss_name:
        description:
            - The name of the VM scale set.
        required: True
    instance_id:
        description:
            - The instance ID of the virtual machine.
        required: True
    latest_model:
        type: bool
        description:
            - Set to C(yes) to upgrade to the latest model.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Upgrade instance to the latest image
    azure_rm_computevirtualmachinescalesetinstance:
      resource_group: myResourceGroup
      vmss_name: myVMSS
      instance_id: "2"
      latest_model: yes
'''

RETURN = '''
instances:
    description: A list of instances.
    returned: always
    type: complex
    contains:
        instance_id:
            description:
                - Virtual Machine instance Id
            returned: always
            type: str
            sample: 0
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: { 'tag1': 'abc' }
        latest_model:
            description:
                - Is latest model applied?
            returned: always
            type: bool
            sample: True
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualMachineScaleSetInstance(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vmss_name=dict(
                type='str',
                required=True
            ),
            instance_id=dict(
                type='str'
            ),
            latest_model=dict(
                type='bool'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.vmss_name = None
        self.instance_id = None
        self.latest_model = None
        super(AzureRMVirtualMachineScaleSetInstance, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['instances'] = self.get()

        self.results['aaa'] = (self.latest_model is not None)
        self.results['bbb'] = not self.results['instances'][0].get('latest_model_applied', None)

        if self.latest_model is not None and not self.results['instances'][0].get('latest_model_applied', None):
            self.apply_latest_model()
            self.results['instances'][0]['latest_model'] = True

        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.virtual_machine_scale_set_vms.get(resource_group_name=self.resource_group,
                                                                          vm_scale_set_name=self.vmss_name,
                                                                          instance_id=self.instance_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Virtual Machine Scale Set VM.')

        if response:
            results.append(self.format_response(response))

        return results

    def apply_latest_model(self):
        try:
            poller = self.compute_client.virtual_machine_scale_sets.update_instances(resource_group_name=self.resource_group,
                                                                                     vm_scale_set_name=self.vmss_name,
                                                                                     instance_ids=[self.instance_id])
            self.get_poller_result(poller)
        except CloudError as exc:
            self.fail("Error applying latest model {0} - {1}".format(self.name, str(exc)))


    def format_response(self, item):
        d = item.as_dict()
        d = {
            'tags': d.get('tags', None),
            'instance_id': d.get('instance_id', None),
            'latest_model': d.get('latest_model_applied', None)
        }
        return d


def main():
    AzureRMVirtualMachineScaleSetInstance()


if __name__ == '__main__':
    main()
