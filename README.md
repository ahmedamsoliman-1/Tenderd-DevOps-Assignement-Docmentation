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
├── README.md
├── docker-compose.yaml
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
├── update_git.sh
```

### Infrastructure Repository:
Contains the infrastructure as code (IaC) for deploying the microservices to Kubernetes.
* Repository: [Tenderd-DevOps-Assignement-Infra-1](https://github.com/ahmedamsoliman-1/Tenderd-DevOps-Assignement-Infra-1)
* Structure:
```
Tenderd-DevOps-Assignement-Infra-1
├── README.md
├── helm-charts
│   ├── frontend-svc-chart
│   ├── templates
│   ├── values.yaml
├── k8-status.sh
├── terraform
│   ├── dev
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   ├── variables.tf
├── update_git.sh

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

### Tenderd-DevOps-Assignement-Infra-1: 
![Repo One](repo-2.png)
#### Deployment Process:
- The deployment process uses Helm charts and Terraform to manage Kubernetes resources and GCP infrastructure.
- Terraform: Manages GCP resources, such as creating a GKE cluster and provisioning necessary infrastructure.
- Helm Charts: Define Kubernetes resources for each microservice.

## Monitoring
Monitoring and logging are integrated using Prometheus and Grafana for metrics, and ELK stack (Elasticsearch, Logstash, and Kibana) for logs.

## Logging
Logging is not supported yet (possibility to capture and visualize using ELK stack (Elasticsearch, Logstash, and Kibana))

## Google Cloud Platform 
This services deployed in Google Cloud Platform (GCP) using Google Kubernetes Engine (GKE). This feature is integrated into the CI/CD pipeline to ensure secure and efficient deployment.
Also GCP bucket is used to host terrafom lock file, for Github Actions to keep track the status of deployed resources and to be used later to destroy resources (with GitHub Actions as well) 

## Check the current services running
* Tenderd ServiceHub Frontend - URL : 
* Tenderd user services - URL : 
* Tenderd order services - URL : 
- Grafana Dashboards for running apps and k8 ifra
- Promethues Dashboards

