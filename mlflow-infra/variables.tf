variable "aws_region" {
  default = "ap-south-1"
}

variable "instance_type" {
  default = "t3.small"
}

variable "key_name" {
  description = "EC2 SSH key name"
  default     = "mlflow-key"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key"
  type        = string
  default     = "~/.ssh/mlflow-key.pub"
}