# AWS Automation Tool

This tool automates the process of setting up a web server and a PostgreSQL database on AWS. It uses the boto3 Python SDK to interact with various AWS services including EC2, ELB, IAM, RDS, and S3.

## Features

- Creates EC2 instances with a specified instance type.
- Configures the instances with a specified server configuration.
- Creates a load balancer and registers the instances with it.
- Creates an S3 bucket for storage.
- Creates an IAM role for RDS and attaches the necessary policies.
- Creates a PostgreSQL database on RDS with a specified configuration.

## Prerequisites

- Python 3.6 or later.
- boto3 Python SDK.
- AWS account with the necessary permissions for EC2, ELB, IAM, RDS, and S3.
- AWS credentials configured in your environment.

## Usage

1. Clone this repository to your local machine.
2. Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script with your desired parameters:

    ```bash
    python main.py
    ```

## Security

This tool handles sensitive data like AWS credentials, usernames, and passwords. It's recommended to store these values in environment variables or use AWS Secrets Manager instead of hardcoding them in your code.

## Contributing

Contributions are welcome! Please read the contributing guidelines before making any changes.

## License

This project is licensed under the terms of the MIT license.
