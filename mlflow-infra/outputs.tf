output "mlflow_public_ip" {
  value = aws_instance.mlflow_server.public_ip
}

output "mlflow_url" {
  value = "http://${aws_instance.mlflow_server.public_ip}:5000"
}