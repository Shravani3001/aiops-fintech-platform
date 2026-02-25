#!/bin/bash
set -euxo pipefail

exec > /var/log/user-data.log 2>&1

sleep 30
apt-get update -y
apt-get install -y docker.io git curl
systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu
