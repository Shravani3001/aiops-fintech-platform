variable "aws_region" {
  default = "ap-south-1"
}

variable "public_key_path" {
  description = "Path to SSH public key"
  default = "./jenkins-key.pub"
}

