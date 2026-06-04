# Cloud Run Quality & Performance Guide

## Production-Grade Configuration
To achieve the performance stability discussed in the [Case Study](../case-studies/cloud-run-performance-stabilization.md), use the following hardened settings in your Terraform/Service manifest.

### 1. Concurrency & Scaling
- **Max Instances**: Always set a `max_instance` limit to prevent runaway costs during DDoS or misconfiguration.
- **Concurrency**: Tune `container_concurrency` based on your language's threading model. For Node.js/Go, 80-100 is often a good start.
- **Min Instances**: Set `min_instances > 0` for critical services to eliminate cold starts for P99 latency sensitive workloads.

### 2. Resource Limits
```hcl
resources {
  limits = {
    cpu    = "1000m"
    memory = "512Mi"
  }
}
```

### 3. Probes
Always implement both `startupProbe` and `livenessProbe`. Startup probes are critical for heavy applications to prevent Cloud Run from killing the container before it's ready.

## Performance Testing Strategy (k6)
Don't just test the `/health` endpoint.
- **Scenario A: Cold Start Testing**: Deploy with 0 min-instances and hit an endpoint with a heavy dependency.
- **Scenario B: Burst Scaling**: Use k6 `ramping-arrival-rate` to see how fast Cloud Run scales instances.

## Quality Gates
- **Latency Gate**: P95 < 500ms under 50 req/sec.
- **Error Gate**: < 1% 5xx errors during scaling events.
