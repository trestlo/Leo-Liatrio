# Leo-Liatrio

## dev branch

Tools that need to be installed:
- Python and pip ruamel.yaml
- AWS CLI
- Terraform
- Docker
- kubectl

AWS CLI must be logged in as a role that can run the deploy script.
Permissions needed:
- IAM
- ECR
- EKS
- VPC
- EC2

Connect to AWS (Run the following command and then input Access Key and Secret Key when prompted):

```sh
aws configure
```

Run the deployment python script:

```sh
python3 deploy.py
```

The deployment script will handle everything from creating the infrastructure in AWS to building the Docker image.
The script will prompt for when everything should be cleaned up, and it will then dismantle and delete all built objects.
