# Model Drift Detection and AI-Augmented Analysis

Model drift is a critical Site Reliability Engineering (SRE) concern in MLOps, as it represents a silent degradation of the system's core value proposition. Our platform implements a tiered, AI-augmented strategy to proactively detect and diagnose drift, ensuring model reliability and accelerating the time to remediation.

This process is managed by the `ai-drift-detection.yml` GitHub Actions workflow, leveraging historical data from **MLflow** and intelligent analysis from **Gemini 2.5 Flash Lite**.

---

## 1. Core Architecture and Workflow

The drift detection mechanism is integrated into the **AI-Augmented Monitoring & Operations Loop** (Phase 3.2).

### Data Source: MLflow

All model training runs, metrics (accuracy, precision, recall), and artifacts are logged to the centralized **MLflow** instance running on the GCP Control Plane. This provides the necessary historical baseline data for comparison.

### Trigger Mechanism

| Current State (MVP) | Future State (Short-Term Enhancement) |
| :--- | :--- |
| **Manual Dispatch:** Triggered via `workflow_dispatch` in GitHub Actions for demonstration and ad-hoc checks. | **Automated Alert:** Triggered by a **Prometheus** alert rule that scrapes a custom MLflow exporter, firing when `mlflow_model_accuracy < baseline * 0.95`. |

### Workflow Steps (`ai-drift-detection.yml`)

1.  **Metrics Collection:** The workflow fetches the current model's performance metrics and the historical baseline metrics (last 10 runs) from the MLflow Tracking Server.
2.  **Drift Calculation:** Calculates the drift percentage: `((baseline - current) / baseline) * 100`.
3.  **AI Analysis:** The collected data is sent to the Gemini API with a specialized prompt.
4.  **Remediation Workflow:** Based on the AI's classification, a GitHub Issue is created with actionable steps.

---

## 2. Tiered Drift Detection Strategy

Our strategy prioritizes **outcome-based monitoring** (Concept Drift) as the primary signal, with **Prediction Drift** serving as an early warning system.

### Tier 1: Concept Drift Monitoring (Primary Signal)

This tier focuses on the **model's outcome**—how well it performs against ground truth. This is the most critical indicator of model decay.

| Metric | Baseline & Threshold | Response |
| :--- | :--- | :--- |
| **Model Accuracy** | Rolling 7-day, 14-day, and 30-day averages. | **Critical Alert:** Accuracy drops **>10%** from the 7-day baseline **OR** falls below an **85%** absolute threshold. |
| **Precision, Recall, F1** | Monitored per class to detect performance degradation in specific segments. | **Action:** Triggers the AI analysis for root cause hypothesis and automated retraining recommendation. |
| **Drift Type** | **Concept Drift** (relationship between features and target changed) or **Model Decay** (performance degrades over time). | |

### Tier 2: Prediction Drift Monitoring (Early Warning)

This tier focuses on the **model's output**—the distribution of its predictions. This is a real-time signal that does not require ground truth labels.

| Metric | Baseline & Threshold | Response |
| :--- | :--- | :--- |
| **Prediction Class Distribution** | 24-hour moving average of the output class probabilities. | **Warning Alert:** Prediction distribution shifts **>30%** from the baseline. |
| **Mean Confidence Score** | Average confidence of the model's predictions. | **Warning Alert:** Mean confidence drops **>15%**. |
| **Drift Type** | **Prediction Drift** (likely caused by upstream Data Drift). | **Action:** AI analysis generates a hypothesis (e.g., "Likely data drift in features X, Y, Z") for early investigation. |

### Tier 3: Data Drift Monitoring (Future Enhancement)

This tier involves feature-level analysis (e.g., Population Stability Index - PSI, Kolmogorov-Smirnov test - KS test) to compare the distribution of incoming features against the training data. This is a resource-intensive task and has been **deferred** to a post-MVP enhancement to demonstrate pragmatic prioritization of high-ROI features.

---

## 3. AI-Augmented Drift Analysis

The core value of this system is the intelligent analysis provided by Gemini. The AI is not just reporting a number; it is acting as an expert **ML Model Monitoring Specialist**.

### Specialized Prompt Structure

The workflow constructs a structured prompt to guide the LLM's output:

| Prompt Component | Purpose |
| :--- | :--- |
| **Role** | `ML Model Monitoring Specialist` |
| **Context** | Current vs. baseline accuracy, historical trend, calculated drift percentage, and Tier 2 prediction shift data. |
| **Task** | 1. **Drift Classification** (Data/Concept/Model Decay + P0/P1/P2 severity). 2. **Root Cause Hypothesis** (3 likely causes). 3. **Recommended Actions** (Immediate/Short-term/Long-term). 4. **Retraining Decision** (Yes/No/Wait + rationale). |
| **Format** | Markdown, data-driven, actionable, and referencing the trend. |

### Remediation Workflow

The AI's severity classification directly dictates the automated response:

| AI Classification | Severity | Automated Action |
| :--- | :--- | :--- |
| **P0** | Critical (>10% drift) | **Auto-trigger Retraining Pipeline** (Future). Create high-priority GitHub Issue. |
| **P1** | High (5-10% drift) | Create high-priority GitHub Issue with full analysis and action plan. |
| **P2** | Medium (<5% drift) | Create monitoring GitHub Issue for tracking and manual review. |

This process ensures that the platform moves beyond simple alerting to providing **actionable, expert-level remediation guidance** within seconds of a drift event being detected.