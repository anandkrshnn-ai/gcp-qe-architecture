# Chaos Experiments

- **GKE Pod Kill** — Tests application resilience to pod evictions (very common in GKE).
- **Network Latency** — Simulates inter-service latency in GKE clusters.
- **Cloud SQL Failover** — Validates application recovery during database failover events.

**How to Run**:
1. Install Chaos Mesh on your cluster
2. `kubectl apply -f [experiment].yaml`
3. Monitor impact using Cloud Monitoring SLOs
