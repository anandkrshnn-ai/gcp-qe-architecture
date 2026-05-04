# Canary Deployment Pattern

A canary deployment pattern to minimize risk by rolling out changes to a small subset of users before full release.

## Implementation (Cloud Run)
- Use Cloud Run Traffic Splitting.
- **Phase 1**: 10% traffic to new revision.
- **Phase 2**: 50% traffic if Golden Signals are stable.
- **Phase 3**: 100% traffic after 1 hour of stable performance.

## Quality Gates
- Monitor Error Rate (must be < 0.1% increase).
- Monitor P95 Latency (must be < 10% increase).
- Run Gemini RCA Agent on canary logs during rollout.
