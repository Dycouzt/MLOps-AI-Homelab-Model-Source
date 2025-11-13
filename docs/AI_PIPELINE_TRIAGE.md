# AI-Augmented CI/CD Pipeline Failure Triage

A broken CI/CD pipeline is a major bottleneck to development velocity. Our platform incorporates an AI-Augmented Triage system that automatically analyzes pipeline failures, determines the root cause, and provides specific, actionable fix instructions to the developer. This significantly accelerates the feedback loop and reduces the time developers spend debugging CI/CD issues.

This process is managed by the `ai-pipeline-triage.yml` GitHub Actions workflow.

---

## 1. The Automated Triage Workflow

The triage system is designed to be fully automatic, triggering immediately upon a pipeline failure.

### Trigger Mechanism

| Event | Scope | Automation |
| :--- | :--- | :--- |
| **`workflow_run`** | Completed with `conclusion: failure` | **Automatic:** No manual intervention is required. The system watches the main CI/CT/CD pipeline (`ci-ct-cd.yml`). |

### Workflow Steps (`ai-pipeline-triage.yml`)

1.  **Failure Context Extraction:**
    *   Uses the GitHub API to fetch the failed workflow run details.
    *   Identifies the **first failed job** and **failed step name**.
    *   Downloads the full job logs.
    *   Extracts key metadata: Commit SHA, branch name, and a truncated version of the logs (up to 5000 characters) for the AI prompt.
2.  **Failure Type Classification:**
    *   The failed job/step name is used to classify the failure type, which determines the specialized **AI Persona** and **Prompt Structure**.
3.  **Specialized AI Analysis:**
    *   A context-specific prompt is built and sent to the Gemini API.
4.  **Automated Issue Creation:**
    *   A new GitHub Issue is created with the AI's analysis, providing the developer with an instant, expert-level diagnosis.

---

## 2. Specialized AI Personas and Prompts

The system's intelligence comes from its ability to adapt the AI's persona and context based on the failure type, ensuring the advice is highly relevant and specific.

| Failed Job/Step Name | Failure Type | AI Persona (System Context) | Key Task for AI |
| :--- | :--- | :--- | :--- |
| **`SAST`**, **`Bandit`** | DevSecOps (Static Analysis) | `DevSecOps Security Specialist` | 1. Root Cause (Vulnerability). 2. Risk Assessment (Real threat or false positive?). 3. **Fix Instructions (Specific code fix with line numbers).** 4. Prevention. |
| **`SCA`**, **`Snyk`** | Dependency Vulnerability | `Software Supply Chain Security Expert` | 1. Vulnerable dependency and CVE. 2. Recommended version upgrade. 3. Impact of the vulnerability. |
| **`test`**, **`Pytest`** | Unit/Integration Testing | `Python Testing Expert` | 1. Failed test file and function. 2. Hypothesis for the test failure (e.g., assertion error, missing mock). 3. Fix instructions. |
| **`train`**, **`Model Validation`** | Continuous Training (CT) | `ML Engineer & Data Scientist` | 1. Validation Threshold Failure (e.g., Accuracy < 85%). 2. Root Cause Hypothesis (e.g., Data quality issue, hyperparameter drift). 3. Next steps (e.g., Re-run with new seed, check data pipeline). |
| **`Container`**, **`Trivy`** | Container Security/Build | `Containerization & DevSecOps Expert` | 1. Critical CVEs found. 2. Fix (e.g., Update base image, remove package). 3. Build error root cause (e.g., missing dependency in final stage). |
| **Default** | General DevOps/Scripting | `Expert DevOps Engineer` | 1. General script error analysis. 2. Suggest command line fix. |

---

## 3. Developer Feedback and Actionability

The final GitHub Issue serves as the developer's instant, personalized runbook for fixing the pipeline.

### Automated Issue Content

| Issue Component | Value Proposition |
| :--- | :--- |
| **Title** | `[PIPELINE FAILURE] {Failure Type} - {Commit SHA}` |
| **Body (AI Analysis)** | The full, markdown-formatted report from Gemini, including the specific fix instructions and code snippets (if applicable). |
| **Failure Details** | Raw logs, failed job/step name, and a link to the failed workflow run. |
| **Labels** | `pipeline-failure`, `ai-triage`, and the severity level. |

### Value Proposition

*   **Instant Triage:** Developers receive a diagnosis within seconds, eliminating the typical delay of waiting for a human expert.
*   **Specific Fixes:** The AI provides concrete, context-aware instructions (e.g., "Change line 42 in `app.py` from `assert` to `if`" for a Bandit failure).
*   **Accelerated Velocity:** By reducing the time spent on pipeline debugging, the system directly accelerates the developer feedback loop and overall development velocity.
*   **Learning Opportunity:** The detailed explanations from the AI serve as a continuous learning tool for developers, improving their understanding of DevSecOps and MLOps best practices.