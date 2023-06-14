import boto3
from typing import List
from server_config import ServerConfig


class AWSProvider:
    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.elbv2 = boto3.client('elbv2')
        self.iam = boto3.client('iam')
        self.rds = boto3.client('rds')
        self.s3 = boto3.client('s3')

    def create_storage(size: int, storage_type: str) -> str:
        s3 = boto3.client('s3')
        iam = boto3.client('iam')
        rds = boto3.client('rds')

        # Create bucket
        bucket_name = 'my-bucket-name'
        s3.create_bucket(Bucket=bucket_name)

    def create_instances(self, count: int, instance_type: str) -> List[str]:
        # Create instances
        instances = self.ec2.create_instances(
            ImageId='ami-0c94855ba95c71c99',
            MinCount=count,
            MaxCount=count,
            InstanceType=instance_type,
            KeyName='my-key-pair',
            SecurityGroups=['my-security-group']
        )

        # Wait for instances to be running
        for instance in instances:
            instance.wait_until_running()

        # Return instance IDs
        return [instance.id for instance in instances]

    def configure_instances(self, instance_ids: List[str], server_config: ServerConfig):
        # Configure instances
        for instance_id in instance_ids:
            instance = self.ec2.Instance(instance_id)

            # Apply security configurations
            instance.modify_attribute(
                Groups=['my-security-group', server_config.security_group_id]
            )

            # Apply logging configurations
            instance.modify_attribute(
                Attribute='userData',
                Value=server_config.user_data_script
            )

    def create_load_balancer(self, instance_ids: List[str]) -> str:
        # Create target group
        target_group_response = self.elbv2.create_target_group(
            Name='my-target-group',
            Protocol='HTTP',
            Port=80,
            TargetType='instance',
            VpcId='my-vpc-id'
        )
        target_group_arn = target_group_response['TargetGroups'][0]['TargetGroupArn']

        # Register instances with target group
        for instance_id in instance_ids:
            self.elbv2.register_targets(
                TargetGroupArn=target_group_arn,
                Targets=[{'Id': instance_id}]
            )

        # Create load balancer
        load_balancer_response = self.elbv2.create_load_balancer(
            Name='my-load-balancer',
            Subnets=['my-subnet-id'],
            SecurityGroups=['my-security-group'],
            Scheme='internet-facing',
            Type='application'
        )
        load_balancer_arn = load_balancer_response['LoadBalancers'][0]['LoadBalancerArn']

        # Create listener
        self.elbv2.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol='HTTP',
            Port=80,
            DefaultActions=[
                {'Type': 'forward', 'TargetGroupArn': target_group_arn}]
        )

        # Return load balancer DNS
        return load_balancer_response['LoadBalancers'][0]['DNSName']

    def create_storage(self, size: int, storage_type: str) -> str:
        # Create bucket
        bucket_name = 'my-bucket-name'
        self.s3.create_bucket(Bucket=bucket_name)

        # Create IAM role for RDS
        role_name = 'my-rds-role'
        assume_role_policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Principal': {'Service': 'rds.amazonaws.com'},
                    'Action': 'sts:AssumeRole'
                }
            ]
        }
        role_response = self.iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
        )
        role_arn = role_response['Role']['Arn']

        # Attach policy to IAM role
        policy_arn = 'arn:aws:iam::aws:policy/AmazonS3FullAccess'
        self.iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )

        # Create RDS storage
        storage_response = self.rds.create_db_cluster(
            Engine='postgres',
            EngineVersion='14.1',
            DBInstanceIdentifier='my-db-instance',
            MasterUsername='my-db-username',
            MasterUserPassword='my-db-password',
            VpcSecurityGroupIds=['my-security-group'],
            DBSubnetGroupName='my-subnet-group',
            BackupRetentionPeriod=7,
            PreferredBackupWindow='02:00-03:00',
            Port=5432,
            StorageEncrypted=True,
            KmsKeyId='my-kms-key-id',
            MultiAZ=True,
            StorageType=storage_type,
            AllocatedStorage=size,
            IAMDatabaseAuthenticationEnabled=True,
            EnableCloudwatchLogsExports=['postgresql'],
            DBParameterGroupName='default.postgres14',
            DBInstanceClass='db.t3.medium'
        )

        # Return storage ID
        return storage_response['DBCluster']['DBClusterIdentifier']
