# Chaos Experiments

**GKE Pod Kill** — Tests application resilience to pod evictions (very common in GKE).

**How to Run**:
1. Install Chaos Mesh on your cluster
2. `kubectl apply -f gke-pod-kill.yaml`
3. Monitor impact using Cloud Monitoring SLOs
