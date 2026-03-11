#!/bin/bash
set -e

echo "Updating system..."
apt update

echo "Installing Java..."
apt install -y openjdk-21-jdk

echo "Installing base tools..."
apt install -y docker.io git jq python3-pip unzip curl

echo "Installing AWS CLI v2..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

echo "Installing DVC with S3 support..."
pip3 install --no-cache-dir "dvc[s3]"

echo "Fixing PATH for DVC..."
ln -s /usr/local/bin/dvc /usr/bin/dvc || true

systemctl enable docker
systemctl start docker

echo "Allowing ubuntu user to run docker..."
usermod -aG docker ubuntu

echo "Creating Jenkins directory..."
mkdir -p /opt/jenkins
chown ubuntu:ubuntu /opt/jenkins

echo "Downloading Jenkins..."
cd /opt/jenkins
wget https://get.jenkins.io/war-stable/latest/jenkins.war

echo "Creating Jenkins service..."

cat <<EOF > /etc/systemd/system/jenkins.service
[Unit]
Description=Jenkins
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/jenkins
ExecStart=/usr/bin/java -Xms256m -Xmx512m -jar /opt/jenkins/jenkins.war
Restart=always
RestartSec=10
Environment="JENKINS_HOME=/home/ubuntu/.jenkins"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable jenkins
systemctl start jenkins

echo "Jenkins installation complete."