import time
import boto3
from typing import List

class PostgreSQLServer:
    def __init__(self, username: str, password: str, db_name: str, instance_type: str, backup_retention_period: int, maintenance_window: str, preferred_backup_window: str, parameter_group_name: str, security_group_name: str, subnet_group_name: str, vpc_security_group_ids: List[str], vpc_subnet_ids: List[str]):
        self.rds = boto3.client('rds')
        self.username = username
        self.password = password
        self.db_name = db_name
        self.instance_type = instance_type
        self.backup_retention_period = backup_retention_period
        self.maintenance_window = maintenance_window
        self.preferred_backup_window = preferred_backup_window
        self.parameter_group_name = parameter_group_name
        self.security_group_name = security_group_name
        self.subnet_group_name = subnet_group_name
        self.vpc_security_group_ids = vpc_security_group_ids
        self.vpc_subnet_ids = vpc_subnet_ids

    def create_server(self, storage_id: str) -> str:
        # Create database instance
        instance_response = self.rds.create_db_instance(
            DBInstanceIdentifier='my-db-instance',
            DBInstanceClass=self.instance_type,
            Engine='aurora-postgresql',
            EngineVersion='10.7',
            MasterUsername=self.username,
            MasterUserPassword=self.password,
            DBName=self.db_name,
            VpcSecurityGroupIds=self.vpc_security_group_ids,
            DBSubnetGroupName=self.subnet_group_name,
            PubliclyAccessible=False,
            MultiAZ=False,
            StorageEncrypted=True,
            KmsKeyId='my-kms-key-id',
            EnableIAMDatabaseAuthentication=True,
            DBParameterGroupName=self.parameter_group_name,
            BackupRetentionPeriod=self.backup_retention_period,
            PreferredBackupWindow=self.preferred_backup_window,
            StorageType='aurora',
            DBClusterIdentifier=storage_id,
            Tags=[{'Key': 'Name', 'Value': 'my-db-instance'}]
        )

        # Wait for database instance to be available
        while True:
            instance = self.rds.describe_db_instances(DBInstanceIdentifier='my-db-instance')['DBInstances'][0]
            if instance['DBInstanceStatus'] == 'available':
                break
            time.sleep(10)

        # Return database instance ID
        return instance_response['DBInstance']['DBInstanceIdentifier']

    def configure_server(self, instance_id: str):
        # Apply security configurations
        self.rds.modify_db_instance(
            DBInstanceIdentifier=instance_id,
            VpcSecurityGroupIds=self.vpc_security_group_ids
        )

        # Apply logging configurations
        self.rds.modify_db_instance(
            DBInstanceIdentifier=instance_id,
            EnableCloudwatchLogsExports=['postgresql']
        )