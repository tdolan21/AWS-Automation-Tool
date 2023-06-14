import os
from typing import List

class ServerConfig:
    def __init__(self):
        self.security_group_id = 'my-security-group-id'
        self.user_data_script = self._generate_user_data_script()

    def apply_configurations(self, instance_ids: List[str], load_balancer_dns: str):
        # Apply security configurations
        pass

    def _generate_user_data_script(self) -> str:
        # Generate user data script for logging configurations
        return f"""#!/bin/bash
echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/14/main/pg_hba.conf
echo "log_destination = 'csvlog'" >> /etc/postgresql/14/main/postgresql.conf
echo "logging_collector = on" >> /etc/postgresql/14/main/postgresql.conf
echo "log_directory = '/var/log/postgresql'" >> /etc/postgresql/14/main/postgresql.conf
echo "log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'" >> /etc/postgresql/14/main/postgresql.conf
echo "log_truncate_on_rotation = on" >> /etc/postgresql/14/main/postgresql.conf
echo "log_rotation_age = 1d" >> /etc/postgresql/14/main/postgresql.conf
echo "log_rotation_size = 0" >> /etc/postgresql/14/main/postgresql.conf
systemctl restart postgresql"""
