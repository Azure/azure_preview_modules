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
module: azure_rm_devtestlabsnotificationchannel
version_added: "2.8"
short_description: Manage Notification Channel instance.
description:
    - Create, update and delete instance of Notification Channel.

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
            - The name of the notificationChannel.
        required: True
    location:
        description:
            - The location of the resource.
    web_hook_url:
        description:
            - The webhook URL to send notifications to.
    description:
        description:
            - Description of notification.
    events:
        description:
            - The list of event for which this notification is enabled.
        type: list
        suboptions:
            event_name:
                description:
                    - The event type for which this notification is enabled (i.e. C(auto_shutdown), C(cost)).
                choices:
                    - 'auto_shutdown'
                    - 'cost'
    unique_identifier:
        description:
            - The unique immutable identifier of a resource (Guid).
    state:
      description:
        - Assert the state of the Notification Channel.
        - Use 'present' to create or update an Notification Channel and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Notification Channel
    azure_rm_devtestlabsnotificationchannel:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The identifier of the resource.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.devtestlabs import DevTestLabsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMNotificationChannels(AzureRMModuleBase):
    """Configuration class for an Azure RM Notification Channel resource"""

    def __init__(self):
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
            location=dict(
                type='str'
            ),
            web_hook_url=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            events=dict(
                type='list'
            ),
            unique_identifier=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.lab_name = None
        self.name = None
        self.notification_channel = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMNotificationChannels, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.notification_channel["location"] = kwargs[key]
                elif key == "web_hook_url":
                    self.notification_channel["web_hook_url"] = kwargs[key]
                elif key == "description":
                    self.notification_channel["description"] = kwargs[key]
                elif key == "events":
                    ev = kwargs[key]
                    if 'event_name' in ev:
                        if ev['event_name'] == 'auto_shutdown':
                            ev['event_name'] = 'AutoShutdown'
                        elif ev['event_name'] == 'cost':
                            ev['event_name'] = 'Cost'
                    self.notification_channel["events"] = ev
                elif key == "unique_identifier":
                    self.notification_channel["unique_identifier"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_notificationchannel()

        if not old_response:
            self.log("Notification Channel instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Notification Channel instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Notification Channel instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_notificationchannel()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Notification Channel instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_notificationchannel()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_notificationchannel():
                time.sleep(20)
        else:
            self.log("Notification Channel instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_notificationchannel(self):
        '''
        Creates or updates Notification Channel with the specified configuration.

        :return: deserialized Notification Channel instance state dictionary
        '''
        self.log("Creating / Updating the Notification Channel instance {0}".format(self.name))

        try:
            response = self.mgmt_client.notification_channels.create_or_update(resource_group_name=self.resource_group,
                                                                               lab_name=self.lab_name,
                                                                               name=self.name,
                                                                               notification_channel=self.notification_channel)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Notification Channel instance.')
            self.fail("Error creating the Notification Channel instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_notificationchannel(self):
        '''
        Deletes specified Notification Channel instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Notification Channel instance {0}".format(self.name))
        try:
            response = self.mgmt_client.notification_channels.delete(resource_group_name=self.resource_group,
                                                                     lab_name=self.lab_name,
                                                                     name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Notification Channel instance.')
            self.fail("Error deleting the Notification Channel instance: {0}".format(str(e)))

        return True

    def get_notificationchannel(self):
        '''
        Gets the properties of the specified Notification Channel.

        :return: deserialized Notification Channel instance state dictionary
        '''
        self.log("Checking if the Notification Channel instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.notification_channels.get(resource_group_name=self.resource_group,
                                                                  lab_name=self.lab_name,
                                                                  name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Notification Channel instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Notification Channel instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def main():
    """Main execution"""
    AzureRMNotificationChannels()


if __name__ == '__main__':
    main()
