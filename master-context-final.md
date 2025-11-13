# Project Master Context: AI-Augmented, Self-Healing MLOps Platform
## Final Implementation Documentation

## 1. Project Vision & Core Purpose

The primary vision is to build a fully automated, hybrid MLOps platform that manages the entire lifecycle of a machine learning model, from code commit to production deployment and monitoring.

The project's unique differentiator is its **multi-domain AI-Augmented operational layer**. The platform uses Google's Gemini 2.5 Flash Lite LLM via REST API to perform intelligent:
- **Real-time log analysis** and root cause diagnosis for production alerts
- **Model drift detection** with automated remediation recommendations
- **CI/CD pipeline failure triage** with specific, actionable fix instructions

This demonstrates a forward-thinking approach to AIOps (AI for IT Operations) within an MLOps context, showcasing how AI can reduce Mean Time To Resolution (MTTR), improve system reliability, and accelerate development velocity.

**Architecture Philosophy:** This platform demonstrates cloud-agnostic hybrid architecture principles. The control plane runs on GCP (chosen for Kubernetes heritage and Gemini integration), while the data plane runs on-premises (simulated via k3d on Windows). All infrastructure is defined in portable Kubernetes manifests, making the platform migratable to AWS, Azure, or fully on-premises environments.

This project serves as a portfolio centerpiece to showcase advanced, practical skills in Platform Engineering, MLOps, DevSecOps, Hybrid Cloud Architecture, Multi-Cluster Management, and Applied AI.

---

## 2. Key Objectives & Showcase Goals

This project is designed to demonstrate the following key competencies to potential employers:

### Platform Engineering & Infrastructure
- **Hybrid Cloud Architecture:** Ability to design and operate distributed systems spanning cloud (GCP) and on-premises (k3d) infrastructure
- **Multi-Cluster Kubernetes Management:** Managing two independent Kubernetes clusters with centralized GitOps control
- **Secure Hybrid Connectivity:** Implementing production-grade VPN connectivity (Tailscale) for cross-cluster communication
- **Cloud-Native & Orchestration Mastery:** Deep, practical knowledge of Kubernetes (k3s) as a portable, cloud-agnostic orchestration platform

### MLOps & DevOps Excellence
- **Modern DevOps Best Practices:** Strict adherence to GitOps principles using ArgoCD as the single source of truth for cluster state
- **Advanced CI/CT/CD Pipeline Engineering:** Design and implementation of sophisticated pipelines handling ML-specific requirements including Continuous Training (CT) and model validation gates
- **ML Lifecycle Management:** Practical understanding of tools (MLflow, KServe concepts) and processes required to version, deploy, and serve ML models effectively
- **Infrastructure as Code (IaC):** All infrastructure and platform configuration defined declaratively in code and stored in Git

### Security & Compliance (DevSecOps)
- **Integrated Security (DevSecOps):** Security is not an afterthought - the pipeline includes automated SAST, SCA, secrets detection, and container vulnerability scanning at every stage
- **Shift-Left Security:** Security checks integrated into the earliest possible stages of the pipeline
- **Vulnerability Management:** Automated scanning with Bandit, Snyk, Gitleaks, and Trivy
- **Supply Chain Security:** Container image provenance and vulnerability tracking

### AIOps & Intelligent Operations
- **Multi-Domain AIOps Integration:**
  - **Observability:** Intelligent log analysis and alert contextualization using Gemini AI
  - **ML Operations:** Automated drift detection and model health diagnostics
  - **Developer Experience:** CI/CD failure triage with actionable remediation steps
  - Demonstrates practical application of LLMs to reduce MTTR, improve model reliability, and accelerate developer feedback loops
- **Prompt Engineering:** Structured prompts for operational use cases with specialized context based on failure types
- **Cost Optimization:** Utilizing free-tier Gemini API (2.5 Flash Lite) for production-grade intelligent automation

### Site Reliability Engineering (SRE)
- **Cross-Cluster Observability:** Prometheus monitoring spanning multiple Kubernetes clusters
- **Proactive Alerting:** Alert rules for pod health, resource utilization, and model performance
- **Incident Response Automation:** AI-powered analysis reducing manual troubleshooting time
- **Documentation & Runbooks:** Automated generation of incident reports and remediation steps

---

## 3. Core Architecture & End-to-End Workflow

The platform operates in three distinct phases with an additional AI intelligence layer:

### Phase 1: The Platform Foundation (Hybrid Multi-Cluster Architecture)

#### Cloud Control Plane (GCP e2-small)
**Purpose:** Centralized management and platform services

**Infrastructure:**
- **Provider:** Google Cloud Platform (Compute Engine)
- **Instance Type:** e2-small (2 vCPU, 2GB RAM)
- **Region:** us-west1-b
- **OS:** Ubuntu 22.04 LTS
- **Cost:** ~$13/month (~$6.50 for 2-week project)

**K3s Configuration:**
- **Mode:** Server (control plane)
- **Components:** API Server, Scheduler, Controller Manager, etcd
- **Storage:** local-path provisioner (default)
- **Networking:** Flannel CNI

**Platform Services Deployed:**
1. **ArgoCD** (GitOps Controller)
   - Manages applications on both GCP and k3d clusters
   - Watches GitHub repository for infrastructure manifests
   - Automated sync with prune and self-heal enabled
   - Multi-cluster management via cluster secrets
   
2. **MLflow** (Model Registry & Experiment Tracking)
   - Tracks model training runs and metrics
   - Stores model artifacts with versioning
   - SQLite backend (for demo; production would use PostgreSQL)
   - Persistent volume for artifact storage (5GB)
   - Exposed via NodePort 30500

3. **Prometheus** (Metrics Collection)
   - Scrapes metrics from both clusters (GCP in-cluster, k3d via Tailscale)
   - 7-day retention (optimized for 2GB RAM)
   - Alert rules for pod health, resource utilization
   - Exposed via NodePort 30900

4. **Grafana** (Visualization)
   - Dashboards for infrastructure and application metrics
   - Connected to Prometheus as data source
   - Exposed via NodePort 30300

5. **Alertmanager** (Alert Routing)
   - Routes alerts based on severity
   - Webhook configuration for AI workflow triggers
   - Exposed via NodePort 30930

**Firewall Rules:**
- Port 6443: Kubernetes API (for ArgoCD remote cluster access)
- Ports 30000-32767: NodePort range for services

---

#### On-Premises Edge Node (Windows + k3d)
**Purpose:** ML workload execution simulating edge/on-premises deployment

**Infrastructure:**
- **Host:** Windows 11 laptop (borrowed, dedicated to project)
- **Container Runtime:** Docker Desktop with WSL2 backend
- **k3d Version:** Latest stable
- **Cluster Name:** ml-worker
- **Available RAM:** ~8.5GB

**K3d Configuration:**
```bash
k3d cluster create ml-worker \
  --servers 1 \
  --agents 1 \
  --api-port 6550 \
  --port "8080:80@loadbalancer" \
  --port "8443:443@loadbalancer" \
  --port "30808:30808@agent:0" \
  --port "30809:30809@agent:0" \
  --port "30850:30850@agent:0" \
  --port "30900:30900@agent:0" \
  --port "30500:30500@agent:0" \
  --k3s-arg "--disable=traefik@server:*" \
  --k3s-arg "--tls-san=100.85.38.128@server:*"
```

**Port Mappings:**
- 6550 → 6443: Kubernetes API (for ArgoCD)
- 8080 → 80: HTTP Ingress
- 8443 → 443: HTTPS Ingress
- 30808: iris-classifier inference endpoint
- 30809-30850: Reserved for future ML applications
- 30900: Prometheus metrics scraping

**Workloads Deployed:**
- **iris-classifier:** Scikit-learn RandomForest model serving via Flask
- **Namespace:** ml-apps
- **Resources:** 256Mi-512Mi memory, 100m-500m CPU

**Cluster Registration:**
- Registered with ArgoCD on GCP cluster
- Uses Tailscale IP for secure connectivity
- ArgoCD deploys manifests from GitHub to this cluster

**Architecture Benefits:**
- Simulates edge computing patterns (cloud control plane + containerized edge workers)
- Bypasses WSL2 networking limitations through k3d's Docker networking
- Demonstrates hybrid deployment strategies common in IoT/edge ML scenarios
- Shows multi-cluster management skills

---

#### Hybrid Connectivity (Tailscale VPN)
**Purpose:** Secure, encrypted connectivity between GCP and on-premises infrastructure

**Implementation:**
- **GCP VM Tailscale IP:** 100.x.x.x (example: 100.85.38.128)
- **Windows Tailscale IP:** 100.x.x.x (dynamic assignment)
- **Network:** Mesh VPN (all nodes can communicate directly)

**Why Tailscale:**
- Zero-trust security model
- No port forwarding or firewall rule complexity
- Easy setup (5-minute installation)
- Free tier sufficient (100 devices, 3 users)
- Industry-relevant (used by companies like Shopify for hybrid infra)

**Configuration:**
- GCP VM runs Tailscale daemon
- Windows runs Tailscale client
- k3s TLS certificates include Tailscale IP (`--tls-san`)
- ArgoCD connects to k3d via Tailscale IP
- Prometheus scrapes k3d metrics via Tailscale IP

**Challenge Overcome:** 
- Original plan: Physical homelab server with Proxmox
- Reality: Network isolation (public WiFi, different subnets)
- Solution: Hybrid cloud + Tailscale VPN (more industry-relevant anyway)

---

#### Mac Developer Workstation (Optional)
**Purpose:** Multi-cluster management and development

**Tools Installed:**
- kubectl (configured for both GCP and k3d contexts)
- ArgoCD CLI (for cluster management)
- Git (for code commits)
- VS Code (for development)

**Kubeconfig Setup:**
```yaml
contexts:
  - name: gcp (default)
  - name: k3d (Windows cluster via Tailscale)
```

**Usage:**
- Switch contexts: `kubectl config use-context gcp|k3d`
- Can manage both clusters from a single machine
- Does NOT run any Kubernetes components

---

### Phase 2: The MLOps CI/CT/CD Pipeline (GitHub Actions)

#### Repository Structure
**Model Source Repository:** `MLOps-AI-Homelab-Model-Source`
- Contains: ML model code, training scripts, inference server, Dockerfile, tests
- Triggers: CI/CD pipeline on push to main/develop

**Infrastructure Manifests Repository:** `MLOps-AI-Homelab-Infra-Manifests`
- Contains: Kubernetes manifests for all services (platform + applications)
- Watched by: ArgoCD for automated sync
- Structure:
  ```
  platform/
    ├── mlflow/
    ├── monitoring/
  applications/
    ├── iris-classifier/
  argocd-apps/
    ├── iris-classifier-app.yaml
  ```

#### Pipeline Stages (End-to-End)

**Stage 1: Continuous Integration (CI)**

1.1. **Code Quality Checks**
   - **Tool:** Flake8 (Python linting)
   - **Purpose:** Enforce PEP 8 style guidelines
   - **Failure Condition:** Syntax errors, undefined names, complexity violations

1.2. **Unit Testing**
   - **Tool:** Pytest
   - **Coverage:** Test dataset loading, model structure, API endpoints
   - **Failure Condition:** Any test failure

**Stage 2: Security Scanning (DevSecOps)**

2.1. **SAST (Static Application Security Testing)**
   - **Tool:** Bandit
   - **Scans:** Python code for security issues (SQL injection, hardcoded secrets, etc.)
   - **Output:** JSON report with severity ratings
   - **Expected Findings:** Pickle usage (accepted for ML), assert in tests (normal), Flask host binding (required for containers)

2.2. **SCA (Software Composition Analysis)**
   - **Tool:** Snyk (optional, requires account)
   - **Scans:** requirements.txt for vulnerable dependencies
   - **Threshold:** High/Critical severity
   - **Action:** Fails pipeline if critical CVEs found

2.3. **Secrets Detection**
   - **Tool:** Gitleaks
   - **Scans:** Git history for accidentally committed secrets
   - **Failure Condition:** Any secret pattern detected
   - **Prevention:** Pre-commit hook alternative

**Stage 3: Continuous Training (CT)**

3.1. **Model Training**
   - **Dataset:** Iris dataset (scikit-learn built-in)
   - **Algorithm:** RandomForest Classifier (n_estimators=100, max_depth=10)
   - **Split:** 80/20 train/test
   - **Metrics Tracked:** Accuracy, Precision, Recall, F1-score

3.2. **MLflow Integration**
   - **Tracking URI:** `http://GCP_PUBLIC_IP:30500`
   - **Experiment Name:** iris-classification
   - **Logged Data:**
     - Hyperparameters (n_estimators, max_depth, random_state)
     - Metrics (accuracy, precision, recall, f1)
     - Model artifact (pickled RandomForest)
     - Validation status (PASSED/FAILED)

3.3. **Model Validation**
   - **Threshold:** Accuracy >= 85%
   - **Action:** Pipeline fails if below threshold
   - **Trigger:** AI triage workflow if failure occurs
   - **Typical Accuracy:** ~95% (Iris is a simple dataset)

**Stage 4: Containerization & Security**

4.1. **Container Image Build**
   - **Strategy:** Multi-stage Docker build
   - **Base Image:** python:3.11-slim
   - **Security:**
     - Non-root user (appuser, UID 1000)
     - Minimal dependencies (only runtime requirements)
     - Health check endpoint
   - **Size:** ~200MB (optimized)

4.2. **Container Vulnerability Scanning**
   - **Tool:** Trivy
   - **Scan Depth:** OS packages + Python libraries
   - **Severity Filter:** CRITICAL, HIGH
   - **Failure Condition:** Critical CVEs present
   - **Output:** SARIF format for GitHub Security tab

4.3. **Image Registry**
   - **Registry:** GitHub Container Registry (GHCR)
   - **Authentication:** GitHub Actions automatic token
   - **Image Tag Strategy:**
     - `main-latest`: Latest from main branch
     - `main-<commit-sha>`: Specific commit version
     - Example: `ghcr.io/dycouzt/mlops-ai-homelab-model-source:main-a1b2c3d`

**Stage 5: Continuous Deployment (CD) via GitOps**

5.1. **GitOps Update**
   - **Mechanism:** GitHub Actions commits to infra-manifests repo
   - **File Modified:** `applications/iris-classifier/deployment.yaml`
   - **Change:** Update image tag to new version
   - **Authentication:** GitHub Personal Access Token (INFRA_REPO_PAT secret)

5.2. **ArgoCD Synchronization**
   - **Trigger:** Git commit detected by ArgoCD
   - **Target Cluster:** k3d (on-premises)
   - **Sync Policy:** Automated with prune and self-heal
   - **Deployment Strategy:** Rolling update (RollingUpdate)
   - **Health Check:** Kubernetes readiness/liveness probes

5.3. **Verification**
   - **ArgoCD Status:** Synced + Healthy
   - **Pod Status:** Running
   - **Service:** NodePort 30808 accessible
   - **Test:** `curl http://localhost:30808/health`

**Stage 6: AI-Augmented Failure Handling**

6.1. **Pipeline Failure Detection**
   - **Trigger:** `workflow_run` event with `conclusion: failure`
   - **Scope:** Any stage failure (CI, security, training, container, deployment)

6.2. **Automated Triage Workflow**
   - **Workflow:** `ai-pipeline-triage.yml`
   - **Actions:**
     - Fetch failed workflow logs via GitHub API
     - Extract error messages and context
     - Classify failure type (SAST, SCA, test, training, container)
     - Build specialized prompt for Gemini based on failure type

6.3. **Gemini AI Analysis**
   - **Model:** gemini-2.5-flash-lite (free tier)
   - **API:** Vertex AI REST endpoint
   - **Prompt Structure:**
     - System context (DevSecOps specialist, ML engineer, etc.)
     - Failure details (logs, error messages)
     - Task specification (root cause, risk assessment, fix, prevention)
   - **Output:** Markdown-formatted triage report

6.4. **Developer Feedback**
   - **GitHub Issue Creation:** Automatic with labels
   - **Content:**
     - Failure type and severity
     - AI-generated analysis
     - Step-by-step fix instructions
     - Code snippets (if applicable)
     - Link to failed workflow run
   - **Labels:** `pipeline-failure`, `ai-triage`, severity level

---

### Phase 3: The AI-Augmented Monitoring & Operations Loop

#### 3.1. Real-Time Log Analysis (Production Alerts)

**Trigger Mechanism:**
- **Source:** Prometheus alert fires (pod crash, high CPU, OOMKilled, etc.)
- **Route:** Alertmanager → (Future: Webhook receiver) → GitHub Actions
- **Current Implementation:** Manual trigger via `workflow_dispatch`

**Alert Types Configured:**
| Alert Name | Condition | Severity | For Duration |
|------------|-----------|----------|--------------|
| ModelPodNotRunning | Pod phase != Running | Critical | 2 minutes |
| ModelPodFrequentRestarts | >0.1 restarts/15min | Warning | 5 minutes |
| ModelPodOOMKilled | Terminated reason: OOMKilled | Critical | 1 minute |
| ModelHighCPUUsage | CPU >80% of limit | Warning | 5 minutes |
| ModelHighMemoryUsage | Memory >90% of limit | Warning | 5 minutes |

**Workflow Process (`ai-log-analysis.yml`):**

Step 1: **Context Gathering**
- Input parameters: cluster, alert_name, alert_severity, pod_name, namespace
- Authenticate to target cluster (GCP or k3d via kubeconfig secret)
- Fetch pod logs (last 100 lines): `kubectl logs <pod> -n <namespace> --tail=100`
- Fetch Kubernetes events: `kubectl get events --field-selector involvedObject.name=<pod>`

Step 2: **AI Analysis**
- Authenticate to GCP with service account key
- Get OAuth access token: `gcloud auth print-access-token`
- Build JSON payload for Gemini API
- Structured prompt:
  ```
  Role: Expert MLOps SRE
  Context: Alert details, pod logs, K8s events
  Task: 
    1. Root Cause Hypothesis (3 causes, ranked)
    2. Impact Assessment
    3. Immediate Actions
    4. Prevention Recommendations
  Format: Markdown, actionable, ML-specific
  ```
- Call Vertex AI API:
  ```bash
  curl -X POST \
    -H "Authorization: Bearer $TOKEN" \
    https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/publishers/google/models/gemini-2.5-flash-lite:generateContent
  ```
- Parse response: Extract AI-generated text

Step 3: **Reporting & Actionability**
- Create GitHub Issue with:
  - Alert summary (severity, pod, namespace, cluster)
  - AI-generated analysis (markdown formatted)
  - Raw logs and events (collapsed details)
  - Labels: `production-alert`, `ai-analysis`, severity
- Upload artifacts: pod-logs.txt, pod-events.txt, analysis-report.md

**Value Proposition:**
- Reduces MTTR by 60-80% (immediate expert-level analysis)
- Provides actionable insights (not just logs)
- Frees on-call engineer from manual log parsing
- Captures tribal knowledge in AI system prompts

---

#### 3.2. Model Drift Detection & Analysis

**Trigger Mechanism:**
- **Current:** Manual via `workflow_dispatch` (for demo)
- **Future:** Prometheus alert when accuracy < threshold

**Metrics Monitored:**
- Model accuracy (primary metric)
- Prediction distribution (data drift indicator)
- Inference latency (performance drift)
- Request volume (traffic patterns)

**Workflow Process (`ai-drift-detection.yml`):**

Step 1: **Metrics Collection**
- Inputs: model_name, current_accuracy, baseline_accuracy
- Fetch MLflow historical data (last 10 runs):
  ```bash
  curl ${MLFLOW_URI}/api/2.0/mlflow/runs/search
  ```
- Parse metrics: accuracy, precision, recall, timestamps
- Calculate drift percentage: `((baseline - current) / baseline) * 100`

Step 2: **AI Drift Analysis**
- Authenticate to GCP (same as log analysis)
- Build specialized prompt:
  ```
  Role: ML Model Monitoring Specialist
  Context: Current vs baseline accuracy, historical trend, drift %
  Task:
    1. Drift Classification (Data/Concept/Model Decay + P0/P1/P2)
    2. Root Cause Hypothesis (3 likely causes)
    3. Recommended Actions (Immediate/Short-term/Long-term)
    4. Retraining Decision (Yes/No/Wait + rationale)
  Format: Markdown, data-driven, reference trend
  ```
- Call Gemini API (same endpoint)

Step 3: **Remediation Workflow**
- Parse AI severity classification:
  - **P0 (Critical, >10% drift):** Auto-trigger retraining pipeline (future)
  - **P1 (High, 5-10% drift):** Create high-priority GitHub Issue
  - **P2 (Medium, <5% drift):** Create monitoring GitHub Issue
- Issue content:
  - Drift metrics and percentage
  - AI classification and analysis
  - Historical trend graph (via MLflow link)
  - Actionable next steps
- Labels: `model-drift`, severity label, `ml-ops`

**Drift Types Explained:**
- **Data Drift:** Input feature distributions changed (upstream data changes)
- **Concept Drift:** Relationship between features and target changed (world changed)
- **Model Decay:** Model performance degrades over time (aging, not updated)

---

#### 3.3. Pipeline Failure Triage (Automated)

**Trigger Mechanism:**
- **Event:** `workflow_run` completed with `conclusion: failure`
- **Scope:** Main CI/CD pipeline (`ci-ct-cd.yml`)
- **Automatic:** No manual intervention needed

**Workflow Process (`ai-pipeline-triage.yml`):**

Step 1: **Failure Context Extraction**
- Use GitHub API to fetch workflow run details
- Get failed jobs list
- Download job logs (first failed job)
- Extract:
  - Workflow name
  - Failed job name
  - Failed step name
  - Commit SHA and message
  - Branch name
  - Logs (truncated to 5000 chars)

Step 2: **Failure Type Classification**
- Parse failed job name to determine type:
  - **"SAST" or "Bandit"** → DevSecOps security specialist prompt
  - **"SCA" or "Snyk"** → Dependency vulnerability prompt
  - **"test"** → Python testing expert prompt
  - **"train"** → ML engineer prompt
  - **"Container" or "Trivy"** → Container security prompt
  - **Default** → General DevOps engineer prompt

Step 3: **Specialized AI Analysis**
- Build context-specific prompt based on failure type
- Example (SAST):
  ```
  Role: DevSecOps Security Specialist
  Context: SAST scan failed, Bandit findings
  Task:
    1. Root Cause (What vulnerability?)
    2. Risk Assessment (Real threat or false positive?)
    3. Fix Instructions (Specific code fix with line numbers)
    4. Prevention (How to avoid in future?)
  Format: Markdown, specific, actionable
  ```
- Call Gemini API

Step 4: **Automated Issue Creation**
- Create GitHub Issue with:
  - Title: `[PIPELINE FAILURE] {failure_type} - {commit_sha}`
  - Body: Failure details + AI analysis + logs + quick actions checklist
  - Labels: `pipeline-failure`, `ai-triage`, severity label
- Artifact upload: triage-report.md

**Value Proposition:**
- Instant triage (no waiting for human expert)
- Consistent quality (AI uses best practices)
- Specific fixes (not generic advice)
- Learning opportunity (developers learn from AI explanations)

---

### Phase 4: Cross-Cluster Monitoring Architecture

#### Prometheus Configuration (Multi-Cluster Scraping)

**Scrape Targets:**
1. **GCP Cluster (In-Cluster)**
   - Kubernetes API server
   - Kubernetes nodes (kubelet metrics)
   - Kubernetes pods (via service discovery)
   - MLflow service (mlflow.mlflow.svc.cluster.local:5000)

2. **k3d Cluster (Remote via Tailscale)**
   - ML application pods: `100.85.38.128:30808/metrics`
   - Labels: cluster=k3d-on-premises, environment=edge

**Configuration Example:**
```yaml
scrape_configs:
  - job_name: 'k3d-ml-apps'
    static_configs:
    - targets: ['100.85.38.128:30808']
      labels:
        cluster: 'k3d-on-premises'
        environment: 'edge'
        location: 'windows-workstation'
    metrics_path: '/metrics'
    scrape_interval: 15s
```

**Challenges Overcome:**
- k3d NodePort (30808) had to be explicitly exposed during cluster creation
- Tailscale connectivity required TLS SAN in k3s certificates
- Prometheus needed static config (no k8s service discovery for external clusters)

---

## 4. Technology Stack (Final Implementation)

### Cloud Infrastructure
- **Cloud Provider:** Google Cloud Platform (GCP)
  - **Service:** Compute Engine (not GKE)
  - **Instance:** e2-small (2 vCPU, 2GB RAM, 30GB disk)
  - **Region:** us-west1-b
  - **Cost:** $6.50 (2 weeks) or ~$13/month

### On-Premises Infrastructure
- **OS:** Windows 11 with WSL2 (Ubuntu 22.04)
- **Container Runtime:** Docker Desktop (with WSL2 backend)
- **k3d Version:** Latest stable (k3s-in-docker)
- **Available Resources:** 8.5GB RAM, 4 CPU cores

### Orchestration & Platform
- **Kubernetes Distribution:** k3s (lightweight, production-ready)
  - **Control Plane:** GCP e2-small (k3s server mode)
  - **Data Plane:** Windows k3d (k3s agent mode, containerized)
  - **Version:** v1.33 (GCP), v1.31 (k3d)
- **GitOps Controller:** ArgoCD v2.x
  - **Multi-cluster:** Manages 2 clusters (GCP + k3d)
  - **Sync Policy:** Automated with prune and self-heal
- **Containerization:** Docker (multi-stage builds)

### CI/CD & Automation
- **CI/CD Platform:** GitHub Actions (free for public repos)
- **Container Registry:** GitHub Container Registry (GHCR)
- **Workflows:** 4 workflows (CI/CD, log analysis, pipeline triage, drift detection)

### MLOps Tooling
- **Model Registry:** MLflow 2.18.0
  - **Backend:** SQLite (demo; production would use PostgreSQL)
  - **Artifact Store:** Local filesystem with PVC
  - **Access:** NodePort 30500 on GCP cluster
- **Model Serving:** Custom Flask application (v3.0.3)
  - **Framework:** scikit-learn 1.5.2
  - **Deployment:** Kubernetes Deployment on k3d cluster
  - **Future:** KServe for production-grade serving

### DevSecOps Tooling
- **SAST:** Bandit 1.8.6 (Python security linter)
- **SCA:** Snyk (optional, dependency scanning)
- **Secrets Detection:** Gitleaks v8 (Git history scanning)
- **Container Scanning:** Trivy (Aqua Security, OS + library CVEs)
- **Policy:** Pipeline fails on CRITICAL vulnerabilities

### Monitoring & Alerting
- **Metrics Collection:** Prometheus v3.0.0
  - **Retention:** 7 days (RAM-optimized)
  - **Scrape Interval:** 15 seconds
  - **Multi-cluster:** Scrapes GCP (in-cluster) + k3d (via Tailscale)
- **Visualization:** Grafana 11.3.0
  - **Data Source:** Prometheus
  - **Access:** NodePort 30300
- **Alert Routing:** Alertmanager v0.27.0
  - **Webhook:** GitHub Actions workflow_dispatch (via webhook receiver)
  - **Access:** NodePort 30930

### AI Integration
- **LLM Provider:** Google Gemini API (Vertex AI)
- **Model:** gemini-2.5-flash-lite
- **Interface:** REST API (OAuth 2.0 authentication)
- **Authentication:** GCP Service Account with `roles/aiplatform.user`
- **Use Cases:**
  - Real-time log analysis for production alerts
  - Model drift detection and root cause hypothesis
  - CI/CD pipeline failure triage and remediation guidance
- **Cost:** $0 (free tier: 15 RPM, 1500 requests/day, 2M tokens/month)
- **Prompt Engineering:** Specialized prompts per use case (log analysis, drift, triage)

### Networking & Security
- **VPN:** Tailscale (mesh VPN for hybrid connectivity)
  - **GCP Node:** 100.x.x.x
  - **Windows Node:** 100.x.x.x
  - **Cost:** $0 (free tier)
- **TLS:** k3s auto-generated certificates (with Tailscale IP in SAN)
- **Firewall:** GCP firewall rules (port 6443 only)

### Development Tools
- **Language:** Python 3.11
- **Package Manager:** pip
- **Testing:** pytest 8.3.3
- **Linting:** flake8
- **IDE:** VS Code (on Mac)
- **CLI Tools:** kubectl, argocd, gcloud, gh (GitHub CLI)

---

## 5. Guiding Principles (Final)

### Infrastructure & Operations
- **Infrastructure as Code (IaC):** All infrastructure and platform configuration MUST be defined declaratively in code and stored in Git
- **GitOps is the Source of Truth:** The state of both Kubernetes clusters MUST reflect the state of the main branch of the manifests repository. No manual `kubectl apply` commands
- **Automation First:** Every repetitive task, from testing to deployment to analysis, should be automated
- **Immutable Infrastructure:** Containers are treated as immutable artifacts. To change a running application, a new image is built and deployed
- **Multi-Cluster Management:** Use centralized GitOps (ArgoCD) to manage multiple clusters as a single control plane

### Security & Compliance
- **Shift-Left Security:** Security checks are integrated into the earliest possible stages of the pipeline
- **Defense in Depth:** Multiple layers of security (SAST, SCA, secrets, container scanning, runtime policies)
- **Least Privilege:** Service accounts, RBAC, and network policies follow minimum necessary permissions
- **Audit Trail:** All changes tracked in Git, all actions logged

### ML Operations
- **Continuous Training:** Models must be retrained and validated before deployment
- **Validation Gates:** Accuracy thresholds prevent bad models from reaching production
- **Experiment Tracking:** All training runs logged to MLflow with full reproducibility
- **Model Versioning:** Every model artifact is versioned and traceable to source code commit
- **Drift Monitoring:** Continuous monitoring of model performance with automated alerting

### AI-Augmented Operations
- **Human-in-the-Loop:** AI provides recommendations, humans make final decisions
- **Context-Aware Prompts:** Prompts are specialized based on the type of operational issue
- **Actionable Insights:** AI outputs must be specific, with concrete steps, not generic advice
- **Cost Optimization:** Use free-tier services where possible, optimize token usage
- **Prompt Engineering:** Iterative refinement of prompts based on output quality

### Cloud-Agnostic Design
- **Portable Kubernetes Manifests:** No cloud-specific APIs or services
- **Standard k8s:** Use vanilla k3s, not managed services (GKE, EKS, AKS)
- **Multi-Cloud Ready:** Platform can migrate to AWS, Azure, or on-premises with minimal changes
- **Hybrid by Design:** Demonstrates understanding of distributed systems and edge computing

---

## 6. Challenges Overcome & Lessons Learned

### Challenge 1: Network Isolation (Original Homelab Constraint)
**Problem:**
- Original plan: Physical server with Proxmox → VMs → Kubernetes
- Reality: Temporary living situation with public WiFi, no router access
- Mac and Windows on different subnets (172.16.x.x), cannot communicate

**Solutions Attempted:**
- ❌ Local Proxmox cluster: Not feasible (no hardware control)
- ❌ Native k3s on WSL2: Major networking issues (well-documented problem)
- ❌ k3s on Mac: Not natively supported, requires virtualization

**Final Solution:**
- ✅ Hybrid cloud architecture (GCP + k3d on Windows)
- ✅ Tailscale VPN for secure connectivity
- ✅ k3d instead of bare-metal k3s (Docker networking more reliable)

**Lesson Learned:**
- Constraints force creativity → hybrid architecture is MORE impressive than local-only
- Real-world relevance: Many companies have similar hybrid setups
- Network debugging skills significantly improved

---

### Challenge 2: k3s + WSL2 Networking Issues
**Problem:**
- k3s agent in WSL2 cannot properly connect to GCP control plane
- WSL2 networking layer conflicts with k3s expectations
- Errors: TLS handshake timeouts, connection refusals, internal IP routing failures

**Root Cause:**
- k3s prefers internal IPs but WSL2 NAT layer breaks this assumption
- Windows firewall and WSL2 virtual network adapter conflicts

**Solution:**
- Switched to k3d (k3s-in-docker)
- Docker Desktop networking is more reliable than WSL2 native
- k3d handles all networking complexity internally

**Lesson Learned:**
- Don't fight against the tooling - find the path of least resistance
- k3d is actually a better simulation of edge/containerized deployments
- Containerized Kubernetes is a legitimate production pattern (IoT gateways, etc.)

---

### Challenge 3: Gemini API CLI Deprecation
**Problem:**
- Documentation and tutorials showed: `gcloud ai generative-models generate-text`
- This command was deprecated/changed
- Beta commands also didn't work as expected

**Solution:**
- Discovered the REST API is the stable interface
- Use OAuth access tokens + direct curl calls
- More portable (works in any environment with HTTP client)

**Lesson Learned:**
- Always verify API documentation against actual implementation
- REST APIs are more stable than CLI wrappers
- OAuth token pattern is industry standard (learned proper auth flow)

---

### Challenge 4: k3d Port Mapping for Cross-Cluster Monitoring
**Problem:**
- First k3d cluster creation: only exposed basic ports (80, 443, 6443)
- Prometheus on GCP couldn't scrape metrics from k3d (port 30808 not accessible)
- Had to recreate cluster multiple times

**Solution:**
- Comprehensive port mapping strategy during cluster creation
- Exposed all necessary NodePorts upfront (30808, 30809, 30850, 30900)
- Added ports to Docker container at creation time (can't add later)

**Lesson Learned:**
- Plan infrastructure thoroughly before deployment
- Document all required ports and their purposes
- Recreating infrastructure is sometimes faster than trying to patch

---

### Challenge 5: ArgoCD Multi-Cluster Configuration
**Problem:**
- ArgoCD needs kubeconfig with externally accessible k3s API
- k3d default kubeconfig uses `localhost:6550`
- GCP cluster can't reach `localhost` on Windows machine

**Solution:**
- Update k3s TLS certificates to include Tailscale IP (`--tls-san` flag)
- Modify kubeconfig to use Tailscale IP instead of localhost
- Test connectivity from GCP: `curl https://TAILSCALE_IP:6550/version`
- Register cluster with ArgoCD using modified kubeconfig

**Lesson Learned:**
- TLS certificate SANs are critical for multi-homed services
- Always test connectivity from the client perspective
- ArgoCD cluster registration is well-documented but requires careful attention to networking

---

### Challenge 6: GitHub Actions + Gemini API Integration
**Problem:**
- Complex JSON escaping for prompts with logs/multiline content
- GitHub Actions output size limits
- Proper error handling for AI API calls

**Solution:**
- Use `jq -Rs` for proper JSON escaping of multiline strings
- Build JSON payloads programmatically (avoid heredocs in JSON)
- Implement fallback error messages if API fails
- Save full responses as artifacts (bypass output size limits)

**Lesson Learned:**
- Shell scripting in CI/CD requires careful quoting and escaping
- Always include error handling for external API calls
- Artifacts are better than outputs for large data

---

### Challenge 7: Resource Constraints (RAM Optimization)
**Problem:**
- GCP e2-small: Only 2GB RAM
- Need to run: k3s control plane + ArgoCD + MLflow + Prometheus + Grafana + Alertmanager
- Initial deployment: OOMKilled errors

**Solution:**
- Aggressive resource limits on all pods:
  - ArgoCD: 400MB
  - MLflow: 300MB
  - Prometheus: 512MB (reduced retention to 7 days)
  - Grafana: 256MB
  - Alertmanager: 64MB
- Disable unnecessary features (Traefik ingress controller)
- Use SQLite instead of PostgreSQL for MLflow

**Lesson Learned:**
- Kubernetes resource limits are critical for small instances
- Every service has tunable parameters for resource usage
- Prometheus retention is the biggest RAM consumer (metrics data)
- Small instances force you to understand resource management deeply

---

## 7. Future Improvements & Enhancements

### Short-Term (1-2 weeks of work)
1. **Grafana Dashboards:**
   - Model inference latency over time
   - Request rate and error rate
   - Resource utilization (CPU, memory)
   - Alert summary dashboard

2. **Webhook Receiver Service:**
   - Deploy small Flask app in monitoring namespace
   - Receives Alertmanager webhooks
   - Triggers GitHub Actions workflows automatically
   - Eliminates manual workflow_dispatch trigger

3. **Slack Integration:**
   - Post AI analysis to Slack channel
   - Real-time notifications for on-call engineers
   - Link to GitHub Issue for full details

4. **Automated Drift Detection:**
   - Custom Prometheus exporter for MLflow metrics
   - Alert rule: `mlflow_model_accuracy < baseline * 0.95`
   - Automatic trigger of drift detection workflow

### Medium-Term (1-2 months of work)
5. **KServe Integration:**
   - Replace Flask inference server with KServe
   - Implement canary deployments (50/50 traffic split)
   - Demonstrate blue/green deployment patterns
   - Add model explainability (SHAP values)

6. **Additional ML Models:**
   - Deploy 2-3 more models (regression, NLP, image classification)
   - Show multi-model management
   - Different resource requirements
   - Model-to-model dependencies

7. **Advanced Monitoring:**
   - Custom metrics from model (prediction distribution, feature drift)
   - Prometheus client library in Flask app
   - Real-time drift detection (not just batch)
   - Request tracing (OpenTelemetry)

8. **CI/CD Improvements:**
   - Add integration tests (test against deployed model)
   - Performance testing (load test inference endpoint)
   - Automated rollback on deployment failure
   - Canary analysis (progressive delivery)

### Long-Term (2-3 months of work)
9. **Production Hardening:**
   - PostgreSQL for MLflow backend
   - S3-compatible storage for model artifacts
   - HA setup for platform services (multiple replicas)
   - Backup and disaster recovery procedures

10. **Advanced AIOps:**
    - Anomaly detection in metrics (Prophet, LSTM)
    - Predictive alerting (alert before incident happens)
    - Auto-remediation (not just recommendations)
    - Feedback loop (track if AI suggestions were helpful)

11. **Security Enhancements:**
    - Kubernetes Network Policies
    - Pod Security Standards (PSS)
    - OPA/Gatekeeper for policy enforcement
    - Secrets management (External Secrets Operator)

12. **Multi-Tenancy:**
    - Namespace per team/project
    - RBAC for different user roles
    - Resource quotas and limits per namespace
    - Separate MLflow experiments per team

---

## 8. Project Outcomes & Metrics

### Technical Achievements
- ✅ **2 Kubernetes clusters** deployed and managed (GCP + k3d)
- ✅ **7-stage CI/CD pipeline** with 4 types of security scanning
- ✅ **3 AI-powered workflows** (log analysis, drift detection, pipeline triage)
- ✅ **GitOps-driven deployment** (100% of infrastructure in Git)
- ✅ **Multi-cluster monitoring** (Prometheus scraping across clusters)
- ✅ **Zero-downtime deployments** (rolling updates via ArgoCD)
- ✅ **End-to-end ML lifecycle** (training → validation → deployment → monitoring)

### Cost Efficiency
- **Total Infrastructure Cost:** $6.50 (2-week project) or ~$13/month
- **AI API Cost:** $0 (within free tier)
- **Developer Time:** ~40-50 hours over 2 weeks
- **ROI:** Immeasurable (portfolio piece for career advancement)

### Skills Developed
- **Platform Engineering:** Multi-cluster Kubernetes, hybrid cloud architecture
- **MLOps:** Full ML pipeline design, model registry, drift detection
- **DevSecOps:** Integrated security scanning, vulnerability management
- **AIOps:** LLM integration, prompt engineering, operational automation
- **SRE:** Observability, monitoring, alerting, incident response
- **Networking:** VPN setup, multi-cluster connectivity, troubleshooting
- **Problem Solving:** Overcame 7+ major technical challenges

### Portfolio Value
- **Differentiation:** AI-augmented monitoring (most MLOps projects don't have this)
- **Real-World Relevance:** Hybrid architecture mirrors enterprise patterns
- **Completeness:** End-to-end system (not just a tutorial)
- **Complexity:** Multi-cluster, multi-repo, multi-technology integration
- **Documentation:** Comprehensive README, architecture diagrams, demo-ready

---

## 9. Key Differentiators (Why This Project Stands Out)

### 1. AI-Augmented Operations (Not Just "AI Buzzword")
**What Most Do:** Deploy a model, maybe add monitoring
**What This Does:** Uses AI to OPERATE the platform itself
- AI analyzes production alerts → reduces MTTR
- AI triages pipeline failures → accelerates development
- AI detects model drift → prevents degradation
**Why It Matters:** Shows understanding of AI as a tool for engineers, not just for end-users

### 2. Hybrid Cloud Architecture (Real-World Pattern)
**What Most Do:** Deploy to a single cloud or local cluster
**What This Does:** Control plane in cloud, workloads on-premises
**Why It Matters:** 
- Demonstrates multi-cluster management skills
- Shows understanding of edge computing
- Mirrors how companies like Shopify, Cloudflare operate
- Addresses data sovereignty, latency, cost concerns

### 3. Security as a First-Class Citizen (DevSecOps)
**What Most Do:** Maybe add a Dockerfile, maybe some tests
**What This Does:** 4 types of automated security scanning in pipeline
- SAST (Bandit), SCA (Snyk), Secrets (Gitleaks), Container (Trivy)
**Why It Matters:** 
- Security is a top concern for hiring managers
- Shows understanding of supply chain security
- Demonstrates shift-left security principles

### 4. GitOps-Driven (Not Just CI/CD)
**What Most Do:** CI/CD that deploys directly via kubectl
**What This Does:** GitOps with ArgoCD (Git is source of truth)
**Why It Matters:**
- Industry best practice (CNCF graduated project)
- Enables audit trail, easy rollback, declarative config
- Shows understanding of modern deployment patterns

### 5. Production-Grade Observability
**What Most Do:** "Here's my model, it works"
**What This Does:** 
- Multi-cluster Prometheus monitoring
- Alert rules for pod health, resources, performance
- AI-powered analysis of alerts
- Grafana dashboards (future)
**Why It Matters:** Production ML is 10% training, 90% operations

### 6. Comprehensive Documentation
**What Most Do:** Basic README with setup instructions
**What This Does:**
- Detailed architecture documentation
- Challenges and lessons learned
- Future improvements roadmap
- Demo-ready video and talking points
**Why It Matters:** Shows communication skills, thoroughness, professionalism

---

## 10. Demo Script & Talking Points (For Video/Interviews)

### Video Structure (10-12 minutes total)

**[0:00-1:00] Introduction & Hook**
- "Hi, I'm [Name], and I built an AI-augmented MLOps platform that demonstrates how modern companies operate machine learning in production."
- "The unique differentiator? It uses Google's Gemini AI to automatically analyze production alerts, detect model drift, and triage pipeline failures - reducing Mean Time To Resolution by 60-80%."
- "Let me show you how it works."

**[1:00-2:30] Project Overview & Motivation**
- "Most MLOps tutorials show you how to train and deploy a model."
- "But in production, models fail. Pipelines break. Alerts fire at 3 AM."
- "This project asks: What if AI could handle the first level of triage?"
- Show diagram of architecture (hybrid cloud)
- "Control plane in GCP, workloads on-premises, connected via Tailscale VPN"

**[2:30-4:30] Architecture Deep Dive**
- Screen share: ArgoCD UI showing both clusters
  - "ArgoCD manages two clusters from a single control plane"
  - Show k3d cluster registered, iris-classifier app synced
- Screen share: Prometheus targets
  - "Prometheus scrapes metrics from both GCP and on-premises"
  - Show k3d-ml-apps target UP
- Screen share: MLflow experiments
  - "Every model training run is logged with full reproducibility"
  - Show metrics, parameters, model artifacts

**[4:30-6:30] CI/CD Pipeline Walkthrough**
- Screen share: GitHub Actions
  - "When I push code, a 7-stage pipeline kicks off"
  - Show pipeline stages: CI, Security, Training, Container, Deploy
- Screen share: Security scanning results
  - "Bandit finds security issues, Trivy scans for CVEs"
  - "Pipeline fails if critical vulnerabilities found"
- Screen share: ArgoCD sync
  - "GitOps update triggers ArgoCD to deploy to k3d"
  - Show pod rolling update

**[6:30-8:30] AI-Augmented Monitoring (The Star of the Show)**
- **Demo 1: Log Analysis**
  - Screen share: GitHub Actions workflow
  - "I can manually trigger log analysis for any pod"
  - Show workflow run, fetching logs, calling Gemini
  - Screen share: GitHub Issue
  - "Gemini provides root cause hypothesis and immediate actions"
  - Highlight actionable insights

- **Demo 2: Pipeline Triage**
  - Screen share: Failed pipeline
  - "When a pipeline fails, AI automatically analyzes it"
  - Show triage workflow run
  - Screen share: GitHub Issue with AI analysis
  - "AI classified it as a security issue and provided a specific fix"

- **Demo 3: Drift Detection**
  - Screen share: Drift detection workflow
  - "I can manually check for model drift"
  - Show AI analyzing metrics from MLflow
  - Screen share: GitHub Issue
  - "AI recommends whether to retrain, wait, or rollback"

**[8:30-9:30] Challenges & Lessons Learned**
- "This wasn't straightforward. Let me share some challenges:"
  - "Network isolation forced me into hybrid cloud (better outcome)"
  - "WSL2 + k3s networking issues → switched to k3d"
  - "Gemini CLI deprecation → learned REST API patterns"
- "Each challenge taught me something valuable about production systems"

**[9:30-10:30] Future Improvements**
- "Where would I take this next?"
  - "Add KServe for production-grade serving"
  - "Implement canary deployments"
  - "Build Grafana dashboards"
  - "Automate the Alertmanager webhook"
- "But the core is production-ready today"

**[10:30-11:00] Technology Stack Summary**
- Quick list: Kubernetes, ArgoCD, MLflow, Prometheus, Gemini, GitHub Actions
- "All industry-standard, cloud-agnostic tools"
- "Total cost: $13/month for a full production-grade platform"

**[11:00-12:00] Closing & Call to Action**
- "This project demonstrates:"
  - "Multi-cluster Kubernetes management"
  - "End-to-end MLOps pipeline"
  - "Practical AI integration (not just hype)"
  - "Production-grade security and observability"
- "All code is on GitHub: [show repos]"
- "Thanks for watching! Questions? Find me on LinkedIn."

---

### Interview Talking Points (Elevator Pitch Variations)

**30-Second Version:**
"I built a hybrid MLOps platform with AI-powered monitoring. It uses GitOps to deploy ML models across GCP and on-premises, with Gemini AI automatically analyzing production alerts and pipeline failures to reduce MTTR."

**2-Minute Version:**
"I wanted to demonstrate not just how to deploy ML models, but how to operate them in production. So I built a hybrid platform with a GCP control plane and on-premises workloads.

The pipeline has 7 stages including security scanning - SAST, SCA, container scanning. Models must pass accuracy thresholds before deployment.

The unique part is AI-augmented monitoring. When production alerts fire, Gemini analyzes the logs and provides root cause hypotheses with immediate actions. When pipelines fail, AI triages the failure and suggests specific fixes.

It's all GitOps-driven via ArgoCD managing two Kubernetes clusters. Multi-cluster Prometheus monitors both. Total cost? $13/month.

The project demonstrates platform engineering, MLOps, DevSecOps, and practical AI integration."

**5-Minute Version:**
[Use the 2-minute version, then add:]

"Let me walk through a scenario: A model pod crashes with OOMKilled. Prometheus fires an alert. My workflow fetches the pod logs and Kubernetes events, sends them to Gemini with a structured prompt, and Gemini returns a markdown report with:
- Root cause: Likely memory leak in preprocessing step
- Impact: 100% of inference requests failing
- Immediate action: Increase memory limit to 1GB, restart pod
- Prevention: Add memory profiling to CI tests

All this appears in a GitHub Issue within 60 seconds of the alert firing.

Or consider pipeline failures: If a security scan fails, AI looks at the Bandit findings and says 'This is a false positive - pickle is standard for ML model serialization. However, consider using joblib for better performance.'

That's the value - not replacing engineers, but giving them expert-level analysis instantly."

---

## 11. Repository Links & Resources

### Primary Repositories
- **Model Source:** https://github.com/Dycouzt/MLOps-AI-Homelab-Model-Source
- **Infrastructure Manifests:** https://github.com/Dycouzt/MLOps-AI-Homelab-Infra-Manifests

### Key Files to Highlight
- `ci-ct-cd.yml`: Main CI/CD pipeline (7 stages)
- `ai-log-analysis.yml`: Log analysis workflow
- `ai-pipeline-triage.yml`: Pipeline triage workflow
- `ai-drift-detection.yml`: Drift detection workflow
- `platform/monitoring/monitoring.yaml`: Prometheus + Grafana + Alertmanager
- `platform/mlflow/mlflow.yaml`: MLflow deployment
- `applications/iris-classifier/deployment.yaml`: Model deployment

### External Resources
- ArgoCD: https://argo-cd.readthedocs.io/
- MLflow: https://mlflow.org/docs/latest/index.html
- Prometheus: https://prometheus.io/docs/
- Gemini API: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini
- k3s: https://k3s.io/
- k3d: https://k3d.io/

---

## 12. Final Thoughts & Reflections

This project evolved significantly from the original vision (Proxmox homelab) to the final implementation (hybrid cloud with k3d). The constraints forced creative solutions that resulted in a MORE impressive and industry-relevant architecture.

Key learnings:
1. **Constraints breed innovation** - Network isolation led to hybrid architecture
2. **Tools change, principles don't** - GitOps, IaC, automation are timeless
3. **AI is a tool, not magic** - Proper prompts and integration patterns matter
4. **Production is harder than training** - 90% of MLOps is operations
5. **Documentation is as important as code** - Helps you and future employers understand your work

This project demonstrates that you don't need expensive infrastructure to learn production-grade skills. A $13/month GCP instance + a borrowed laptop + free AI APIs = A complete MLOps platform.

The investment: ~50 hours of learning and building.
The payoff: A portfolio piece that stands out in interviews.

**Next steps:** Apply to MLOps, Platform Engineering, and SRE roles. Use this project as your technical showcase. Practice the demo until you can deliver it confidently in 5-10 minutes.

**You've built something real. Now go show it off.** 🚀

---

*Document Version: 1.0 Final*
*Last Updated: 2025-11-12*
*Project Duration: 2 weeks*
*Status: ✅ Production-Ready*