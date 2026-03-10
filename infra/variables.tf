variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "aiops-fintech"
}

variable "openai_api_key" {
  type      = string
  sensitive = true
}

variable "mlflow_url" {
  description = "MLflow server URL"
}