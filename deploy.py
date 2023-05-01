"""This module uses Terraform to create necessary resources in AWS then deploys 
    a k8s cluster using those resources."""
import sys
import time
import subprocess
import json
from ruamel.yaml import YAML

def run_command(command, cwd=None):
    """Run commands. Provide error and exit if failed"""
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd
        )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}\n\
            Error message: {stderr.decode('utf-8')}")
        sys.exit(1)
    return stdout.decode('utf-8')

TERRAFORM_DIR = "./terraform"
K8S_DIR = "./k8s-flask"

# Plan Terraform and display output
PLAN_OUTPUT = run_command("terraform init", cwd=TERRAFORM_DIR)
PLAN_OUTPUT = run_command("terraform plan", cwd=TERRAFORM_DIR)
print(PLAN_OUTPUT)

# Prompt user to apply
while True:
    user_input = input("Would you like to apply this Terraform? (yes or no): ")
    if user_input.lower() == "yes":
        print("Applying Terraform...")
        run_command("terraform apply -auto-approve", cwd=TERRAFORM_DIR)
        break
    if user_input.lower() == "no":
        sys.exit("User declined to apply. No changes made.")
    print("Invalid input.")
print("Terraform applied.")

# Get account ID and log into ECR
AWS_ACCOUNT_ID = run_command("aws sts get-caller-identity \
    --query 'Account' \
    --output text").strip()

print("Logging into ECR...")
run_command(f"aws ecr get-login-password --region us-west-2 | \
    docker login --username AWS --password-stdin \
        {AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com")

# Garbage Python, but gets the ECR URL and cluster name
ECR_REPOSITORY_URL = run_command("terraform output ecr_url", \
                                 cwd=TERRAFORM_DIR) \
                                .rsplit('= ', maxsplit=1)[-1].rstrip()
EKS_CLUSTER_NAME = run_command("terraform output cluster_name", \
                                 cwd=TERRAFORM_DIR) \
                                .rsplit('= ', maxsplit=1)[-1].rstrip()

# EKS_CLUSTER_NAME = run_command("terraform output cluster_name", \
#                                cwd=TERRAFORM_DIR)\
#                                 .rsplit('= ', maxsplit=1)[-1].rstrip()

# Push the Docker image to ECR
print("Building and pushing Docker image...")
run_command("docker build -t leo-flask-liatrio:dev .", \
            cwd=K8S_DIR)
run_command(f"docker tag leo-flask-liatrio:dev {ECR_REPOSITORY_URL}:dev", \
            cwd=K8S_DIR)
run_command(f"docker push {ECR_REPOSITORY_URL}:dev", \
            cwd=K8S_DIR)

# Load the YAML file
yaml = YAML()
with open('./k8s-flask/app-deployment.yaml', 'r') as f:
    data = yaml.load(f)

# Update the image value
data['spec']['template']['spec']['containers'][0]['image'] = "{ECR_REPOSITORY_URL}:dev"

# Write the updated YAML file
with open('./k8s-flask/app-deployment.yaml', 'w') as f:
    yaml.dump(data, f)

print("Connecting to EKS cluster...")
run_command(f"aws eks update-kubeconfig \
    --region us-west-2 --name {EKS_CLUSTER_NAME}")

print("Applying Kubernetes...")
run_command("kubectl apply -f service-deployment.yaml")
run_command("kubectl apply -f app-deployment.yaml")

print("Waiting for external IP to become available...")
time.sleep(30)
EXTERNAL_IP = None
while not EXTERNAL_IP:
    EXTERNAL_IP = run_command("kubectl get service leo-flask-svc \
        -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'").strip()
print(f"Application is accessible at: http://{EXTERNAL_IP}:8080/api/v1/message")
