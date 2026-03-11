#!/bin/bash
apt update -y
apt install -y docker.io

systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

mkdir -p /mlruns

docker run -d \
  --name mlflow \
  -p 5000:5000 \
  -v /mlruns:/mlruns \
  ghcr.io/mlflow/mlflow:v2.12.2 \
  mlflow server \
  --host 0.0.0.0 \
  --port 5000