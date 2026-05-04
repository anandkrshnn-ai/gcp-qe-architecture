# Cloud Run Quality Guide

## Key Quality Practices

- Proper startup + liveness probes
- Resource limits (CPU & Memory)
- Custom metrics for autoscaling
- Traffic splitting for canary releases
- Performance testing with realistic load

## Recommended SLOs
- Availability: 99.5%
- P95 Latency: < 800ms
- Cold start percentage: < 5%
