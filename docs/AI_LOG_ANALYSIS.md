## LOG\_ANALYSIS.md

# AI-Augmented Real-Time Log Analysis for Production Alerts

The platform's most significant differentiator is its ability to use AI to perform real-time root cause analysis on production alerts. This capability is a core component of our AIOps strategy, designed to drastically reduce the Mean Time To Resolution (MTTR) by providing on-call engineers with immediate, expert-level diagnostic reports.

This process is managed by the `ai-log-analysis.yml` GitHub Actions workflow.

---

## 1. The Alert-to-Analysis Workflow

The system is designed to automatically transition from a raw alert signal to a structured, actionable incident report.

### Trigger Mechanism

| Current State (MVP) | Future State (Short-Term Enhancement) |
| :--- | :--- |
| **Manual Dispatch:** Triggered via `workflow_dispatch` in GitHub Actions, simulating a manual alert triage process. | **Automated Webhook:** **Alertmanager** routes a webhook to a small, dedicated **Webhook Receiver Service** (Flask app) deployed in the monitoring namespace, which then automatically triggers the GitHub Actions workflow. |

### Workflow Steps (`ai-log-analysis.yml`)

1.  **Context Gathering:** The workflow receives input parameters (e.g., `pod_name`, `namespace`, `alert_name`, `cluster`).
2.  **Log & Event Fetching:** Authenticates to the target cluster (GCP or k3d via kubeconfig secret) and executes the following commands:
    *   **Pod Logs:** `kubectl logs <pod> -n <namespace> --tail=100` (fetches the most recent 100 lines).
    *   **Kubernetes Events:** `kubectl get events --field-selector involvedObject.name=<pod>` (fetches relevant events like `OOMKilled`, `ImagePullBackOff`, etc.).
3.  **AI Analysis:** The raw logs and events are bundled into a structured prompt and sent to the Gemini API.
4.  **Reporting & Actionability:** The AI-generated analysis is parsed and used to create a detailed GitHub Issue.

---

## 2. Alert Types Configured

The Prometheus Alertmanager is configured with rules to detect common MLOps and Kubernetes operational issues, which serve as the input for the AI analysis workflow.

| Alert Name | Condition | Severity | Typical Root Cause |
| :--- | :--- | :--- | :--- |
| **ModelPodNotRunning** | Pod phase is not `Running` | Critical | Deployment misconfiguration, failed readiness probe, image pull error. |
| **ModelPodFrequentRestarts** | Restarts > 0.1 per 15 minutes | Warning | Liveness probe failure, application crash (e.g., unhandled exception). |
| **ModelPodOOMKilled** | Terminated reason is `OOMKilled` | Critical | Memory leak in the inference server, insufficient memory limits, large model loading. |
| **ModelHighCPUUsage** | CPU > 80% of limit | Warning | High request volume, inefficient model inference code, missing resource limits. |
| **ModelHighMemoryUsage** | Memory > 90% of limit | Warning | Memory leak, resource contention, incorrect memory request/limit settings. |

---

## 3. AI-Powered Diagnostic Structure

The Gemini model is instructed to act as an **Expert MLOps SRE** and deliver a structured, actionable report, moving beyond simple log aggregation.

### Specialized Prompt Structure

The prompt is engineered to ensure the AI's output is immediately useful for an on-call engineer:

| Prompt Component | Purpose |
| :--- | :--- |
| **Role** | `Expert MLOps SRE` |
| **Context** | Alert details (name, severity, pod, cluster), full pod logs, and Kubernetes events. |
| **Task** | 1. **Root Cause Hypothesis** (3 most likely causes, ranked). 2. **Impact Assessment** (What is the user impact?). 3. **Immediate Actions** (Step-by-step fix instructions). 4. **Prevention Recommendations** (How to avoid recurrence). |
| **Format** | Markdown, actionable, ML-specific (e.g., suggesting a model rollback or increasing a memory limit). |

### Reporting and Actionability

The final output is a GitHub Issue that serves as the incident report and runbook:

| Issue Component | Value Proposition |
| :--- | :--- |
| **Title** | `[PRODUCTION ALERT] {Alert Name} - {Pod Name}` |
| **Body (AI Analysis)** | The full, markdown-formatted report from Gemini, including the root cause and fix instructions. |
| **Raw Logs & Events** | Collapsed details sections containing the raw `kubectl logs` and `kubectl get events` output for human verification. |
| **Labels** | `production-alert`, `ai-analysis`, and the severity level (`critical`, `warning`). |

### Value Proposition

By automating the initial log parsing and diagnosis, the AI-Augmented Log Analysis system achieves:

*   **Reduced MTTR:** Provides an expert-level diagnosis in under 60 seconds, eliminating manual log-sifting time.
*   **Consistent Quality:** Ensures every incident is triaged using a consistent set of best practices defined in the system prompt.
*   **Knowledge Capture:** The AI's analysis and prevention recommendations serve as a living runbook, capturing tribal knowledge and improving system resilience over time.