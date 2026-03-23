# Project Title

**AIOps FinTech Platform – AI-Driven Incident Detection and Self-Healing System for FinTech Services**

---

# Project Overview

The **AIOps FinTech Platform** is an end-to-end intelligent monitoring and incident management system designed for financial technology applications. The platform combines **Machine Learning, DevOps, and AIOps practices** to monitor API performance, detect operational anomalies, generate automated root cause analysis (RCA), and trigger self-healing mechanisms.

The system integrates a **credit risk prediction machine learning model** with a production-style infrastructure that includes **FastAPI services, MLflow model registry, Dockerized services, Prometheus monitoring, Grafana dashboards, and Alertmanager notifications**.

When operational issues such as high latency or abnormal request volumes occur, the platform automatically detects the incident through monitoring alerts, analyzes the root cause using an AI-driven AIOps module, and attempts automated remediation actions. Incident history is also stored and reused to reduce repeated analysis and improve operational efficiency.

This project demonstrates how **MLOps, DevOps, and AIOps workflows can be combined to build resilient and intelligent financial service platforms**.

---

# Problem Statement

Modern FinTech applications operate in highly dynamic environments where service reliability, performance, and quick incident resolution are critical. Traditional monitoring systems generate alerts when issues occur, but they often require **manual investigation and troubleshooting**, which can delay recovery and impact business operations.

In financial systems that handle loan approvals or credit risk predictions, downtime, slow responses, or system failures can lead to **customer dissatisfaction, operational losses, and compliance risks**.

Additionally, managing machine learning models in production requires proper **versioning, monitoring, and automated deployment mechanisms** to ensure reliability and reproducibility.

Therefore, there is a need for an intelligent system that can:

* Monitor application performance in real time
* Detect anomalies automatically
* Analyze the root cause of incidents
* Trigger automated recovery actions
* Maintain a reliable ML model deployment pipeline

---

# Objective of the Machine Learning Model

The objective of the machine learning model in this project is to **predict the credit risk of borrowers based on financial and behavioral features**.

The model helps financial institutions assess whether a borrower is likely to default or repay a loan, enabling faster and more data-driven decision making. By integrating the model into an API-based system, predictions can be served in real time as part of the fintech application workflow.

The ML model is managed through an **MLOps pipeline using MLflow Model Registry**, ensuring that models are versioned, tracked, and deployed consistently across environments.

---

# Tech Stack

### Programming & Backend

* Python
* FastAPI

### Machine Learning & MLOps

* Scikit-Learn
* MLflow
* DVC

### DevOps & Containerization

* Docker
* Docker Compose
* Jenkins

### Cloud Infrastructure

* AWS EC2
* AWS ECS Fargate
* AWS ECR
* Terraform

### Monitoring & AIOps

* Prometheus
* Grafana
* Alertmanager

### Database

* MongoDB

### Version Control

* Git
* GitHub

---

# Features

### Machine Learning Capabilities

* Credit risk prediction model for loan applicants
* Model training and artifact generation
* MLflow model tracking and registry-based deployment

### API-Based Prediction System

* FastAPI service for real-time prediction
* REST APIs for borrower data ingestion and prediction requests
* Health check endpoints for service monitoring

### Monitoring & Observability

* Prometheus metrics for API requests and latency
* Grafana dashboards for real-time visualization
* Alertmanager for automated alert notifications

### AIOps Incident Management

* Automatic detection of operational incidents through alerts
* AI-based root cause analysis for unknown incidents
* Incident severity classification and explanation generation

### Self-Healing Mechanism

* Automated remediation actions such as API restarts
* Storage of incident history in MongoDB
* Reuse of known fixes to reduce repeated troubleshooting

### Production-Style Infrastructure

* Fully containerized microservice architecture using Docker
* Infrastructure provisioning using Terraform
* Deployment on AWS ECS Fargate with Application Load Balancer

---

# Project Structure

```bash
aiops-fintech-platform
│
├ api/
│ ├ ml/
│ │ ├ data/
│ │ │ ├ raw/
│ │ │ │ ├ borrowers_raw.csv
│ │ │ │ └ .gitignore
│ │ │ └ processed/
| | |    ├ borrowers_processed.csv
│ │ ├ train.py
│ │ ├ feature_engineering.py
│ │ └ evaluate_model_light.py
│ │
│ ├ main.py
│ ├ incidents.py
│ ├ register_model.py
│ ├ seed_borrowers.py
│ ├ seed_incidents.py
| ├ dockerfile
│ └ requirements.txt
│
├ monitoring/
│ ├ alertmanager.yml
│ ├ prometheus.yml
│ └ rules/
|    ├ availability-alerts.yml
|    ├ error-alerts.yml
|    ├ latency-alerts.yml
|    ├ restart-alerts.yml
|    ├ traffic-alerts.yml
|    ├ unknown-alert.yml
│
├ infra/
|  ├ main.tf
|  ├ variables.tf
|  ├ outputs.tf
|  ├ provider.tf
|
├ jenkins-infra/
|  ├ install_jenkins.sh
|  ├ main.tf 
|  ├ variables.tf
|  ├ outputs.tf
|
├ mlflow-infra/
|  ├ main.tf
|  ├ mlflow-userdata.sh
|  ├ outputs.tf
|  ├ variables.tf
|
├ dvc-storage-infra/
|  ├ main.tf
|  ├ outputs.tf
|
├ .env
├ docker-compose.yml
├ Jenkinsfile
├ dvc.yaml
├ README.md
└ .gitignore
```

---

# Project Architecture

---

# Prerequisites

Make sure the following tools are installed on your system before running the project.

### 1. Python

Required to run the API service and ML components.

* Version: **Python 3.9 or higher**

Check installation:

```bash
python --version
```

---

### 2. Docker & Docker Compose

Used to run the application services such as:

* FastAPI API service
* Prometheus monitoring
* Grafana dashboards
* Alertmanager

Check installation:

```bash
docker --version
docker compose version
```

---

### 3. Git

Used to clone the project repository.

```bash
git --version
```

---

### 4. Terraform

Used to provision infrastructure on AWS including:

* ECS Fargate services
* Application Load Balancer
* Networking resources
* Jenkins infrastructure
* MLflow infrastructure
* DVC storage infrastructure

Recommended version:

```
Terraform >= 1.5
```

Check installation:

```bash
terraform --version
```

---

### 5. DVC (Data Version Control)

Used for:

* dataset versioning
* ML pipeline tracking
* data reproducibility

Check installation:

```bash
dvc --version
```

---

### 6. AWS CLI

Required for:

* authentication with AWS
* pushing Docker images to ECR
* interacting with ECS and other AWS services

Check installation:

```bash
aws --version
```

---

### 7. MongoDB Atlas Account

The platform uses **MongoDB Atlas** as the cloud database for storing:

* borrower data
* incident history
* AIOps learning records

You will need a **MongoDB connection URI**.

---

### 8. OpenAI API Key

Required for the **AIOps incident analysis module** to generate:

* root cause analysis (RCA)
* severity classification
* incident explanations

---

### 9. Slack Webhook 

Used for sending **alert notifications** from Alertmanager.

---

# Setup Instructions

Follow the steps below to set up and run the **AIOps FinTech Platform**.

---

# 1. Clone the Repository

```bash
git clone https://github.com/Shravani3001/aiops-fintech-platform.git
cd aiops-fintech-platform
```

---

# 2. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_openai_api_key

MONGO_URI=your_mongodb_connection_string

MODEL_NAME=credit_risk_model

MODEL_ALIAS=production

PROM_URL=http://prometheus:9090/api/v1/query

LATENCY_THRESHOLD=0.3

SLACK_WEBHOOK_URL=your_slack_webhook

ECS_CLUSTER_NAME=aiops-fintech-cluster

ECS_SERVICE_NAME=aiops-fintech-service

AWS_DEFAULT_REGION=ap-south-1

MLFLOW_TRACKING_URI=http://mlflow-server-public-ip:5000

MLFLOW_REGISTRY_URI=http://mlflow-server-public-ip:5000

AWS_ACCESS_KEY_ID=your_access_key

AWS_SECRET_ACCESS_KEY=your_secret_key

RAW_DATA_PATH=api/ml/data/raw/borrowers_raw.csv

PROCESSED_DATA_PATH=api/ml/data/processed/borrowers_processed.csv

FEATURE_PATH=api/ml/feature_columns.joblib

MODEL_PATH=api/ml/credit_risk_model.joblib
```

⚠️ Do **not commit the `.env` file** to GitHub.

---

## 3. Create MongoDB Atlas Cluster

This project uses **MongoDB Atlas** as the cloud database for storing:

* borrower data
* incident history
* AIOps learning records

Follow these steps to create the database.

### 1. Create MongoDB Atlas Account

Go to:

[https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)

Create a free account and log in.

---

### 2. Create a Cluster

Create a **free shared cluster (M0)**.

Choose:

* name - aiops
* Cloud Provider: AWS
* Region: Mumbai

---

### 3. Create Database User

Go to **Database Access → Add New Database User**

Example:

```text
Username: aiops_user
Password: your_password
```

Give **Read and Write access**.

---

### 4. Allow Network Access

Go to **Network Access → Add IP Address**

For development you can allow:

```text
0.0.0.0/0
```

(This allows access from any IP.)

---

### 5. Get the Connection String

Click:

```
Connect → Drivers → Python
```

MongoDB Atlas will give a connection string like:

Modify it by adding the **database name**.

Example:

```text
mongodb+srv://aiops_user:password@aiops.q5fbml.mongodb.net/credit_risk?retryWrites=true&w=majority&appName=aiops
```

**Note:** Replace `password` in the connection string with the password you created for the MongoDB Atlas database user. The username should remain **`aiops_user`**, as configured during the cluster setup.

---

### 6. Add the URI to `.env`

Add the connection string to your `.env` file.

```env
MONGO_URI=mongodb+srv://aiops_user:password@aiops.q5fbml.mongodb.net/credit_risk?retryWrites=true&w=majority&appName=aiops
```

This allows the API service to connect to MongoDB Atlas.

---

# 4. Start the Platform

The platform uses **Docker Compose** to run the core services.

Start the services:

```bash
cd aiops-fintech-platform

docker compose build

docker compose up -d
```

This launches the following components:

* Credit Risk API (FastAPI)
* Prometheus monitoring
* Grafana dashboards
* Alertmanager
* borrower-seeder
* incident-seeder

---

# 4. Verify Running Services

```bash
docker compose ps
```

After startup, access the services:

| Service           | URL                                                      |
| ----------------- | -------------------------------------------------------- |
| FastAPI API       | [http://localhost:8000](http://localhost:8000)           |
| API Documentation | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Prometheus        | [http://localhost:9090](http://localhost:9090)           |
| Grafana           | [http://localhost:3000](http://localhost:3000)           |
| Alertmanager      | [http://localhost:9093](http://localhost:9093)           |

---

# 5. Verify MongoDB Data

After starting the platform, verify that the seeders have populated the database.

### 1. Open MongoDB Atlas

Go to your MongoDB Atlas dashboard:

Navigate to:

```
Your cluster → Browse Collections
```

---

### 2. Select the Database

Open the following database:

```
credit_risk
```

---

### 3. Check the Collections

You should see the following collections created automatically:

```
borrowers
incidents
```

---

### 4. Verify Seeded Data

Open the **Browse Collections** and confirm that borrower documents are present.

### Expected Result

The database structure should look like:

```
credit_risk
 ├── borrowers
 └── incidents
```

If documents appear in both collections, the seeders have executed successfully.

---

# Infrastructure Deployment

The infrastructure for the platform is provisioned using **Terraform on AWS**.
This setup deploys the following components:

* **MLflow server** for model tracking and registry
* **AWS ECS infrastructure** for the API service
* **DVC remote storage infrastructure**
* **Jenkins CI/CD server**

Follow the steps below.

---

# 1. Deploy MLflow Infrastructure

Navigate to the MLflow infrastructure directory:

```bash
cd mlflow-infra
```

Generate an SSH key pair for accessing the MLflow server:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mlflow-key
```

Then run Terraform:

```bash
terraform init
terraform plan
terraform apply
```

### Why this step is needed

This Terraform configuration provisions an **MLflow tracking server on AWS EC2**, which is used to:

* track ML experiments
* store model versions
* manage the **MLflow Model Registry**

After deployment, Terraform will output a value similar to:

```text
mlflow_url = http://<public-ip>:5000
```

Save this URL — it will be used in the next step.

---

# 2. Deploy Application Infrastructure (ECS)

Navigate to the infrastructure folder:

```bash
cd ../infra
```

Update the **MongoDB connection string** by replacing `<password>` with your MongoDB Atlas cluster password:

```hcl
environment = [
  { name = "MLFLOW_TRACKING_URI", value = var.mlflow_url},
  { name = "MONGO_URI", value = "mongodb+srv://aiops_user:<password>@aiops.q5fbml.mongodb.net/credit_risk?retryWrites=true&w=majority&appName=aiops"},
  { name = "OPENAI_API_KEY", value = var.openai_api_key},
  { name = "ECS_CLUSTER_NAME", value = "${var.project_name}-cluster"},
  { name = "ECS_SERVICE_NAME", value = "${var.project_name}-service"},
  { name = "AWS_DEFAULT_REGION", value = var.aws_region}
]
```

---

### Create Terraform Variables File

Create a file named:

```text
terraform.tfvars
```

Add the following values:

```hcl
openai_api_key = "your-openai-api-key"
mlflow_url     = "http://mlflow-server-public-ip:5000"
```

Paste the **MLflow URL obtained from the previous Terraform output**.

---

### Run Terraform

```bash
terraform init
terraform plan
terraform apply
```

### Why this step is needed

This Terraform configuration creates the **core application infrastructure**, including:

* ECS cluster
* ECS service
* Task definition
* Application Load Balancer
* Networking and IAM roles

This infrastructure hosts the **FastAPI credit risk API service**.

---

# 3. Deploy DVC Storage Infrastructure

Navigate to the DVC storage infrastructure folder:

```bash
cd ../dvc-storage-infra
```

Run Terraform:

```bash
terraform init
terraform plan
terraform apply
```

### Why this step is needed

This infrastructure creates a **remote storage backend for DVC**, allowing datasets and model artifacts to be versioned and retrieved during CI/CD pipelines.

---

# 4. Deploy Jenkins CI/CD Server

Navigate to the Jenkins infrastructure folder:

```bash
cd ../jenkins-infra
```

Generate an SSH key pair:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_key
```

Then deploy Jenkins using Terraform:

```bash
terraform init
terraform plan
terraform apply
```

### Why this step is needed

This Terraform configuration provisions a **Jenkins server on AWS EC2**, which is used to:

* automate model training
* build Docker images
* push images to Amazon ECR
* deploy updated containers to ECS

---

# 5. Access MLflow and Jenkins

After deployment:

MLflow will be available at:

```text
http://<mlflow-public-ip>:5000
```

Jenkins will be available at:

```text
http://<jenkins-public-ip>:8080
```

---

# 6. SSH into Jenkins Server

Use the SSH command from Terraform output:

```bash
ssh -i ~/.ssh/jenkins_key ubuntu@<jenkins-public-ip>
```

Retrieve the Jenkins initial admin password:

```bash
sudo cat /home/ubuntu/.jenkins/secrets/initialAdminPassword
```

Paste this password into the Jenkins setup screen.

Create a Jenkins admin user and install **Suggested Plugins**.

---

# 7. Install Required Jenkins Plugins

Go to:

```
Manage Jenkins → Plugins
```

Install:

* Docker Pipeline
* Pipeline Stage View
* Pipeline Utility Steps
* Pipeline: AWS Steps
* Pipeline: GitHub

---

# 8. Push Project to GitHub

Initialize and push the repository:

```bash
git init
git add .
git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/your-username/aiops-fintech-platform.git

git push -u origin main
```

---

# 9. Create Jenkins Pipeline

In Jenkins:

```
New Item → Pipeline
```

Enable:

```
GitHub project
GitHub hook trigger for GITScm polling
```

In **Pipeline Definition** select:

```
Pipeline script from SCM
```

Set:

```
Repository URL → your GitHub repository
Branch → main
Script Path → Jenkinsfile
```

Save the pipeline.

---

# 10. Configure GitHub Webhook

In GitHub:

```
Repository → Settings → Webhooks → Add webhook
```

Set:

```
Payload URL:
http://<jenkins-public-ip>:8080/github-webhook/
```

Content type:

```
application/json
```

Now every push to GitHub will automatically trigger the Jenkins pipeline.

---

# Jenkins Pipeline Workflow

The pipeline performs the following steps:

1. Detects whether **ML or dataset changes occurred**
2. Pulls dataset from **DVC remote**
3. Re-runs the **ML training pipeline**
4. Builds a **Docker image of the API**
5. Pushes the image to **Amazon ECR**
6. Registers a **new ECS task definition**
7. Updates the ECS service to deploy the new version

This enables **automated CI/CD for both ML models and application code**.

---

# Add This Section After Jenkins Pipeline

## Verify ECS Deployment

After the Jenkins pipeline completes successfully, the application is deployed to **AWS ECS Fargate**.

### ⏳ Wait for Service Stabilization

It may take **3–5 minutes** for the ECS service to become healthy.

During this time:

* New task is created
* Container starts
* ALB health checks pass

---

## Get Application URL (ALB DNS)

When you ran `terraform apply` in the `infra` folder, an **Application Load Balancer (ALB)** was created.

You need to note the **ALB DNS name** from Terraform output.

Example:

```text id="w5v4y9"
alb_dns_name = aiops-fintech-alb-123456.ap-south-1.elb.amazonaws.com
```

If you missed it earlier, you can retrieve it again:

```bash id="h9k2df"
terraform output
```

---

## Access the Application

Once the ECS service is running and healthy, access the FastAPI service using:

```text id="e37r0y"
http://<alb_dns_name>
```

Example:

```text id="00c12r"
http://aiops-fintech-alb-123456.ap-south-1.elb.amazonaws.com
```

---

## Verify API Health

Open in browser or use curl:

```bash id="04izdl"
curl http://<alb_dns_name>/health
```

Expected response:

```json id="1anq6i"
{
  "status": "ok"
}
```

---

## Access API Documentation

```text id="kpbr69"
http://<alb_dns_name>/docs
```

This opens the FastAPI Swagger UI where you can test endpoints.

---

## Check ECS Service Status (Optional)

Go to AWS Console:

```id="1l0so6"
ECS → Clusters → aiops-fintech-cluster → Services
```

Verify:

* Desired tasks = 1
* Running tasks = 1
* Health status = Healthy

---

# Important Note 

⚠️ If the API is not accessible immediately:

* Wait a few minutes for ALB health checks
* Ensure ECS task is in **RUNNING** state
* Check target group health in EC2 → Load Balancers

---

### Access FastAPI via ALB

Once the ECS service is running, open:

```text
http://<alb-dns-name>/docs
```

This will open the FastAPI Swagger UI.

---

### Test Credit Risk Prediction

Navigate to the /predict endpoint
Click “Try it out”
Enter a borrower ID:

```json
{
  "borrower_id": "B001"
}
```

⚠️ Do not remove the double quotes.

Click Execute

You should receive a prediction response indicating the borrower’s credit risk.

---

# 9. Monitoring & AIOps Testing

The monitoring stack includes:

* **Prometheus** for metrics collection
* **Grafana** for dashboards
* **Alertmanager** for alert notifications

Alerts trigger the **AIOps module**, which performs:

* incident severity classification
* AI-based root cause analysis
* automated remediation actions

---

## 1. Access Monitoring Tools

Since monitoring runs locally via Docker:

| Tool         | URL                                            |
| ------------ | ---------------------------------------------- |
| Prometheus   | [http://localhost:9090](http://localhost:9090) |
| Grafana      | [http://localhost:3000](http://localhost:3000) |
| Alertmanager | [http://localhost:9093](http://localhost:9093) |

---

## 2. Test Known Alert (High Latency)

### Step 1: Modify Alert Rule

Open the file:

```text
monitoring/rules/latency-alerts.yml
```

Update the threshold to trigger quickly:

```yaml
expr: histogram_quantile(
        0.95,
        sum(rate(credit_model_prediction_latency_seconds_bucket[1m])) by (le)
      ) > 0.01
```

Also reduce duration:

```yaml
for: 30s
```

---

### Step 2: Restart Prometheus

```bash
docker compose restart prometheus
```

---

### Step 3: Generate Traffic

Open the FastAPI Swagger UI (http://<alb-dns-name>/docs) and execute the /predict endpoint multiple times (e.g., using borrower ID B001) until the alert is triggered.

---

### Step 4: Verify Alert

Go to:

```text
http://localhost:9090
```

Check:

```text
Alerts → HighPredictionLatency → Firing
```

---

### Step 5: Check Alertmanager

```text
http://localhost:9093
```

You should see the alert routed.

---

### Step 6: Check AIOps Logs

```bash
docker compose logs -f api
```

You will observe:

* alert received
* severity classification
* RCA generation
* possible self-healing action

---

### Step 7: Verify Auto-Healing

Run:

```bash
docker compose ps
```

You may see:

* `credit-risk-api` restarted recently

---

### Step 8: Verify Incident in MongoDB

Go to MongoDB Atlas:

```text
credit_risk → incidents
```

You should see:

* alert name
* severity
* RCA
* trigger count

---

## 3. Observe CI/CD Trigger

If self-healing involves deployment:

* Jenkins pipeline may trigger
* ECS task will update

Check in AWS Console:

```text
ECS → Cluster → Service → Tasks
```

---

## 4. Test Unknown Alert (AIOps Learning)

### Step 1: Modify Unknown Alert Rule

Open:

```text
monitoring/rules/unknown-alert.yml
```

Use:

```yaml
groups:
- name: unknown-alerts
  rules:
  - alert: UnknownTestAlert
    expr: sum(rate(http_requests_total[1m])) > 1
    for: 30s
    labels:
      severity: critical
      category: test
    annotations:
      summary: "Synthetic unknown incident for AIOps testing"
      current_value: "{{ $value }}"
```

---

### Step 2: Restart Prometheus

```bash
docker compose restart prometheus
```

---

### Step 3: Trigger Alert

Open the FastAPI Swagger UI (http://<alb-dns-name>/docs) and execute the /predict endpoint multiple times (e.g., using borrower ID B001) until the alert is triggered.

---

### Step 4: Verify Alert Flow

Check:

* Prometheus → alert firing
* Alertmanager → alert received
* Slack → notification received
* API logs → AI-generated RCA

---

## 5. AIOps Learning Behavior

For unknown alerts:

* OpenAI generates:

  * root cause analysis
  * suggested fix

* Incident is stored in MongoDB

After repeated occurrences:

* incident becomes **known**
* system skips OpenAI
* applies stored resolution

---

## 6. Important Design Note

⚠️ The system does **not automatically restart critical services** for unknown alerts.

Reason:

* prevents unsafe actions
* avoids incorrect self-healing
* ensures controlled remediation

---

## 7. Cost Optimization Strategy

* Unknown incidents → analyzed using OpenAI
* Stored in MongoDB
* Promoted to **known incidents** after validation

Result:

* reduced API cost
* faster resolution
* up to **95% incidents auto-handled**
* improved system reliability

---

Great — this is a very strong section 👍 I’ll **polish it into a clean, professional README format** with correct flow, wording, and clarity.

---

# Grafana Dashboard Setup

This section demonstrates how to visualize API performance metrics using **Grafana dashboards**.

---

## 1. Open Grafana

Access Grafana in your browser:

```text
http://localhost:3000
```

Login using your configured credentials (default is usually `admin / admin` if not changed).

---

## 2. Configure Prometheus Data Source

1. Go to **Connections → Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Set URL:

```text
http://prometheus:9090
```

5. Click **Save & Test**

---

## 3. Create Dashboard

1. Go to **Dashboards → New → New Dashboard**
2. Click **Add new panel**
3. Select **Prometheus** as the data source

Create the following panels:

---

## Panel 1: Prediction Requests Total

**Description:**
Total number of credit risk prediction requests handled by the API. This counter only increases and helps understand overall traffic volume and usage patterns.

**Query:**

```promql
credit_model_predictions_total
```

---

## Panel 2: Prediction Latency (95th Percentile)

**Description:**
95th percentile prediction latency over the last 5 minutes. This shows how slow the slowest 5% of requests are and helps detect performance degradation.

**Query:**

```promql
histogram_quantile(0.95, sum(rate(credit_model_prediction_latency_seconds_bucket[5m])) by (le))
```

---

## Panel 3: Requests per Minute

**Description:**
Number of prediction requests per minute. Helps identify traffic spikes and load patterns.

**Query:**

```promql
rate(credit_model_predictions_total[1m]) * 60
```

---

## Panel 4: API Errors per Minute

**Description:**
Number of API errors (4xx and 5xx) per minute. Useful for detecting failures and instability.

**Query:**

```promql
sum(rate(http_requests_total{status=~"4..|5.."}[5m])) * 60
```

---

## Panel 5: Total API Requests per Minute

**Description:**
Total number of API requests handled per minute. Shows overall traffic load and usage spikes.

**Query:**

```promql
sum(rate(http_requests_total[1m])) * 60
```

---

## 4. Save Dashboard

* Name the dashboard:

```text
Credit Risk API Dashboard
```

* Click **Save Dashboard**

---

## Expected Outcome

The dashboard will display:

* API traffic trends
* Request volume
* Latency distribution
* Error rates

This helps monitor system health and supports **AIOps-driven incident detection**.

---

**These metrics are used by Prometheus alert rules to detect anomalies and trigger AIOps-based incident analysis and remediation.**

---


# Project Workflow 

The platform follows an end-to-end workflow integrating ML, monitoring, and AIOps automation:

```text
User → FastAPI API → ML Model Prediction → Prometheus Metrics
→ Alertmanager → AIOps Engine → MongoDB (incident storage)
→ Self-Healing / CI-CD Trigger → AWS ECS Deployment
```

### Workflow Explanation

1. User sends a request to the FastAPI `/predict` endpoint
2. The ML model generates a credit risk prediction
3. Prometheus collects metrics such as latency and request count
4. Alertmanager evaluates alert rules and triggers alerts
5. AIOps module analyzes the alert:

   * Classifies severity
   * Generates root cause analysis (RCA)
   * Suggests or applies fixes
6. Incident details are stored in MongoDB
7. Known issues are auto-resolved using stored solutions
8. If needed, Jenkins triggers CI/CD and updates ECS services

---

# API Endpoints 

The platform exposes the following key API endpoints:

### Health Check

```http
GET /health
```

Checks if the API service is running.

---

### Credit Risk Prediction

```http
POST /predict
```

Predicts the credit risk for a borrower.

**Request Body:**

```json
{
  "borrower_id": "B001"
}
```

---

### AIOps Incident Analysis

```http
POST /incident/analyze
```

Processes alerts from Alertmanager and performs:

* severity classification
* root cause analysis
* self-healing actions

---

# Future Improvements 

The following enhancements can further improve the platform:

* Deploy using **Kubernetes (EKS)** for better scalability
* Implement **advanced anomaly detection models** instead of rule-based alerts
* Add **auto-scaling policies** based on traffic and system load
* Introduce **role-based access control (RBAC)** for secure access
* Enable **multi-region deployment** for high availability
* Improve AIOps with **feedback loops and reinforcement learning**
* Integrate **centralized logging (ELK stack)** for deeper observability

---


