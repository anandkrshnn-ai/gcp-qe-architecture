# GKE Testing & Resilience Guide

## Hardened GKE Configuration
Based on the [Resilience Case Study](../case-studies/gke-resilience-improvement.md).

### 1. Pod Disruption Budgets (PDB)
Mandatory for all production workloads to ensure availability during node upgrades.
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: frontend-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: frontend
```

### 2. Resource Quotas & Limits
Never deploy without `requests` and `limits`. The [Gemini RCA Agent](../frameworks/gemini-agent-qe/) frequently identifies missing limits as the root cause of OOMKill incidents.

## Chaos Engineering with Chaos Mesh
Implement these experiments to validate GKE resilience:
1. **PodKill**: Randomly kill 20% of pods to verify PDB and deployment controller behavior.
2. **Network Latency**: Inject 200ms latency between frontend and backend services to test timeout handling.

## Automated Validation
Use `gatekeeper` or `datree` in CI to enforce these rules before `kubectl apply`.
