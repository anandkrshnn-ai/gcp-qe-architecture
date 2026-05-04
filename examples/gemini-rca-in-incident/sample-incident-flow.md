# Sample Incident Flow

**Incident**: High error rate on GKE pod (Error code 137 / OOMKill)

**Gemini RCA Output**:
- **Root Cause**: Missing resource limits in the Kubernetes Deployment manifest causing a memory-leaking container to starve other pods.
- **Confidence**: 95%
- **Recommended Gate**: Add **k6 Performance testing** (memory leak detection) + **Chaos Mesh pod-kill** experiment.
- **Suggested Fix**: Update Deployment spec with `resources.requests` and `resources.limits`.
- **Reasoning**: Log entries show multiple `OOMKill` events followed by container restarts. Performance metrics show steady memory growth over 6 hours.

## Action Taken
1. Added resource limits to `terraform-baseline/modules/gke/`.
2. Updated the [Production Readiness Checklist](../../patterns/production-readiness-checklist.md) to include mandatory resource limit validation.
3. Scheduled a Chaos experiment to validate container restart behavior.
