import React, { useState } from 'react';
import { Server, GitBranch, Zap, Brain, Shield, Eye, Package, Activity, ArrowRight, CheckCircle, AlertTriangle } from 'lucide-react';

const MLOpsPlatformExplainer = () => {
  const [activeView, setActiveView] = useState('overview');
  const [selectedFlow, setSelectedFlow] = useState(null);

  const flows = {
    deployment: {
      title: "End-to-End Deployment Flow",
      color: "blue",
      steps: [
        { icon: GitBranch, title: "1. Code Commit", desc: "Developer pushes code to GitHub (model-source repo)", detail: "Triggers GitHub Actions workflow on push to main/develop branch" },
        { icon: Shield, title: "2. Security Scan", desc: "Bandit (SAST), Snyk (SCA), Gitleaks, Trivy", detail: "Pipeline fails if CRITICAL vulnerabilities found. Protects supply chain." },
        { icon: CheckCircle, title: "3. Model Training", desc: "Train RandomForest on Iris dataset", detail: "Logs to MLflow: accuracy, precision, recall, F1. Validates ≥85% accuracy." },
        { icon: Package, title: "4. Container Build", desc: "Multi-stage Docker build + Trivy scan", detail: "Non-root user, minimal image (~200MB). Pushed to GHCR with commit SHA tag." },
        { icon: GitBranch, title: "5. GitOps Update", desc: "Update infra-manifests repo deployment.yaml", detail: "GitHub Actions commits new image tag. ArgoCD detects change." },
        { icon: Zap, title: "6. ArgoCD Sync", desc: "ArgoCD deploys to k3d cluster", detail: "Rolling update, health checks, automatic sync with prune/self-heal." },
        { icon: CheckCircle, title: "7. Production", desc: "Model serving on NodePort 30808", detail: "Flask app responds to /predict endpoint. Prometheus scrapes metrics." }
      ]
    },
    aiMonitoring: {
      title: "AI-Augmented Monitoring Flow",
      color: "purple",
      steps: [
        { icon: AlertTriangle, title: "1. Alert Fires", desc: "Prometheus detects pod crash/OOMKilled", detail: "Alert rules check pod phase, restarts, CPU, memory every 15s" },
        { icon: Activity, title: "2. Context Gathering", desc: "GitHub Actions fetches logs + events", detail: "kubectl logs --tail=100, kubectl get events for the failing pod" },
        { icon: Brain, title: "3. Gemini Analysis", desc: "AI analyzes logs with specialized prompt", detail: "Role: MLOps SRE. Task: Root cause (3 hypotheses), impact, actions, prevention" },
        { icon: Package, title: "4. GitHub Issue", desc: "Auto-create issue with AI insights", detail: "Labels: production-alert, severity. Contains actionable remediation steps." },
        { icon: CheckCircle, title: "5. Resolution", desc: "Engineer applies fix, closes issue", detail: "MTTR reduced 60-80%. AI provides expert-level analysis instantly." }
      ]
    },
    pipelineTriage: {
      title: "Pipeline Failure Triage Flow",
      color: "red",
      steps: [
        { icon: AlertTriangle, title: "1. Pipeline Fails", desc: "CI/CD stage fails (security, test, training)", detail: "workflow_run event with conclusion: failure triggers triage" },
        { icon: Activity, title: "2. Log Extraction", desc: "GitHub API fetches failed job logs", detail: "Gets workflow run, failed jobs, step details, commit info" },
        { icon: Brain, title: "3. Failure Classification", desc: "Determine type: SAST, SCA, test, training", detail: "Different AI prompt for each type (DevSecOps, ML engineer, etc.)" },
        { icon: Brain, title: "4. AI Triage", desc: "Gemini provides root cause + fix", detail: "Specific code fix, risk assessment, prevention strategy" },
        { icon: Package, title: "5. GitHub Issue", desc: "Auto-create with fix instructions", detail: "Labels: pipeline-failure, ai-triage. Developer gets immediate guidance." }
      ]
    },
    driftDetection: {
      title: "Model Drift Detection Flow",
      color: "orange",
      steps: [
        { icon: Activity, title: "1. Metrics Collection", desc: "Fetch current + historical accuracy", detail: "MLflow API: last 10 runs, compare current vs baseline" },
        { icon: Brain, title: "2. Drift Calculation", desc: "Calculate percentage change", detail: "drift_pct = ((baseline - current) / baseline) * 100" },
        { icon: Brain, title: "3. AI Classification", desc: "Gemini classifies drift severity", detail: "P0 (>10%), P1 (5-10%), P2 (<5%). Data/Concept/Model decay type." },
        { icon: Package, title: "4. Remediation Plan", desc: "AI recommends: retrain/wait/rollback", detail: "Immediate, short-term, long-term actions with rationale" },
        { icon: CheckCircle, title: "5. Action", desc: "P0: auto-retrain, P1/P2: GitHub Issue", detail: "Future: automated retraining pipeline trigger for P0" }
      ]
    }
  };

  const architectureComponents = [
    { 
      name: "GCP Control Plane", 
      icon: Server, 
      color: "blue",
      services: ["ArgoCD", "MLflow", "Prometheus", "Grafana", "Alertmanager"],
      role: "Centralized management"
    },
    { 
      name: "k3d Data Plane", 
      icon: Package, 
      color: "green",
      services: ["iris-classifier", "ML Workloads"],
      role: "Edge/on-prem execution"
    },
    { 
      name: "Tailscale VPN", 
      icon: Shield, 
      color: "purple",
      services: ["Secure mesh network"],
      role: "Hybrid connectivity"
    },
    { 
      name: "GitHub Actions", 
      icon: Zap, 
      color: "orange",
      services: ["CI/CD", "AI Workflows"],
      role: "Automation engine"
    },
    { 
      name: "Gemini AI", 
      icon: Brain, 
      color: "pink",
      services: ["Log Analysis", "Drift Detection", "Pipeline Triage"],
      role: "Intelligent operations"
    }
  ];

  const ValueProps = () => (
    <div className="space-y-4">
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4">
        <h3 className="font-bold text-blue-900 mb-2">🎯 For Technical Audiences</h3>
        <ul className="text-sm space-y-1 text-blue-800">
          <li>• Multi-cluster Kubernetes management (GitOps with ArgoCD)</li>
          <li>• 7-stage CI/CT/CD pipeline with shift-left security</li>
          <li>• Hybrid cloud architecture (GCP control + on-prem workloads)</li>
          <li>• AIOps integration (Gemini for log analysis, drift detection, triage)</li>
          <li>• Production-grade observability (Prometheus multi-cluster scraping)</li>
        </ul>
      </div>

      <div className="bg-green-50 border-l-4 border-green-500 p-4">
        <h3 className="font-bold text-green-900 mb-2">💼 For Non-Technical Audiences</h3>
        <ul className="text-sm space-y-1 text-green-800">
          <li>• <strong>Problem:</strong> ML models break in production, costing time and money</li>
          <li>• <strong>Solution:</strong> AI assistant monitors the platform 24/7</li>
          <li>• <strong>Impact:</strong> Reduces troubleshooting time by 60-80%</li>
          <li>• <strong>Cost:</strong> $13/month for entire platform (cloud efficiency)</li>
          <li>• <strong>Security:</strong> 4 layers of automated security scanning</li>
        </ul>
      </div>

      <div className="bg-purple-50 border-l-4 border-purple-500 p-4">
        <h3 className="font-bold text-purple-900 mb-2">🚀 Key Differentiators</h3>
        <ul className="text-sm space-y-1 text-purple-800">
          <li>• <strong>AI-Augmented:</strong> Not just ML deployment - AI operates the platform</li>
          <li>• <strong>Hybrid Architecture:</strong> Mirrors enterprise patterns (edge computing)</li>
          <li>• <strong>DevSecOps:</strong> Security integrated, not bolted on</li>
          <li>• <strong>Cloud-Agnostic:</strong> Portable to AWS, Azure, on-prem</li>
          <li>• <strong>Complete System:</strong> End-to-end, not just a tutorial</li>
        </ul>
      </div>
    </div>
  );

  const FlowVisualization = ({ flow }) => {
    const flowData = flows[flow];
    return (
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-gray-800">{flowData.title}</h3>
        <div className="space-y-3">
          {flowData.steps.map((step, idx) => (
            <div key={idx}>
              <div className="flex items-start gap-3 bg-white p-4 rounded-lg border-2 border-gray-200 hover:border-blue-400 transition-all">
                <step.icon className={`w-6 h-6 text-${flowData.color}-600 flex-shrink-0 mt-1`} />
                <div className="flex-1">
                  <h4 className="font-bold text-gray-900">{step.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{step.desc}</p>
                  <p className="text-xs text-gray-500 mt-2 italic">{step.detail}</p>
                </div>
              </div>
              {idx < flowData.steps.length - 1 && (
                <div className="flex justify-center py-2">
                  <ArrowRight className="w-5 h-5 text-gray-400" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gradient-to-br from-gray-50 to-blue-50 min-h-screen">
      <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          AI-Augmented MLOps Platform
        </h1>
        <p className="text-gray-600 mb-6">
          Interactive guide to understanding your hybrid, self-healing ML platform
        </p>

        <div className="flex gap-2 mb-6 flex-wrap">
          <button
            onClick={() => { setActiveView('overview'); setSelectedFlow(null); }}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeView === 'overview' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => { setActiveView('architecture'); setSelectedFlow(null); }}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeView === 'architecture' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Architecture
          </button>
          <button
            onClick={() => { setActiveView('flows'); setSelectedFlow(null); }}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeView === 'flows' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Flows
          </button>
          <button
            onClick={() => { setActiveView('value'); setSelectedFlow(null); }}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeView === 'value' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Value Props
          </button>
        </div>

        <div className="bg-gray-50 rounded-lg p-6">
          {activeView === 'overview' && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Project Overview</h2>
              
              <div className="bg-blue-50 border-l-4 border-blue-600 p-4">
                <h3 className="font-bold text-blue-900 mb-2">🎯 Core Purpose</h3>
                <p className="text-gray-700">
                  Build a fully automated MLOps platform that uses <strong>AI to operate itself</strong>. 
                  When models fail, pipelines break, or performance degrades, Gemini AI automatically 
                  analyzes the issue and provides actionable remediation steps.
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg border-2 border-gray-200">
                  <h4 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Server className="w-5 h-5 text-blue-600" />
                    Infrastructure
                  </h4>
                  <ul className="text-sm space-y-1 text-gray-600">
                    <li>• <strong>GCP e2-small:</strong> Control plane (k3s)</li>
                    <li>• <strong>Windows k3d:</strong> Data plane (ML workloads)</li>
                    <li>• <strong>Tailscale:</strong> Secure VPN connectivity</li>
                    <li>• <strong>Cost:</strong> $13/month total</li>
                  </ul>
                </div>

                <div className="bg-white p-4 rounded-lg border-2 border-gray-200">
                  <h4 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-orange-600" />
                    Automation
                  </h4>
                  <ul className="text-sm space-y-1 text-gray-600">
                    <li>• <strong>GitOps:</strong> ArgoCD (2 clusters)</li>
                    <li>• <strong>CI/CD:</strong> GitHub Actions (7 stages)</li>
                    <li>• <strong>Security:</strong> Bandit, Snyk, Gitleaks, Trivy</li>
                    <li>• <strong>MLOps:</strong> MLflow tracking & registry</li>
                  </ul>
                </div>

                <div className="bg-white p-4 rounded-lg border-2 border-gray-200">
                  <h4 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Eye className="w-5 h-5 text-green-600" />
                    Observability
                  </h4>
                  <ul className="text-sm space-y-1 text-gray-600">
                    <li>• <strong>Prometheus:</strong> Multi-cluster metrics</li>
                    <li>• <strong>Grafana:</strong> Visualization dashboards</li>
                    <li>• <strong>Alertmanager:</strong> Smart alert routing</li>
                    <li>• <strong>Scraping:</strong> Both GCP + k3d via Tailscale</li>
                  </ul>
                </div>

                <div className="bg-white p-4 rounded-lg border-2 border-gray-200">
                  <h4 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Brain className="w-5 h-5 text-purple-600" />
                    AI Intelligence
                  </h4>
                  <ul className="text-sm space-y-1 text-gray-600">
                    <li>• <strong>Model:</strong> Gemini 2.5 Flash Lite</li>
                    <li>• <strong>Use Cases:</strong> 3 operational workflows</li>
                    <li>• <strong>Interface:</strong> REST API (Vertex AI)</li>
                    <li>• <strong>Cost:</strong> $0 (free tier sufficient)</li>
                  </ul>
                </div>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-600 p-4 mt-4">
                <h3 className="font-bold text-yellow-900 mb-2">⚡ Quick Stats</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-yellow-900">2</div>
                    <div className="text-xs text-yellow-700">Kubernetes Clusters</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-yellow-900">7</div>
                    <div className="text-xs text-yellow-700">Pipeline Stages</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-yellow-900">3</div>
                    <div className="text-xs text-yellow-700">AI Workflows</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-yellow-900">60-80%</div>
                    <div className="text-xs text-yellow-700">MTTR Reduction</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeView === 'architecture' && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">System Architecture</h2>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {architectureComponents.map((component, idx) => (
                  <div key={idx} className={`bg-white p-4 rounded-lg border-2 border-${component.color}-200 hover:border-${component.color}-400 transition-all`}>
                    <div className="flex items-center gap-3 mb-3">
                      <component.icon className={`w-8 h-8 text-${component.color}-600`} />
                      <div>
                        <h3 className="font-bold text-gray-900">{component.name}</h3>
                        <p className="text-xs text-gray-500">{component.role}</p>
                      </div>
                    </div>
                    <div className="space-y-1">
                      {component.services.map((service, sidx) => (
                        <div key={sidx} className="text-sm text-gray-600 flex items-center gap-2">
                          <CheckCircle className="w-3 h-3 text-green-600" />
                          {service}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <div className="bg-white p-6 rounded-lg border-2 border-gray-200 mt-6">
                <h3 className="font-bold text-gray-800 mb-3">🔄 How They Connect</h3>
                <div className="space-y-2 text-sm text-gray-700">
                  <p><strong>1. GitOps Flow:</strong> GitHub → ArgoCD (GCP) → Deploys to both GCP & k3d clusters</p>
                  <p><strong>2. Monitoring Flow:</strong> Prometheus (GCP) → Scrapes k3d via Tailscale → Alertmanager → GitHub Actions</p>
                  <p><strong>3. CI/CD Flow:</strong> GitHub Actions → Security scans → MLflow → Build container → Update Git → ArgoCD deploys</p>
                  <p><strong>4. AI Flow:</strong> Alert/Failure → GitHub Actions → Gemini API → Analysis → GitHub Issue</p>
                </div>
              </div>

              <div className="bg-purple-50 border-l-4 border-purple-600 p-4">
                <h3 className="font-bold text-purple-900 mb-2">🏗️ Why Hybrid Architecture?</h3>
                <ul className="text-sm space-y-1 text-purple-800">
                  <li>• <strong>Real-World Pattern:</strong> Many enterprises run control in cloud, workloads on-prem</li>
                  <li>• <strong>Data Sovereignty:</strong> Sensitive data stays on-premises</li>
                  <li>• <strong>Cost Optimization:</strong> Expensive GPU workloads run on owned hardware</li>
                  <li>• <strong>Edge Computing:</strong> ML inference at the edge (IoT devices, factories)</li>
                  <li>• <strong>Cloud-Agnostic:</strong> Not locked into single provider (k3s runs anywhere)</li>
                </ul>
              </div>
            </div>
          )}

          {activeView === 'flows' && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Operational Flows</h2>
              
              {!selectedFlow ? (
                <div className="grid md:grid-cols-2 gap-4">
                  <button
                    onClick={() => setSelectedFlow('deployment')}
                    className="bg-white p-6 rounded-lg border-2 border-blue-200 hover:border-blue-400 transition-all text-left"
                  >
                    <GitBranch className="w-8 h-8 text-blue-600 mb-3" />
                    <h3 className="font-bold text-gray-900 mb-2">Deployment Flow</h3>
                    <p className="text-sm text-gray-600">Code commit → Security → Training → Build → Deploy (7 stages)</p>
                  </button>

                  <button
                    onClick={() => setSelectedFlow('aiMonitoring')}
                    className="bg-white p-6 rounded-lg border-2 border-purple-200 hover:border-purple-400 transition-all text-left"
                  >
                    <Brain className="w-8 h-8 text-purple-600 mb-3" />
                    <h3 className="font-bold text-gray-900 mb-2">AI Monitoring Flow</h3>
                    <p className="text-sm text-gray-600">Alert → Log analysis → Gemini diagnosis → GitHub Issue (5 steps)</p>
                  </button>

                  <button
                    onClick={() => setSelectedFlow('pipelineTriage')}
                    className="bg-white p-6 rounded-lg border-2 border-red-200 hover:border-red-400 transition-all text-left"
                  >
                    <AlertTriangle className="w-8 h-8 text-red-600 mb-3" />
                    <h3 className="font-bold text-gray-900 mb-2">Pipeline Triage Flow</h3>
                    <p className="text-sm text-gray-600">Pipeline fails → Extract logs → AI triage → Fix instructions (5 steps)</p>
                  </button>

                  <button
                    onClick={() => setSelectedFlow('driftDetection')}
                    className="bg-white p-6 rounded-lg border-2 border-orange-200 hover:border-orange-400 transition-all text-left"
                  >
                    <Activity className="w-8 h-8 text-orange-600 mb-3" />
                    <h3 className="font-bold text-gray-900 mb-2">Drift Detection Flow</h3>
                    <p className="text-sm text-gray-600">Metrics → Calculate drift → AI classify → Remediation plan (5 steps)</p>
                  </button>
                </div>
              ) : (
                <div>
                  <button
                    onClick={() => setSelectedFlow(null)}
                    className="mb-4 text-blue-600 hover:text-blue-800 font-medium"
                  >
                    ← Back to all flows
                  </button>
                  <FlowVisualization flow={selectedFlow} />
                </div>
              )}
            </div>
          )}

          {activeView === 'value' && <ValueProps />}
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
        <h2 className="text-2xl font-bold mb-3">🎬 Demo Script Checklist</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <h3 className="font-bold">Technical Demo Points:</h3>
            <ul className="text-sm space-y-1">
              <li>✓ Show ArgoCD UI (both clusters synced)</li>
              <li>✓ Show Prometheus targets (multi-cluster)</li>
              <li>✓ Show MLflow experiments</li>
              <li>✓ Trigger pipeline (watch stages)</li>
              <li>✓ Show security scan results</li>
              <li>✓ Demo AI log analysis workflow</li>
              <li>✓ Show GitHub Issue with AI insights</li>
            </ul>
          </div>
          <div className="space-y-2">
            <h3 className="font-bold">Key Messages:</h3>
            <ul className="text-sm space-y-1">
              <li>✓ AI reduces MTTR by 60-80%</li>
              <li>✓ Hybrid architecture (enterprise pattern)</li>
              <li>✓ GitOps = audit trail + reliability</li>
              <li>✓ Security integrated (not bolted on)</li>
              <li>✓ $13/month = cost efficiency</li>
              <li>✓ Cloud-agnostic (portable)</li>
              <li>✓ Production-grade observability</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MLOpsPlatformExplainer;