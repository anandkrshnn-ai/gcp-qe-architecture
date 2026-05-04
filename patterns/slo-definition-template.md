# SLO Definition Template

**Service**: [Name of the service]
**SLI**: [Availability | Latency | Throughput | Success Rate]
**SLO Target**: 99.5%
**Error Budget**: 0.5% (approx 13 minutes/month for 99.5%)
**Measurement Period**: 28 days (rolling)

## SLI Details
- **Good Events**: Successful requests (HTTP 2xx, 3xx)
- **Total Events**: All valid requests
- **Filter**: `metric.type="run.googleapis.com/request_count" resource.type="cloud_run_revision"`
