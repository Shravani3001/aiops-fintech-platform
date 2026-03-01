output "jenkins_public_ip" {
  description = "Public IP of Jenkins EC2"
  value       = aws_instance.jenkins.public_ip
}

output "jenkins_ssh_command" {
  description = "SSH command to connect to Jenkins EC2"
  value       = "ssh -i ~/.ssh/jenkins_key ubuntu@${aws_instance.jenkins.public_ip}"
}

output "jenkins_url" {
  description = "Jenkins Web UI URL"
  value       = "http://${aws_instance.jenkins.public_ip}:8080"
}
