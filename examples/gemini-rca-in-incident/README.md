# End-to-End Example: Incident → Gemini RCA → Quality Gate Recommendation

This example shows the full flow of using AI for automated incident analysis and quality gate improvement.

## Workflow
1. **Cloud Logging incident occurs**: A high error rate is detected on a GKE pod.
2. **Gemini RCA Agent analyzes logs**: The agent processes the last 50 log entries to find patterns.
3. **Recommends quality gate + fix**: The agent identifies a missing resource limit and suggests adding Chaos testing.
4. **Links to Production Readiness Checklist**: The findings are used to update the [Production Readiness Checklist](../../patterns/production-readiness-checklist.md).

**Status**: Working demonstration using the scripts in `frameworks/gemini-agent-qe/tools/`.
