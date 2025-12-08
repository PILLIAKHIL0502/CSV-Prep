# Part 2: Infrastructure & DevOps Skills - Complete Practical Guide

## 🎯 Overview

Transform from test automation developer to DevOps-enabled QA engineer. Learn Docker, Kubernetes, Terraform, and monitoring tools that modern enterprises use.

---

## Week 1: Docker Mastery

### Day 1-2: Docker Fundamentals

#### Install Docker

```bash
# Windows/Mac: Download Docker Desktop
# https://www.docker.com/products/docker-desktop

# Linux (Ubuntu):
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
docker run hello-world
```

#### Docker Basics

```bash
# List images
docker images

# List running containers
docker ps

# List all containers
docker ps -a

# Pull an image
docker pull python:3.11

# Run a container
docker run python:3.11 python --version

# Run interactively
docker run -it python:3.11 /bin/bash

# Run in background (detached)
docker run -d -p 8080:80 nginx

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# Remove image
docker rmi <image_id>

# Clean up everything
docker system prune -a
```

### Day 3-4: Containerize Your Test Framework

**Create Dockerfile for Test Framework:**

**File: `Dockerfile`**

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy test framework
COPY . .

# Create directories for reports and screenshots
RUN mkdir -p reports screenshots logs

# Set environment variables
ENV HEADLESS=true
ENV BROWSER=chrome

# Default command: run smoke tests
CMD ["pytest", "tests/", "-m", "smoke", "--html=reports/report.html", "--self-contained-html"]
```

**Build and Run Docker Image:**

```bash
# Build image
docker build -t selenium-gxp-framework:latest .

# Run tests in container
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/screenshots:/app/screenshots \
  selenium-gxp-framework:latest

# Run with different test marker
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  selenium-gxp-framework:latest \
  pytest tests/ -m regression --html=reports/report.html

# Run interactively (for debugging)
docker run -it --rm selenium-gxp-framework:latest /bin/bash
```

### Day 5-6: Docker Compose for Multi-Service

**Scenario:** Run Selenium Grid with multiple browsers

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  # Selenium Hub
  selenium-hub:
    image: selenium/hub:4.15.0
    container_name: selenium-hub
    ports:
      - "4444:4444"
      - "4442:4442"
      - "4443:4443"
    environment:
      - SE_SESSION_REQUEST_TIMEOUT=300
      - SE_NODE_SESSION_TIMEOUT=300
    networks:
      - selenium-grid

  # Chrome Node
  chrome:
    image: selenium/node-chrome:4.15.0
    container_name: chrome-node
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
      - SE_NODE_SESSION_TIMEOUT=300
    shm_size: '2gb'
    networks:
      - selenium-grid

  # Firefox Node
  firefox:
    image: selenium/node-firefox:4.15.0
    container_name: firefox-node
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
    shm_size: '2gb'
    networks:
      - selenium-grid

  # Test Execution Service
  test-runner:
    build: .
    container_name: test-runner
    depends_on:
      - selenium-hub
      - chrome
      - firefox
    environment:
      - SELENIUM_HUB=http://selenium-hub:4444/wd/hub
      - HEADLESS=true
    volumes:
      - ./reports:/app/reports
      - ./screenshots:/app/screenshots
      - ./logs:/app/logs
    networks:
      - selenium-grid
    command: >
      sh -c "sleep 10 && 
             pytest tests/ 
             -m smoke 
             --html=reports/report.html 
             --self-contained-html"

networks:
  selenium-grid:
    driver: bridge
```

**Update conftest.py for Remote WebDriver:**

```python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

@pytest.fixture(scope="function")
def driver(request):
    """WebDriver fixture with Selenium Grid support"""
    
    selenium_hub = os.getenv('SELENIUM_HUB', None)
    
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    
    if selenium_hub:
        # Connect to Selenium Grid
        logger.info(f"Connecting to Selenium Grid: {selenium_hub}")
        driver = webdriver.Remote(
            command_executor=selenium_hub,
            options=chrome_options
        )
    else:
        # Local execution
        driver = webdriver.Chrome(options=chrome_options)
    
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()
```

**Run with Docker Compose:**

```bash
# Start Selenium Grid
docker-compose up -d selenium-hub chrome firefox

# Check grid status
open http://localhost:4444

# Run tests
docker-compose up test-runner

# View logs
docker-compose logs test-runner

# Stop everything
docker-compose down

# Cleanup volumes
docker-compose down -v
```

### Day 7: Docker Best Practices for GxP

**Multi-Stage Build (Smaller Image):**

```dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc

# Install Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget gnupg unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application
COPY . .

# Update PATH
ENV PATH=/root/.local/bin:$PATH

CMD ["pytest", "tests/", "-m", "smoke"]
```

**Tag and Version Images:**

```bash
# Build with version tag
docker build -t selenium-gxp-framework:1.0.0 .
docker build -t selenium-gxp-framework:latest .

# Tag for registry
docker tag selenium-gxp-framework:1.0.0 myregistry.com/selenium-gxp-framework:1.0.0

# Push to registry
docker push myregistry.com/selenium-gxp-framework:1.0.0
```

**Docker Validation Document (GxP Requirement):**

```markdown
# Docker Container Validation

## Container Information
- Image: selenium-gxp-framework:1.0.0
- Base Image: python:3.11-slim
- Purpose: Execute automated tests

## Validation Activities
1. ✅ Image build reproducible (Dockerfile in version control)
2. ✅ Base image from trusted source (Docker Hub official)
3. ✅ No secrets in image (verified with `docker history`)
4. ✅ Dependencies pinned (requirements.txt with versions)
5. ✅ Security scan passed (Trivy/Snyk)

## Test Results
- ✅ Container starts successfully
- ✅ Tests execute correctly
- ✅ Reports generated
- ✅ Exit codes correct (0 for pass, 1 for fail)

Validated by: [Your Name]
Date: [Date]
```

---

## Week 2: Kubernetes Basics

### Day 1-2: Kubernetes Fundamentals

#### Install Kubernetes Tools

```bash
# Install kubectl (command-line tool)
# Windows: choco install kubernetes-cli
# Mac: brew install kubectl
# Linux:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Minikube (local Kubernetes)
# Windows: choco install minikube
# Mac: brew install minikube
# Linux:
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start --driver=docker

# Verify
kubectl version
kubectl cluster-info
kubectl get nodes
```

#### Kubernetes Basic Concepts

```bash
# Namespaces (logical separation)
kubectl get namespaces
kubectl create namespace test-automation

# Pods (smallest deployable unit)
kubectl get pods -n test-automation
kubectl describe pod <pod-name> -n test-automation

# Deployments (manage replicas)
kubectl get deployments -n test-automation

# Services (networking)
kubectl get services -n test-automation

# ConfigMaps (configuration)
kubectl get configmaps -n test-automation

# Secrets (sensitive data)
kubectl get secrets -n test-automation
```

### Day 3-4: Deploy Tests to Kubernetes

**Create Kubernetes Manifests:**

**File: `k8s/namespace.yaml`**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: test-automation
  labels:
    name: test-automation
    environment: dev
```

**File: `k8s/configmap.yaml`**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-config
  namespace: test-automation
data:
  BASE_URL: "https://demo.opencart.com/"
  ENVIRONMENT: "dev"
  HEADLESS: "true"
  BROWSER: "chrome"
  IMPLICIT_WAIT: "10"
  EXPLICIT_WAIT: "20"
```

**File: `k8s/selenium-hub-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: selenium-hub
  namespace: test-automation
  labels:
    app: selenium-hub
spec:
  replicas: 1
  selector:
    matchLabels:
      app: selenium-hub
  template:
    metadata:
      labels:
        app: selenium-hub
    spec:
      containers:
      - name: selenium-hub
        image: selenium/hub:4.15.0
        ports:
        - containerPort: 4444
        - containerPort: 4442
        - containerPort: 4443
        env:
        - name: SE_SESSION_REQUEST_TIMEOUT
          value: "300"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: selenium-hub
  namespace: test-automation
spec:
  selector:
    app: selenium-hub
  ports:
  - name: web
    port: 4444
    targetPort: 4444
  - name: publish
    port: 4442
    targetPort: 4442
  - name: subscribe
    port: 4443
    targetPort: 4443
  type: ClusterIP
```

**File: `k8s/chrome-node-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chrome-node
  namespace: test-automation
  labels:
    app: chrome-node
spec:
  replicas: 2  # Scale up/down based on load
  selector:
    matchLabels:
      app: chrome-node
  template:
    metadata:
      labels:
        app: chrome-node
    spec:
      containers:
      - name: chrome-node
        image: selenium/node-chrome:4.15.0
        env:
        - name: SE_EVENT_BUS_HOST
          value: "selenium-hub"
        - name: SE_EVENT_BUS_PUBLISH_PORT
          value: "4442"
        - name: SE_EVENT_BUS_SUBSCRIBE_PORT
          value: "4443"
        - name: SE_NODE_MAX_SESSIONS
          value: "3"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: dshm
          mountPath: /dev/shm
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory
          sizeLimit: 2Gi
```

**File: `k8s/test-runner-job.yaml`**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-runner
  namespace: test-automation
spec:
  template:
    metadata:
      labels:
        app: test-runner
    spec:
      restartPolicy: Never
      containers:
      - name: test-runner
        image: selenium-gxp-framework:1.0.0
        command: ["pytest"]
        args: 
          - "tests/"
          - "-m"
          - "smoke"
          - "--html=reports/report.html"
          - "--self-contained-html"
        env:
        - name: SELENIUM_HUB
          value: "http://selenium-hub:4444/wd/hub"
        envFrom:
        - configMapRef:
            name: test-config
        volumeMounts:
        - name: reports
          mountPath: /app/reports
        - name: screenshots
          mountPath: /app/screenshots
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: reports
        persistentVolumeClaim:
          claimName: test-reports-pvc
      - name: screenshots
        persistentVolumeClaim:
          claimName: test-screenshots-pvc
  backoffLimit: 0  # Don't retry failed tests automatically
```

**File: `k8s/persistent-volume.yaml`**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-reports-pvc
  namespace: test-automation
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-screenshots-pvc
  namespace: test-automation
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```

**Deploy to Kubernetes:**

```bash
# Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/selenium-hub-deployment.yaml
kubectl apply -f k8s/chrome-node-deployment.yaml
kubectl apply -f k8s/persistent-volume.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=selenium-hub -n test-automation --timeout=60s
kubectl wait --for=condition=ready pod -l app=chrome-node -n test-automation --timeout=60s

# Run tests
kubectl apply -f k8s/test-runner-job.yaml

# Check job status
kubectl get jobs -n test-automation
kubectl describe job test-runner -n test-automation

# View logs
kubectl logs -n test-automation -l app=test-runner --follow

# Get reports (copy from pod)
POD_NAME=$(kubectl get pods -n test-automation -l app=test-runner -o jsonpath='{.items[0].metadata.name}')
kubectl cp test-automation/$POD_NAME:/app/reports ./reports

# Cleanup
kubectl delete job test-runner -n test-automation
```

### Day 5-7: Kubernetes for Test Automation

**CronJob for Scheduled Tests:**

**File: `k8s/scheduled-tests-cronjob.yaml`**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-regression
  namespace: test-automation
spec:
  schedule: "0 2 * * *"  # Every day at 2 AM
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
          - name: test-runner
            image: selenium-gxp-framework:1.0.0
            command: ["pytest"]
            args:
              - "tests/"
              - "-m"
              - "regression"
              - "--html=reports/regression_report.html"
            env:
            - name: SELENIUM_HUB
              value: "http://selenium-hub:4444/wd/hub"
            envFrom:
            - configMapRef:
                name: test-config
```

**Scale Selenium Grid:**

```bash
# Scale Chrome nodes up
kubectl scale deployment chrome-node --replicas=5 -n test-automation

# Scale down
kubectl scale deployment chrome-node --replicas=1 -n test-automation

# Auto-scaling (Horizontal Pod Autoscaler)
kubectl autoscale deployment chrome-node \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n test-automation
```

---

## Week 3: Terraform Basics

### Day 1-2: Terraform Fundamentals

#### Install Terraform

```bash
# Windows: choco install terraform
# Mac: brew install terraform
# Linux:
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Verify
terraform version
```

### Day 3-5: Create Test Infrastructure with Terraform

**File: `terraform/main.tf`**

```hcl
# Configure AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "dev"
}

# VPC for Test Environment
resource "aws_vpc" "test_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "test-automation-vpc"
    Environment = var.environment
  }
}

# Subnet
resource "aws_subnet" "test_subnet" {
  vpc_id                  = aws_vpc.test_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "test-automation-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "test_igw" {
  vpc_id = aws_vpc.test_vpc.id

  tags = {
    Name = "test-automation-igw"
  }
}

# Route Table
resource "aws_route_table" "test_rt" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.test_igw.id
  }

  tags = {
    Name = "test-automation-rt"
  }
}

# Associate Route Table
resource "aws_route_table_association" "test_rta" {
  subnet_id      = aws_subnet.test_subnet.id
  route_table_id = aws_route_table.test_rt.id
}

# Security Group for Test Server
resource "aws_security_group" "test_server_sg" {
  name        = "test-server-sg"
  description = "Security group for test execution server"
  vpc_id      = aws_vpc.test_vpc.id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict in production!
  }

  # Selenium Hub
  ingress {
    from_port   = 4444
    to_port     = 4444
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "test-server-sg"
  }
}

# EC2 Instance for Test Execution
resource "aws_instance" "test_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t3.medium"
  subnet_id     = aws_subnet.test_subnet.id
  
  vpc_security_group_ids = [aws_security_group.test_server_sg.id]
  
  key_name = "my-test-key"  # Create this key pair first

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              service docker start
              usermod -a -G docker ec2-user
              
              # Install Docker Compose
              curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              
              # Pull Selenium Grid images
              docker pull selenium/hub:4.15.0
              docker pull selenium/node-chrome:4.15.0
              EOF

  tags = {
    Name        = "test-execution-server"
    Environment = var.environment
    Purpose     = "automated-testing"
  }
}

# Outputs
output "test_server_public_ip" {
  value = aws_instance.test_server.public_ip
  description = "Public IP of test server"
}

output "selenium_hub_url" {
  value = "http://${aws_instance.test_server.public_ip}:4444"
  description = "Selenium Hub URL"
}
```

**Deploy with Terraform:**

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan (dry-run)
terraform plan

# Apply (create infrastructure)
terraform apply

# View outputs
terraform output

# SSH to server
ssh -i my-test-key.pem ec2-user@<public-ip>

# Destroy infrastructure
terraform destroy
```

---

## Week 4: Monitoring & Observability

### Day 1-3: Grafana Dashboard

**Install Grafana with Docker:**

```bash
# Run Grafana
docker run -d \
  --name=grafana \
  -p 3000:3000 \
  grafana/grafana-oss

# Access: http://localhost:3000
# Default: admin/admin
```

**Create Test Metrics Dashboard:**

```python
# File: utils/metrics_collector.py

import json
import requests
from datetime import datetime

class MetricsCollector:
    """Collect and send test metrics to monitoring system"""
    
    def __init__(self, prometheus_url=None):
        self.prometheus_url = prometheus_url or "http://localhost:9091"
    
    def record_test_result(self, test_name, status, duration, requirement_id=None):
        """Record test execution result"""
        metric = {
            "test_name": test_name,
            "status": status,  # pass/fail
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "requirement_id": requirement_id
        }
        
        # Send to Prometheus Pushgateway
        self._push_to_prometheus(metric)
    
    def _push_to_prometheus(self, metric):
        """Push metrics to Prometheus"""
        # Implementation depends on your setup
        pass
```

### Day 4-7: Complete Monitoring Setup

**File: `docker-compose-monitoring.yml`**

```yaml
version: '3.8'

services:
  # Prometheus (metrics storage)
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    networks:
      - monitoring

  # Grafana (visualization)
  grafana:
    image: grafana/grafana-oss:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - monitoring

  # Pushgateway (receive metrics)
  pushgateway:
    image: prom/pushgateway:latest
    container_name: pushgateway
    ports:
      - "9091:9091"
    networks:
      - monitoring

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:
    driver: bridge
```

---

## 📊 Week 5-6: Practice Projects

### Project 1: Containerize Your Framework
- [ ] Create Dockerfile
- [ ] Build and test image
- [ ] Push to Docker Hub
- [ ] Document in README

### Project 2: Deploy to Kubernetes
- [ ] Create K8s manifests
- [ ] Deploy to Minikube
- [ ] Run tests successfully
- [ ] Collect reports

### Project 3: Infrastructure as Code
- [ ] Write Terraform config
- [ ] Deploy test environment
- [ ] Run tests on cloud
- [ ] Destroy infrastructure

### Project 4: Monitoring Setup
- [ ] Set up Grafana
- [ ] Create dashboard
- [ ] Collect test metrics
- [ ] Share dashboard screenshot

---

## ✅ Skills Checklist

After completing this guide:

- [ ] Can explain Docker vs VM
- [ ] Can write Dockerfile
- [ ] Can use docker-compose
- [ ] Understand Kubernetes architecture
- [ ] Can deploy pods/deployments
- [ ] Can write K8s manifests
- [ ] Know basic kubectl commands
- [ ] Can write Terraform config
- [ ] Can provision cloud infrastructure
- [ ] Can set up monitoring
- [ ] Can create Grafana dashboard

---

## 🎯 Interview Readiness

**Q: Why use Docker for testing?**
A: "Consistency - tests run same everywhere. Isolation - no conflicts. Scalability - easy to scale. Reproducibility - infrastructure as code."

**Q: What's difference between Docker and Kubernetes?**
A: "Docker runs containers on single host. Kubernetes orchestrates containers across multiple hosts with load balancing, scaling, and self-healing."

**Q: Have you used infrastructure as code?**
A: "Yes, I use Terraform to provision test environments on AWS. Infrastructure is versioned in Git, can be created/destroyed on demand, ensures consistency."

---

**Next: Part 3 - Security Testing Guide**
