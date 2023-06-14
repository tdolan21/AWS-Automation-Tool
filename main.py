from typing import List
from aws_provider import AWSProvider
from postgresql_server import PostgreSQLServer
from server_config import ServerConfig

def main(instance_count: int, instance_type: str, db_username: str, db_password: str, db_name: str, db_instance_type: str, db_storage_size: int, db_storage_type: str, db_backup_retention_period: int, db_maintenance_window: str, db_preferred_backup_window: str, db_parameter_group_name: str, db_security_group_name: str, db_subnet_group_name: str, db_vpc_security_group_ids: List[str], db_vpc_subnet_ids: List[str], server_config: ServerConfig):
    print("Initializing AWS Provider...")
    # Initialize AWSProvider
    aws_provider = AWSProvider()

    print("Creating instances...")
    # Create instances
    instance_ids = aws_provider.create_instances(instance_count, instance_type)

    print("Configuring instances...")
    # Configure instances
    aws_provider.configure_instances(instance_ids, server_config)

    print("Creating load balancer...")
    # Create load balancer
    load_balancer_dns = aws_provider.create_load_balancer(instance_ids)

    print("Creating storage...")
    # Create storage
    storage_id = aws_provider.create_storage(db_storage_size, db_storage_type)

    print("Initializing PostgreSQL Server...")
    # Initialize PostgreSQLServer
    postgresql_server = PostgreSQLServer(db_username, db_password, db_name, db_instance_type, db_backup_retention_period, db_maintenance_window, db_preferred_backup_window, db_parameter_group_name, db_security_group_name, db_subnet_group_name, db_vpc_security_group_ids, db_vpc_subnet_ids)

    print("Creating database server...")
    # Create database server
    db_instance_id = postgresql_server.create_server(storage_id)

    print("Configuring database server...")
    # Configure database server
    postgresql_server.configure_server(db_instance_id)

    print("Initializing Server Config...")
    # Initialize ServerConfig
    server_config = ServerConfig()

    print("Applying server configurations...")
    # Apply server configurations
    server_config.apply_configurations(instance_ids + [db_instance_id], load_balancer_dns)

    print("Done!")