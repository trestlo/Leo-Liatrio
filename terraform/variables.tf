variable "aws_region" {
  type        = string
  description = "The AWS region to deploy resources to"
  default     = "us-west-2"
}

variable "cluster_name" {
  type        = string
  description = "The name of the cluster to be deployed in EKS"
  default     = "leo-flask"
}

variable "instance_type" {
  type        = string
  description = "The instance type of the EC2 instances"
  default     = "t2.large"
}

variable "vpc_cidr_block" {
  type        = string
  default     = "10.20.0.0/16"
  description = "CIDR block range for the VPCS"
}

variable "private_subnet_cidr_blocks" {
  type        = list(string)
  default     = ["10.20.0.0/24", "10.20.1.0/24"]
  description = "CIDR block range for the private subnet"
}

variable "public_subnet_cidr_blocks" {
  type = list(string)
  default     = ["10.20.2.0/24", "10.20.3.0/24"]
  description = "CIDR block range for the public subnet"
}

variable "availability_zones" {
  type  = list(string)
  default = ["us-west-2a", "us-west-2b"]
  description = "List of availability zones for the selected region"
}
