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
module: azure_rm_sqldatabase
version_added: "2.5"
short_description: Manage SQL Database instance.
description:
    - Create, update and delete instance of SQL Database.

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
            - The name of the database to be operated on (updated or created).
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    collation:
        description:
            - The collation of the database. If createMode is not Default, this value is ignored.
    create_mode:
        description:
            - "Specifies the mode of database creation.\n\nDefault: regular database creation.\n\nCopy: creates a database as a copy of an existing database.
                sourceDatabaseId must be specified as the resource ID of the source database.\n\nOnlineSecondary/NonReadableSecondary: creates a database as
               a (readable or nonreadable) secondary replica of an existing database. sourceDatabaseId must be specified as the resource ID of the existing p
               rimary database.\n\nPointInTimeRestore: Creates a database by restoring a point in time backup of an existing database. sourceDatabaseId must
               be specified as the resource ID of the existing database, and restorePointInTime must be specified.\n\nRecovery: Creates a database by restori
               ng a geo-replicated backup. sourceDatabaseId must be specified as the recoverable database resource ID to restore.\n\nRestore: Creates a datab
               ase by restoring a backup of a deleted database. sourceDatabaseId must be specified. If sourceDatabaseId is the databaseC(s original resource
               ID, then sourceDatabaseDeletionDate must be specified. Otherwise sourceDatabaseId must be the restorable dropped database resource ID and sour
               ceDatabaseDeletionDate is ignored. restorePointInTime may also be specified to restore from an earlier point in time.\n\nRestoreLongTermRetent
               ionBackup: Creates a database by restoring from a long term retention vault. recoveryServicesRecoveryPointResourceId must be specified as the
               recovery point resource ID.\n\nCopy, NonReadableSecondary, OnlineSecondary and RestoreLongTermRetentionBackup are not supported for DataWareho
               use edition. Possible values include: )CopyC(, )DefaultC(, )NonReadableSecondaryC(, )OnlineSecondaryC(, )PointInTimeRestoreC(, )RecoveryC(, )R
               estoreC(, )RestoreLongTermRetentionBackup'"
        choices: ['Copy', 'Default', 'NonReadableSecondary', 'OnlineSecondary', 'PointInTimeRestore', 'Recovery', 'Restore', 'RestoreLongTermRetentionBackup']
    source_database_id:
        description:
            - "Conditional. If createMode is Copy, NonReadableSecondary, OnlineSecondary, PointInTimeRestore, Recovery, or Restore, then this value is requir
               ed. Specifies the resource ID of the source database. If createMode is NonReadableSecondary or OnlineSecondary, the name of the source databas
               e must be the same as the new database being created."
    source_database_deletion_date:
        description:
            - "Conditional. If createMode is Restore and sourceDatabaseId is the deleted database's original resource id when it existed (as opposed to its c
               urrent restorable dropped database id), then this value is required. Specifies the time that the database was deleted."
    restore_point_in_time:
        description:
            - "Conditional. If createMode is PointInTimeRestore, this value is required. If createMode is Restore, this value is optional. Specifies the poin
               t in time (ISO8601 format) of the source database that will be restored to create the new database. Must be greater than or equal to the sourc
               e database's earliestRestoreDate value."
    recovery_services_recovery_point_resource_id:
        description:
            - "Conditional. If createMode is RestoreLongTermRetentionBackup, then this value is required. Specifies the resource ID of the recovery point to
               restore from."
    edition:
        description:
            - "The edition of the database. The DatabaseEditions enumeration contains all the valid editions. If createMode is NonReadableSecondary or Online
               Secondary, this value is ignored. To see possible values, query the capabilities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/
               locations/{locationID}/capabilities) referred to by operationId: 'Capabilities_ListByLocation.'. Possible values include: C(Web), C(Business),
                C(Basic), C(Standard), C(Premium), C(Free), C(Stretch), C(DataWarehouse), C(System), C(System2)"
        choices: ['Web', 'Business', 'Basic', 'Standard', 'Premium', 'Free', 'Stretch', 'DataWarehouse', 'System', 'System2']
    max_size_bytes:
        description:
            - "The max size of the database expressed in bytes. If createMode is not Default, this value is ignored. To see possible values, query the capabi
               lities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/locations/{locationID}/capabilities) referred to by operationId: 'Capabili
               ties_ListByLocation.'"
    requested_service_objective_id:
        description:
            - "The configured service level objective ID of the database. This is the service level objective that is in the process of being applied to the
               database. Once successfully updated, it will match the value of currentServiceObjectiveId property. If requestedServiceObjectiveId and request
               edServiceObjectiveName are both updated, the value of requestedServiceObjectiveId overrides the value of requestedServiceObjectiveName. To see
                possible values, query the capabilities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/locations/{locationID}/capabilities) ref
               erred to by operationId: 'Capabilities_ListByLocation.'"
    requested_service_objective_name:
        description:
            - "The name of the configured service level objective of the database. This is the service level objective that is in the process of being applie
               d to the database. Once successfully updated, it will match the value of serviceLevelObjective property. To see possible values, query the cap
               abilities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/locations/{locationID}/capabilities) referred to by operationId: 'Capab
               ilities_ListByLocation.'. Possible values include: C(Basic), C(S0), C(S1), C(S2), C(S3), C(P1), C(P2), C(P3), C(P4), C(P6), C(P11), C(P15), C(
               System), C(System2), C(ElasticPool)"
        choices: ['Basic', 'S0', 'S1', 'S2', 'S3', 'P1', 'P2', 'P3', 'P4', 'P6', 'P11', 'P15', 'System', 'System2', 'ElasticPool']
    elastic_pool_name:
        description:
            - "The name of the elastic pool the database is in. If elasticPoolName and requestedServiceObjectiveName are both updated, the value of requested
               ServiceObjectiveName is ignored. Not supported for DataWarehouse edition."
    read_scale:
        description:
            - "Conditional. If the database is a geo-secondary, readScale indicates whether read-only connections are allowed to this database or not. Not su
               pported for DataWarehouse edition. Possible values include: C(Enabled), C(Disabled)"
        choices: ['Enabled', 'Disabled']
    sample_name:
        description:
            - "Indicates the name of the sample schema to apply when creating this database. If createMode is not Default, this value is ignored. Not support
               ed for DataWarehouse edition. Possible values include: C(AdventureWorksLT)"
        choices: ['AdventureWorksLT']
    zone_redundant:
        description:
            - Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) SQL Database
    azure_rm_sqldatabase:
      resource_group: sqlcrudtest-4799
      server_name: sqlcrudtest-5961
      name: testdb
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
database_id:
    description:
        - The ID of the database.
    returned: always
    type: str
    sample: database_id
status:
    description:
        - The status of the database.
    returned: always
    type: str
    sample: status
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDatabases(AzureRMModuleBase):
    """Configuration class for an Azure RM SQL Database resource"""

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
            location=dict(
                type='str'
            ),
            collation=dict(
                type='str'
            ),
            create_mode=dict(
                type='str',
                choices=['Copy', 'Default', 'NonReadableSecondary', 'OnlineSecondary', 'PointInTimeRestore', 'Recovery', 'Restore', 'RestoreLongTermRetentionBackup']
            ),
            source_database_id=dict(
                type='str'
            ),
            source_database_deletion_date=dict(
                type='datetime'
            ),
            restore_point_in_time=dict(
                type='datetime'
            ),
            recovery_services_recovery_point_resource_id=dict(
                type='str'
            ),
            edition=dict(
                type='str',
                choices=['Web', 'Business', 'Basic', 'Standard', 'Premium', 'Free', 'Stretch', 'DataWarehouse', 'System', 'System2']
            ),
            max_size_bytes=dict(
                type='str'
            ),
            requested_service_objective_id=dict(
                type='str'
            ),
            requested_service_objective_name=dict(
                type='str',
                choices=['Basic', 'S0', 'S1', 'S2', 'S3', 'P1', 'P2', 'P3', 'P4', 'P6', 'P11', 'P15', 'System', 'System2', 'ElasticPool']
            ),
            elastic_pool_name=dict(
                type='str'
            ),
            read_scale=dict(
                type='str',
                choices=['Enabled', 'Disabled']
            ),
            sample_name=dict(
                type='str',
                choices=['AdventureWorksLT']
            ),
            zone_redundant=dict(
                type='str'
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

        super(AzureRMDatabases, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "collation":
                    self.parameters["collation"] = kwargs[key]
                elif key == "create_mode":
                    self.parameters["create_mode"] = kwargs[key]
                elif key == "source_database_id":
                    self.parameters["source_database_id"] = kwargs[key]
                elif key == "source_database_deletion_date":
                    self.parameters["source_database_deletion_date"] = kwargs[key]
                elif key == "restore_point_in_time":
                    self.parameters["restore_point_in_time"] = kwargs[key]
                elif key == "recovery_services_recovery_point_resource_id":
                    self.parameters["recovery_services_recovery_point_resource_id"] = kwargs[key]
                elif key == "edition":
                    self.parameters["edition"] = kwargs[key]
                elif key == "max_size_bytes":
                    self.parameters["max_size_bytes"] = kwargs[key]
                elif key == "requested_service_objective_id":
                    self.parameters["requested_service_objective_id"] = kwargs[key]
                elif key == "requested_service_objective_name":
                    self.parameters["requested_service_objective_name"] = kwargs[key]
                elif key == "elastic_pool_name":
                    self.parameters["elastic_pool_name"] = kwargs[key]
                elif key == "read_scale":
                    self.parameters["read_scale"] = kwargs[key]
                elif key == "sample_name":
                    self.parameters["sample_name"] = kwargs[key]
                elif key == "zone_redundant":
                    self.parameters["zone_redundant"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_sqldatabase()

        if not old_response:
            self.log("SQL Database instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("SQL Database instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if SQL Database instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the SQL Database instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sqldatabase()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("SQL Database instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sqldatabase()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_sqldatabase():
                time.sleep(20)
        else:
            self.log("SQL Database instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]
            self.results["database_id"] = response["database_id"]
            self.results["status"] = response["status"]

        return self.results

    def create_update_sqldatabase(self):
        '''
        Creates or updates SQL Database with the specified configuration.

        :return: deserialized SQL Database instance state dictionary
        '''
        self.log("Creating / Updating the SQL Database instance {0}".format(self.name))

        try:
            response = self.mgmt_client.databases.create_or_update(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name,
                                                                   database_name=self.name,
                                                                   parameters=self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the SQL Database instance.')
            self.fail("Error creating the SQL Database instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sqldatabase(self):
        '''
        Deletes specified SQL Database instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SQL Database instance {0}".format(self.name))
        try:
            response = self.mgmt_client.databases.delete(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         database_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the SQL Database instance.')
            self.fail("Error deleting the SQL Database instance: {0}".format(str(e)))

        return True

    def get_sqldatabase(self):
        '''
        Gets the properties of the specified SQL Database.

        :return: deserialized SQL Database instance state dictionary
        '''
        self.log("Checking if the SQL Database instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.databases.get(resource_group_name=self.resource_group,
                                                      server_name=self.server_name,
                                                      database_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SQL Database instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SQL Database instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMDatabases()

if __name__ == '__main__':
    main()
