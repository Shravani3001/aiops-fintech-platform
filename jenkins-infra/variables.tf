variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project prefix for resource naming"
  type        = string
  default     = "jenkins-lab"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.10.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR for public subnet"
  type        = string
  default     = "10.10.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR for private subnet"
  type        = string
  default     = "10.10.2.0/24"
}

variable "availability_zone" {
  description = "AZ for subnets"
  type        = string
  default     = "ap-south-1a"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key"
  type        = string
  default     = "~/.ssh/jenkins_key.pub"
}
