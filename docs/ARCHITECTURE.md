# Architecture Deep Dive

## System Overview

This document provides detailed technical architecture of the AI-Augmented MLOps Platform.

## Component Breakdown

### 1. Control Plane (GCP Cluster)
- **Purpose**: Centralized management and platform services
- **Resources**: e2-small (2 vCPU, 4GB RAM)
- **Services**:
  - ArgoCD: GitOps controller managing both clusters
  - MLflow: Model registry and experiment tracking
  - Prometheus: Multi-cluster metrics collection
  - Grafana: Visualization and dashboards
  - Alertmanager: Alert routing and webhook triggers

### 2. Data Plane (k3d On-Premises)
- **Purpose**: ML workload execution (edge simulation)
- **Resources**: Docker containers (k3d cluster)
- **Services**:
  - iris-classifier: Scikit-learn model inference server
  - Future: Additional ML models, KServe deployments

### 3. AI Intelligence Layer
- **Purpose**: Operational intelligence and automation
- **Technology**: Google Gemini 2.5 Flash Lite API
- **Integration Points**:
  - GitHub Actions workflows
  - Prometheus alert webhooks
  - MLflow metrics analysis

## Network Architecture

### Hybrid Connectivity (Tailscale VPN)
- **GCP Node**: 100.x.x.x (Tailscale IP)
- **Windows Node**: 100.x.x.x (Tailscale IP)
- **Benefit**: Secure, encrypted communication without public exposure

### Port Mappings (k3d)
- 6550 → 6443 (K8s API)
- 8080 → 80 (HTTP Ingress)
- 30808 → 30808 (iris-classifier inference)
- 30900 → 30900 (Prometheus scraping)

## Data Flow

### ML Pipeline Flow
1. Developer pushes code to GitHub
2. GitHub Actions triggers CI/CD pipeline
3. Model trains → logs to MLflow (GCP)
4. Container builds → scans → pushes to GHCR
5. GitOps update → ArgoCD syncs to k3d cluster
6. Model serves on k3d → Prometheus scrapes metrics
7. Alerts trigger → Gemini analyzes → GitHub Issue created

### Monitoring Flow
- Prometheus (GCP) scrapes:
  - GCP cluster metrics (in-cluster)
  - k3d cluster metrics (via Tailscale IP:30808)
- Grafana visualizes unified view
- Alertmanager routes to AI workflows

## Technology Choices

### Why k3s?
- Lightweight (perfect for edge/on-prem)
- Production-ready (certified Kubernetes)
- Easy to set up and manage

### Why ArgoCD?
- GitOps best practice
- Multi-cluster support
- Automated sync and rollback

### Why Gemini 2.5 Flash Lite?
- Free tier (cost-effective)
- Fast inference (<2s responses)
- Good reasoning for operational tasks

## Scalability

### Horizontal Scaling
- Add more k3d agents for ML workloads
- Add more GCP nodes for platform services
- Prometheus federation for metric aggregation

### Vertical Scaling
- Upgrade GCP instance (e2-small → e2-medium)
- Increase k3d resource limits
- Optimize model serving (batching, caching)

## Security Architecture

### Network Security
- Tailscale: Zero-trust mesh VPN
- GCP firewall: Only port 6443 exposed
- k3d: Runs on localhost, no direct internet exposure

### Application Security
- Non-root containers
- Multi-stage builds (minimal images)
- Automated CVE scanning
- Secret management (GitHub Secrets)

### Access Control
- ArgoCD RBAC
- Kubernetes RBAC
- Service account least privilege

## Disaster Recovery

### Backup Strategy
- GitOps: All config in Git (instant recovery)
- MLflow: Model artifacts persisted to PVC
- Prometheus: Metrics retention 7 days

### Recovery Procedures
1. GCP node failure: Recreate from IaC + ArgoCD sync
2. k3d cluster failure: Recreate cluster + ArgoCD re-deploys
3. Data loss: Restore MLflow PV from backup

## Cost Optimization

### Current Costs
- GCP e2-small: ~$13/month
- Tailscale: $0 (free tier)
- Gemini API: $0 (free tier, <2M tokens/month)
- GitHub: $0 (public repos)
- **Total: $13/month**

### Further Optimization
- Use preemptible GCP instances (70% savings)
- Spot instances for non-critical workloads
- Aggressive resource limits
- Horizontal pod autoscaling
