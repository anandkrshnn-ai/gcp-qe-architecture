# Fault Tolerance & Resilience

Distributed systems—especially those relying on external AI APIs—must be designed to handle failure.

## Resilience Strategy

The `VertexAIAnalyzer` implements a multi-layered resilience strategy to ensure that transient failures do not block critical incident remediation.

### 1. Exponential Backoff with Tenacity
We use the `tenacity` library to wrap all real-mode Vertex AI calls. This provides a robust retry mechanism that automatically backs off when encountering quota limits or service interruptions.

**Retry Configuration:**
- **Stop**: After 3 attempts.
- **Wait**: Exponential backoff starting at 2s, capped at 10s.
- **Exceptions**: Retries on all general `Exception` types during the analysis phase.

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def _analyze_real_with_retry(self, logs: List[Dict[str, Any]]) -> List[Finding]:
    return self._analyze_real(logs)
```

### 2. Quota Management (429 Handling)
Vertex AI has strict Rate Limits (RPM/TPM). By implementing retries at the analyzer level, we ensure that occasional `ResourceExhausted` errors are handled transparently without crashing the agent fleet.

### 3. Graceful Fallback
If the consensus quorum fails to reach a decision (e.g., due to AI service unavailability across multiple regions), the `Remediator` defaults to a **SAFE_BLOCK** state, requiring manual human intervention.

## Operational Monitoring

| Metric | Target | Failure Action |
| :--- | :--- | :--- |
| **Analysis Latency** | < 15s | Log warning + Retry |
| **Quota Status** | Healthy | Exponential Backoff |
| **Consensus Success** | > 99% | Notify SRE On-call |
