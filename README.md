#  - Tenderd - DevOps Assignment
# Tenderd-DevOps-Assignement-Docmentation
## Overview
This services is a microservices-based application designed to manage and streamline various services through a unified platform. The primary objective of this project is to implement a robust CI/CD pipeline, deploy the microservices to a Kubernetes cluster, and integrate monitoring and logging solutions to ensure the application's performance and reliability.

This documentation outlines the project structure, CI/CD pipeline, deployment process, and the integration of GCP services for additional functionality.

## Project Repositories
The project is divided into two repositories:

### Microservices Repository: 
Contains the source code for the microservices.
* Repository: [Tenderd-DevOps-Assignement-1](https://github.com/ahmedamsoliman-1/Tenderd-DevOps-Assignement-1)
* Structure:
```
Tenderd-DevOps-Assignement-1
├── frontend-svc
│   ├── Dockerfile
│   ├── node_modules
│   ├── package.json
│   ├── package-lock.json
│   ├── src
│   ├── tests
├── order-svc
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── src
├── user-svc
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── src
├── docker-compose.yaml
├── README.md
```

### Infrastructure Repository:
Contains the infrastructure as code (IaC) for deploying the microservices to Kubernetes.
* Repository: [Tenderd-DevOps-Assignement-Infra-1](https://github.com/ahmedamsoliman-1/Tenderd-DevOps-Assignement-Infra-1)
* Structure:
```
Tenderd-DevOps-Assignement-Infra-1
├── helm-charts
│   ├── frontend-svc-chart
│   ├── templates
│   ├── values.yaml
├── terraform
│   ├── dev
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   ├── variables.tf
├── k8-status.sh
├── README.md

```


## CI/CD Pipeline
The CI/CD pipeline is implemented using GitHub Actions, GCP, Terraform and Docker. 
The pipeline performs the following tasks:
### Tenderd-DevOps-Assignement-1: 
![Repo One](repo-1.png)
#### Deployment Process:
- Code Checkout: Retrieves the latest code from the repository.
- Docker Buildx Setup: Configures Docker Buildx for multi-platform builds.
- Docker Hub Login: Authenticates with Docker Hub using credentials stored in GitHub Secrets.
- Dependency Installation and Testing: Installs dependencies and runs tests for each microservice.
- Docker Image Build and Push: Builds Docker images for each microservice and pushes them to Docker Hub.
#### Github Actions (3):
##### 1- tenderd-build-push-images-hub
```
name: CI

on:
  push:
    branches:
      - dev-1
  pull_request:
    branches:
      - main

jobs:
  btenderd-build-push-images-hub:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - reset of step ...
```
##### tenderd-close-stale-issues
```
name: tenderd-close-stale-issues

on:
  schedule:
    - cron: '30 1 * * *'

jobs:
  tenderd-close-stale-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue is stale because it has been open 30 days with no activity. Remove stale label or comment or this will be closed in 5 days.'
          days-before-stale: 30
          days-before-close: 5
```
##### tenderd-apply-branch-protection
```
name: tenderd-apply-branch-protection

on:
  push:
    branches:
      - main

jobs:
  tenderd-apply-branch-protection:
    runs-on: ubuntu-latest

    steps:
    - name: Apply branch protection rules
      run: |
        echo "Applying relaxed branch protection rules to ${{ github.repository }}"

        curl ...
      env:
        MY_GITHUB_PAT: ${{ secrets.TENDERD_TOKEN }}
```

### Tenderd-DevOps-Assignement-Infra-1: 
![Repo One](repo-2.png)
#### Deployment Process:
- The deployment process uses Helm charts and Terraform to manage Kubernetes resources and GCP infrastructure.
- Terraform: Manages GCP resources, such as creating a GKE cluster and provisioning necessary infrastructure.
- Helm Charts: Define Kubernetes resources for each microservice.
```
Frontend-svc-chart example:
# Chart.yaml
apiVersion: v2
name: frontend-svc
description: A Helm chart for Kubernetes
version: 0.1.0
appVersion: 1.16.0

```
```
terraform statment to deploy resrouce example: 
provider "google" {
  project = var.project
  region  = var.region
}

resource "google_container_cluster" "primary" {
  name     = "primary-cluster"
  location = var.region

  node_config {
    machine_type = "e2-medium"
  }
}
```

#### Github Actions (5):
##### deploy-upgrade-helm-charts-dev
```
name: tenderd-deploy-dev
run-name: ${{ github.actor }} has triggered the pipeline for to build tendered GKE kubernetes cluster and deploy/upgrade helm charts services. 

on:
  push:
    branches:
      - 'dev'

defaults:
  run:
    shell: bash
    working-directory: ./terraform/dev-gke
  
permissions:
  contents: read
  id-token: write

jobs:
  tenderd-deploy-upgrade-helm-charts-dev:
    runs-on: ubuntu-latest
    needs: deploy-gke-k8-cluster-dev
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - reset of step ...
```
##### tenderd-prevision-gke-cluster-dev
```
tenderd-prevision-gke-cluster-dev:
    runs-on: ubuntu-latest
    permissions:
      id-token: write 
      contents: read         
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Configure GCP credentials
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WORKLOAD_IDENTITY_PROVIDER }}
          create_credentials_file: true
          service_account: ${{ secrets.SA }}
          token_format: "access_token"
          access_token_lifetime: "120s"
             
      - reset of step ...
```
##### tenderd-close-stale-issues-prs
```
name: 'Close stale issues and PRs'

on:
  schedule:
    - cron: '30 1 * * *'

jobs:
  tenderd-close-stale-issues-prs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue is stale because it has been open 30 days with no activity. Remove stale label or comment or this will be closed in 5 days.'
          days-before-stale: 30
          days-before-close: 5
```
##### tenderd-apply-branch-protection:
```
name: Apply Branch Rules

on:
  push:
    branches:
      - main

jobs:
  tenderd-apply-branch-protection::
    runs-on: ubuntu-latest

    steps:
    - name: Apply branch protection rules
      run: |
        echo "Applying relaxed branch protection rules to ${{ github.repository }}"

        curl ...
          https://api.github.com/repos/${{ github.repository }}/branches/main/protection
      env:
        MY_GITHUB_PAT: ${{ secrets.TENDERD_TOKEN }}
```
##### destroy-dev
```
name: tenderd-destroy-dev
run-name: ${{ github.actor }} has triggered the pipeline for Terraform

on:
  push:
    branches:
    - 'dev'

defaults:
  run:
    shell: bash
    working-directory: ./terraform/dev-gke
permissions:
  contents: read

jobs:
  destroy-dev:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
    - name: "Checkout"
      uses: actions/checkout@v3
    - reset of step ...
```

#### Images
* Created GKE
![GKE](images/gke.png)
* Github Actions
![GKE](images/cicd.png)
![GKE](images/branch.png)
![GKE](images/pr.png)
## Monitoring
Monitoring and logging are integrated using Prometheus and Grafana for metrics, and ELK stack (Elasticsearch, Logstash, and Kibana) for logs.

## Logging
Logging is not supported yet (possibility to capture and visualize using ELK stack (Elasticsearch, Logstash, and Kibana))

## Docker Compose for Development
The docker-compose.yaml file in micro services repository is used for local development and testing. It simplifies the process of running and managing the microservices locally by defining the necessary services, networks.
- Configuration:
```
version: '3'
services:
  frontend-svc:
    build:
      context: ./frontend-svc
    ports:
      - "3000:3000"
    depends_on:
      - order-svc
      - user-svc

  order-svc:
    build:
      context: ./order-svc
    ports:
      - "3001:3001"

  user-svc:
    build:
      context: ./user-svc
    ports:
      - "3002:3002"

networks:
  default:
    driver: bridge
```
![Repo One](images/docker.png)

## Google Cloud Platform 
This services deployed in Google Cloud Platform (GCP) using Google Kubernetes Engine (GKE). This feature is integrated into the CI/CD pipeline to ensure secure and efficient deployment.
Also GCP bucket is used to host terrafom lock file, for Github Actions to keep track the status of deployed resources and to be used later to destroy resources (with GitHub Actions as well) 

## Future Enhacments
- Enhancing Logging: Integrate ELK stack for comprehensive log management.
- Security Scanning: Add security scanning tools for Docker images.
- Automated Testing: Implement additional testing stages in the CI/CD pipeline.

## Check the current services running
- Tenderd  Frontend - URL [Go](http://tendered.ahmedalimsoliman.com/)
- Grafana Dashboards for running apps and k8 ifra [Go](http://grafana.ahmedalimsoliman.com/)
- Promethues Dashboards [Go](http://prom.ahmedalimsoliman.com/)

![Repo One](images/tend.png)
