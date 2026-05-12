# Deterministic Safety Gates: Operational Hardening

Safety Gates are the final line of defense. While consensus ensures agreement, the **Safety Gate** enforces the **physical and fiscal constraints** of the enterprise infrastructure.

## Operational Constraints

### 1. Failure Domains & Regional Isolation
In a production GKE environment, Safety Gates are deployed as **Regional single-tenant controllers**.
- **Constraint**: A Safety Gate in `us-central1` cannot authorize remediation actions in `europe-west1`. This prevents cross-region failure propagation during a systemic agent hallucination.
- **Resilience**: If the global consensus plane is unreachable, the Safety Gate defaults to a **Fail-Safe "Block-All" state** for state-changing operations, while allowing "Read-Only" observability.

### 2. Decision SLOs
To avoid introducing significant latency into the remediation OODA loop:
- **Target Latency**: 95th percentile decision time must be **< 200ms**.
- **Metric**: `safety_gate_decision_latency_seconds` (Prometheus/Cloud Monitoring).

## Resource & Fiscal Boundaries

### 1. Fiscal Guardrails (Cost Envelopes)
The gate doesn't just check "can we scale," but "should we spend."
- **Reference**: Integrates with **BigQuery Billing Exports** (via safety-config) to verify if the proposed `estimated_cost` exceeds the remaining daily budget for the specific `cost-center` tag.
- **Limit**: $50.00 max per automated remediation event without human override.

### 2. Quota-Aware Scaling
- **Hard Limit**: Cannot exceed 80% of the GCP project's current CPU/Memory quota. This preserves "headroom" for manual SRE emergency response.

## Environment Promotion Strategy

| Environment | Default Policy | Human Approval Gate |
| :--- | :--- | :--- |
| **Development** | ALLOW-ALL (Logged) | None |
| **Staging** | STRICT (Quota Only) | Required for > 2x Scale |
| **Production** | DENY-BY-DEFAULT | Required for ALL destructive ops |

## Implementation Traceability

All gate decisions are emitted as **Structured JSON Logs** to Cloud Logging with the `gate_verdict` field. This allows for immediate auditing via Logs Explorer:
`jsonPayload.gate_verdict="BLOCKED" AND jsonPayload.reason:"Cost"`
