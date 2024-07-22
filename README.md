# ServiceHub - Tenderd - DevOps Assignment
# Tenderd-DevOps-Assignement-Docmentation
## Overview
ServiceHub is a microservices-based application designed to manage and streamline various services through a unified platform. The primary objective of this project is to implement a robust CI/CD pipeline, deploy the microservices to a Kubernetes cluster, and integrate monitoring and logging solutions to ensure the application's performance and reliability.

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
##### 1- build-push-images-hub
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
  build-push-images-hub:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract branch name
        id: extract_version
        run: |
          BRANCH_NAME="${GITHUB_REF#refs/heads/}"
          # Handle PRs and replace slashes
          if [[ $GITHUB_REF == refs/pull/* ]]; then
            BRANCH_NAME="pr-${GITHUB_REF##*/}"
          fi
          # Sanitize branch name for Docker tags
          BRANCH_NAME=$(echo $BRANCH_NAME | sed 's/[^a-zA-Z0-9._-]/_/g')
          echo "BRANCH_NAME=$BRANCH_NAME" >> $GITHUB_ENV

      - name: Install dependencies for frontend service
        run: |
          cd ./frontend-svc
          npm install

      - name: Run tests for frontend service
        run: |
          cd ./frontend-svc
          npm test

      - name: Install dependencies for order service
        run: |
          cd ./order-svc
          npm install

      - name: Run tests for order service
        run: |
          cd ./order-svc
          npm test

      - name: Install dependencies for user service
        run: |
          cd ./user-svc
          npm install

      - name: Run tests for user service
        run: |
          cd ./user-svc
          npm test 

      - name: Build and push Docker images
        if: success()
        run: |
          docker buildx build --platform linux/amd64,linux/arm64 -t ${{ secrets.DOCKER_USERNAME }}/tenderd-devops-frontend-svc:latest -t ${{ secrets.DOCKER_USERNAME }}/frontend-svc:latest --push ./frontend-svc
          docker buildx build --platform linux/amd64,linux/arm64 -t ${{ secrets.DOCKER_USERNAME }}/tenderd-devops-order-svc:latest -t ${{ secrets.DOCKER_USERNAME }}/order-svc:latest --push ./order-svc
          docker buildx build --platform linux/amd64,linux/arm64 -t ${{ secrets.DOCKER_USERNAME }}/tenderd-devops-user-svc:latest -t ${{ secrets.DOCKER_USERNAME }}/user-svc:latest --push ./user-svc
```
##### close-stale-issues
```
name: 'Close stale issues and PRs'

on:
  schedule:
    - cron: '30 1 * * *'

jobs:
  close-stale-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue is stale because it has been open 30 days with no activity. Remove stale label or comment or this will be closed in 5 days.'
          days-before-stale: 30
          days-before-close: 5
```
##### apply-branch-protection
```
name: Apply Branch Rules

on:
  push:
    branches:
      - main

jobs:
  apply-branch-protection:
    runs-on: ubuntu-latest

    steps:
    - name: Apply branch protection rules
      run: |
        echo "Applying relaxed branch protection rules to ${{ github.repository }}"

        curl -X PUT \
          -H "Authorization: token ${{ secrets.TENDERD_TOKEN }}" \
          -H "Accept: application/vnd.github.v3+json" \
          -d '{
            "required_status_checks": null,
            "enforce_admins": false,
            "required_pull_request_reviews": null,
            "restrictions": null,
            "required_linear_history": false,
            "allow_force_pushes": false,
            "allow_deletions": false
          }' \
          https://api.github.com/repos/${{ github.repository }}/branches/main/protection
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
  deploy-upgrade-helm-charts-dev:
    runs-on: ubuntu-latest
    needs: deploy-gke-k8-cluster-dev
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Configure GCP credentials (reuse existing step)
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WORKLOAD_IDENTITY_PROVIDER }}
          create_credentials_file: true
          service_account: ${{ secrets.SA }}
          token_format: "access_token"
          access_token_lifetime: "120s"

      - name: Install gcloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          version: 'latest'

      - name: Install gke-gcloud-auth-plugin
        run: |
          gcloud components install gke-gcloud-auth-plugin

      - name: Get GKE Cluster Credentials
        run: |
          gcloud container clusters get-credentials ${{ secrets.DEV_CLUSTER_NAME }} --zone us-east1-b --project ${{ secrets.GCP_PROJECT }}

      - name: Install Helm (if not already present)
        run: |
          # Check if Helm is installed
          if ! helm version >/dev/null 2>&1; then
            curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
            bash get_helm.sh
          fi
          helm version

      - name: Deploy Helm Charts - Frontend SVC
        run: |
          cd ../../helm-charts/frontend-svc-chart
          helm upgrade --install frontend-release . --namespace tendered --create-namespace -f values.yaml

      - name: Deploy Helm Charts - User SVC
        run: |
          cd ../../helm-charts/user-svc-chart
          helm upgrade --install user-release . --namespace tendered --create-namespace -f values.yaml

      - name: Deploy Helm Charts - Order SVC
        run: |
          cd ../../helm-charts/order-svc-chart
          helm upgrade --install order-release . --namespace tendered --create-namespace -f values.yaml
      
      - name: Deploy Extra services - Monitoring - Ingress
        run: |
          cd ../../helm-charts/extra/grafana
          chmod +x deploy.sh
          ./deploy.sh

          cd ../prometheus
          chmod +x deploy.sh
          ./deploy.sh

          cd ../ingress-nginx
          chmod +x deploy.sh
          ./deploy.sh
```
##### deploy-gke-k8-cluster-dev
```
deploy-gke-k8-cluster-dev:
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
      - name: Echo environment variables
        run: printenv
      - name: Setup Terraform with specified version on the runner
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.7.0
          terraform_wrapper: true
             
      - name: Terraform init
        id: init
        run: terraform init
      
      - name: Terraform Format
        id: fmt
        run: terraform fmt -recursive -write=true 

      - name: Terraform validate
        id: validate
        run: terraform validate

      - name: Terraform plan
        id: plan
        run: terraform plan 
        continue-on-error: true

      - name: Terraform Plan Status
        if: steps.plan.outcome == 'failure'
        run: exit 1

      - name: Terraform Apply
        run: terraform apply -auto-approve
```
##### close-stale-issues
```
name: 'Close stale issues and PRs'

on:
  schedule:
    - cron: '30 1 * * *'

jobs:
  close-stale-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue is stale because it has been open 30 days with no activity. Remove stale label or comment or this will be closed in 5 days.'
          days-before-stale: 30
          days-before-close: 5
```
##### apply-branch-protection
```
name: Apply Branch Rules

on:
  push:
    branches:
      - main

jobs:
  apply-branch-protection:
    runs-on: ubuntu-latest

    steps:
    - name: Apply branch protection rules
      run: |
        echo "Applying relaxed branch protection rules to ${{ github.repository }}"

        curl -X PUT \
          -H "Authorization: token ${{ secrets.TENDERD_TOKEN }}" \
          -H "Accept: application/vnd.github.v3+json" \
          -d '{
            "required_status_checks": null,
            "enforce_admins": false,
            "required_pull_request_reviews": null,
            "restrictions": null,
            "required_linear_history": false,
            "allow_force_pushes": false,
            "allow_deletions": false
          }' \
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
    - name: Configure GCP credentials
      id: auth
      uses: google-github-actions/auth@v2
      with:
        workload_identity_provider: ${{ secrets.WORKLOAD_IDENTITY_PROVIDER }}
        create_credentials_file: true
        service_account: ${{ secrets.SA }}
        token_format: "access_token"
        access_token_lifetime: "120s"
    - name: Echo stuff
      run: printenv
    - name: Setup Terraform with specified version on the runner
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: 1.7.0
        terraform_wrapper: true

    - name: Terraform init
      id: init
      run: terraform init

    - name: Terraform Destroy
      run: terraform destroy -auto-approve


```
#### Images
* Created GKE
![GKE](images/gke.png)
* Github Actions
![GKE](images/github.png)
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
- Tenderd ServiceHub Frontend - URL : 
- Tenderd user services - URL : 
- Tenderd order services - URL : 
- Grafana Dashboards for running apps and k8 ifra
- Promethues Dashboards

