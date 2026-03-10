provider "aws" {
  region = var.aws_region
}

data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_key_pair" "mlflow-key" {
  key_name   = "mlflow-key"
  public_key = file(var.ssh_public_key_path)
}

# -------------------------
# VPC
# -------------------------
resource "aws_vpc" "mlflow_vpc" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "mlflow-vpc"
  }
}

# -------------------------
# Internet Gateway
# -------------------------
resource "aws_internet_gateway" "mlflow_igw" {
  vpc_id = aws_vpc.mlflow_vpc.id

  tags = {
    Name = "mlflow-igw"
  }
}

# -------------------------
# Public Subnet
# -------------------------
resource "aws_subnet" "mlflow_public_subnet" {
  vpc_id                  = aws_vpc.mlflow_vpc.id
  cidr_block              = "10.10.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "mlflow-public-subnet"
  }
}

# -------------------------
# Route Table
# -------------------------
resource "aws_route_table" "mlflow_public_rt" {
  vpc_id = aws_vpc.mlflow_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mlflow_igw.id
  }

  tags = {
    Name = "mlflow-public-rt"
  }
}

resource "aws_route_table_association" "mlflow_rt_assoc" {
  subnet_id      = aws_subnet.mlflow_public_subnet.id
  route_table_id = aws_route_table.mlflow_public_rt.id
}

# -------------------------
# Security Group
# -------------------------
resource "aws_security_group" "mlflow_sg" {
  name        = "mlflow-sg"
  description = "Allow MLflow and SSH access"
  vpc_id      = aws_vpc.mlflow_vpc.id

  ingress {
    description = "MLflow UI"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# -------------------------
# EC2 MLflow Server
# -------------------------
resource "aws_instance" "mlflow_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = aws_key_pair.mlflow-key.key_name
  user_data     = file("${path.module}/mlflow-userdata.sh")

  subnet_id = aws_subnet.mlflow_public_subnet.id

  vpc_security_group_ids = [
    aws_security_group.mlflow_sg.id
  ]

  tags = {
    Name = "mlflow-server"
  }
}