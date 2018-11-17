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
module: azure_rm_mariadbserversecurityalertpolicy
version_added: "2.8"
short_description: Manage Server Security Alert Policy instance.
description:
    - Create, update and delete instance of Server Security Alert Policy.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the threat detection policy.
        required: True
    state:
        description:
            - Specifies the state of the policy, whether it is C(enabled) or C(disabled).
            - Required when C(state) is I(present).
        choices:
            - 'enabled'
            - 'disabled'
    disabled_alerts:
        description:
            - "Specifies an array of alerts that are C(disabled). Allowed values are: Sql_Injection, Sql_Injection_Vulnerability, Access_Anomaly"
        type: list
    email_addresses:
        description:
            - Specifies an array of e-mail addresses to which the alert is sent.
        type: list
    email_account_admins:
        description:
            - Specifies that the alert is sent to the account administrators.
    storage_endpoint:
        description:
            - "Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). This blob storage will hold all Threat Detection audit
               logs."
    storage_account_access_key:
        description:
            - Specifies the identifier key of the Threat Detection audit storage account.
    retention_days:
        description:
            - Specifies the number of days to keep in the Threat Detection audit logs.
    state:
      description:
        - Assert the state of the Server Security Alert Policy.
        - Use 'present' to create or update an Server Security Alert Policy and 'absent' to delete it.
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
  - name: Create (or update) Server Security Alert Policy
    azure_rm_mariadbserversecurityalertpolicy:
      resource_group: securityalert-4799
      server_name: securityalert-6440
      name: Default
      state: Enabled
      disabled_alerts:
        - [
  "Access_Anomaly",
  "Usage_Anomaly"
]
      email_addresses:
        - [
  "testSecurityAlert@microsoft.com"
]
      email_account_admins: True
      storage_endpoint: https://mystorage.blob.core.windows.net
      storage_account_access_key: sdlfkjabc+sdlfkjsdlkfsjdfLDKFTERLKFDFKLjsdfksjdflsdkfD2342309432849328476458/3RSD==
      retention_days: 5
'''

RETURN = '''
id:
    description:
        - Resource ID
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/securityalert-4799/providers/Microsoft.DBforMariaDB/servers/securityalert-644
            0/securityAlertPolicies/default"
state:
    description:
        - "Specifies the state of the policy, whether it is enabled or disabled. Possible values include: 'Enabled', 'Disabled'"
    returned: always
    type: str
    sample: Enabled
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.rdbms.mariadb import MariaDBManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServerSecurityAlertPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Server Security Alert Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            disabled_alerts=dict(
                type='list'
            ),
            email_addresses=dict(
                type='list'
            ),
            email_account_admins=dict(
                type='str'
            ),
            storage_endpoint=dict(
                type='str'
            ),
            storage_account_access_key=dict(
                type='str'
            ),
            retention_days=dict(
                type='int'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServerSecurityAlertPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                 supports_check_mode=True,
                                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "state":
                    self.parameters["state"] = _snake_to_camel(kwargs[key], True)
                elif key == "disabled_alerts":
                    self.parameters["disabled_alerts"] = kwargs[key]
                elif key == "email_addresses":
                    self.parameters["email_addresses"] = kwargs[key]
                elif key == "email_account_admins":
                    self.parameters["email_account_admins"] = kwargs[key]
                elif key == "storage_endpoint":
                    self.parameters["storage_endpoint"] = kwargs[key]
                elif key == "storage_account_access_key":
                    self.parameters["storage_account_access_key"] = kwargs[key]
                elif key == "retention_days":
                    self.parameters["retention_days"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MariaDBManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_serversecurityalertpolicy()

        if not old_response:
            self.log("Server Security Alert Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Server Security Alert Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', {
                       })):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Server Security Alert Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serversecurityalertpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Server Security Alert Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serversecurityalertpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_serversecurityalertpolicy():
                time.sleep(20)
        else:
            self.log("Server Security Alert Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_serversecurityalertpolicy(self):
        '''
        Creates or updates Server Security Alert Policy with the specified configuration.

        :return: deserialized Server Security Alert Policy instance state dictionary
        '''
        self.log("Creating / Updating the Server Security Alert Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.server_security_alert_policies.create_or_update(resource_group_name=self.resource_group,
                                                                                        server_name=self.server_name,
                                                                                        security_alert_policy_name=self.name,
                                                                                        parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Server Security Alert Policy instance.')
            self.fail("Error creating the Server Security Alert Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serversecurityalertpolicy(self):
        '''
        Deletes specified Server Security Alert Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Server Security Alert Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.server_security_alert_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Server Security Alert Policy instance.')
            self.fail("Error deleting the Server Security Alert Policy instance: {0}".format(str(e)))

        return True

    def get_serversecurityalertpolicy(self):
        '''
        Gets the properties of the specified Server Security Alert Policy.

        :return: deserialized Server Security Alert Policy instance state dictionary
        '''
        self.log("Checking if the Server Security Alert Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.server_security_alert_policies.get(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           security_alert_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Server Security Alert Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Server Security Alert Policy instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMServerSecurityAlertPolicies()


if __name__ == '__main__':
    main()
