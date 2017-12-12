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
short_description: Manage SQL Database instance
description:
    - Create, update and delete instance of SQL Database

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
            - Resource location.
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
               ase by restoring a backup of a deleted database. sourceDatabaseId must be specified. If sourceDatabaseId is the database's original resource I
               D, then sourceDatabaseDeletionDate must be specified. Otherwise sourceDatabaseId must be the restorable dropped database resource ID and sourc
               eDatabaseDeletionDate is ignored. restorePointInTime may also be specified to restore from an earlier point in time.\n\nRestoreLongTermRetenti
               onBackup: Creates a database by restoring from a long term retention vault. recoveryServicesRecoveryPointResourceId must be specified as the r
               ecovery point resource ID.\n\nCopy, NonReadableSecondary, OnlineSecondary and RestoreLongTermRetentionBackup are not supported for DataWarehou
               se edition. Possible values include: 'Copy', 'Default', 'NonReadableSecondary', 'OnlineSecondary', 'PointInTimeRestore', 'Recovery', 'Restore'
               , 'RestoreLongTermRetentionBackup'"
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
               locations/{locationID}/capabilities) referred to by operationId: 'Capabilities_ListByLocation.'. Possible values include: 'Web', 'Business', '
               Basic', 'Standard', 'Premium', 'Free', 'Stretch', 'DataWarehouse', 'System', 'System2'"
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
               ilities_ListByLocation.'. Possible values include: 'Basic', 'S0', 'S1', 'S2', 'S3', 'P1', 'P2', 'P3', 'P4', 'P6', 'P11', 'P15', 'System', 'Sys
               tem2', 'ElasticPool'"
    elastic_pool_name:
        description:
            - "The name of the elastic pool the database is in. If elasticPoolName and requestedServiceObjectiveName are both updated, the value of requested
               ServiceObjectiveName is ignored. Not supported for DataWarehouse edition."
    read_scale:
        description:
            - "Conditional. If the database is a geo-secondary, readScale indicates whether read-only connections are allowed to this database or not. Not su
               pported for DataWarehouse edition. Possible values include: 'Enabled', 'Disabled'"
    sample_name:
        description:
            - "Indicates the name of the sample schema to apply when creating this database. If createMode is not Default, this value is ignored. Not support
               ed for DataWarehouse edition. Possible values include: 'AdventureWorksLT'"
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
      resource_group: resource_group_name
      server_name: server_name
      name: database_name
      location: location
      collation: collation
      create_mode: create_mode
      source_database_id: source_database_id
      source_database_deletion_date: source_database_deletion_date
      restore_point_in_time: restore_point_in_time
      recovery_services_recovery_point_resource_id: recovery_services_recovery_point_resource_id
      edition: edition
      max_size_bytes: max_size_bytes
      requested_service_objective_id: requested_service_objective_id
      requested_service_objective_name: requested_service_objective_name
      elastic_pool_name: elastic_pool_name
      read_scale: read_scale
      sample_name: sample_name
      zone_redundant: zone_redundant
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
                type='str',
                required=False
            ),
            collation=dict(
                type='str',
                required=False
            ),
            create_mode=dict(
                type='str',
                required=False
            ),
            source_database_id=dict(
                type='str',
                required=False
            ),
            source_database_deletion_date=dict(
                type='datetime',
                required=False
            ),
            restore_point_in_time=dict(
                type='datetime',
                required=False
            ),
            recovery_services_recovery_point_resource_id=dict(
                type='str',
                required=False
            ),
            edition=dict(
                type='str',
                required=False
            ),
            max_size_bytes=dict(
                type='str',
                required=False
            ),
            requested_service_objective_id=dict(
                type='str',
                required=False
            ),
            requested_service_objective_name=dict(
                type='str',
                required=False
            ),
            elastic_pool_name=dict(
                type='str',
                required=False
            ),
            read_scale=dict(
                type='str',
                required=False
            ),
            sample_name=dict(
                type='str',
                required=False
            ),
            zone_redundant=dict(
                type='str',
                required=False
            ),
            state=dict(
                type='str',
                required=False,
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
                    self.parameters.update({"location": kwargs[key]})
                elif key == "collation":
                    self.parameters.update({"collation": kwargs[key]})
                elif key == "create_mode":
                    self.parameters.update({"create_mode": kwargs[key]})
                elif key == "source_database_id":
                    self.parameters.update({"source_database_id": kwargs[key]})
                elif key == "source_database_deletion_date":
                    self.parameters.update({"source_database_deletion_date": kwargs[key]})
                elif key == "restore_point_in_time":
                    self.parameters.update({"restore_point_in_time": kwargs[key]})
                elif key == "recovery_services_recovery_point_resource_id":
                    self.parameters.update({"recovery_services_recovery_point_resource_id": kwargs[key]})
                elif key == "edition":
                    self.parameters.update({"edition": kwargs[key]})
                elif key == "max_size_bytes":
                    self.parameters.update({"max_size_bytes": kwargs[key]})
                elif key == "requested_service_objective_id":
                    self.parameters.update({"requested_service_objective_id": kwargs[key]})
                elif key == "requested_service_objective_name":
                    self.parameters.update({"requested_service_objective_name": kwargs[key]})
                elif key == "elastic_pool_name":
                    self.parameters.update({"elastic_pool_name": kwargs[key]})
                elif key == "read_scale":
                    self.parameters.update({"read_scale": kwargs[key]})
                elif key == "sample_name":
                    self.parameters.update({"sample_name": kwargs[key]})
                elif key == "zone_redundant":
                    self.parameters.update({"zone_redundant": kwargs[key]})

        old_response = None
        response = None
        results = dict()

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
                return self.results

            response = self.create_update_sqldatabase()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("SQL Database instance deleted")

            if self.check_mode:
                return self.results

            self.delete_sqldatabase()
            self.results['changed'] = True
        else:
            self.log("SQL Database instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response is not None:
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
            response = self.mgmt_client.databases.create_or_update(self.resource_group,
                                                                   self.server_name,
                                                                   self.name,
                                                                   self.parameters)
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
            response = self.mgmt_client.databases.delete(self.resource_group,
                                                         self.server_name,
                                                         self.name)
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
            response = self.mgmt_client.databases.get(self.resource_group,
                                                      self.server_name,
                                                      self.name)
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
