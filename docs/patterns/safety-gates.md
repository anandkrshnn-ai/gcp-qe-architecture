# Deterministic Safety Gates

While consensus ensures that agents agree on an action, **Safety Gates** ensure that the action is safe for the infrastructure.

## Overview

A Safety Gate is a final, deterministic validation step that occurs after consensus is reached but before the actuator (Remediator) executes the code. It enforces hard boundaries on resource usage, cost, and operational scale.

## Core Mechanisms

### 1. Resource Quotas
The gate validates proposals against strict limits defined in the `SafetyConfig`. Common quotas include:
- **Max Replicas**: Prevents runaway scaling events that could exhaust project budget or quota.
- **Max Scale Factor**: Limits the percentage increase in resource allocation per single remediation event.

### 2. Operational Allow-List
Only pre-approved operations (e.g., `SCALE_UP`, `RESTART`, `NOTIFY`) are permitted. Destructive operations like `DELETE` or `PURGE` are blocked by default unless explicitly whitelisted in the production configuration.

### 3. Cost Guardrails
The gate estimates the cost impact of the proposed remediation. If the `estimated_cost` exceeds the `max_estimated_cost` defined in the environment, the action is blocked for human review.

## Gate Result Object

The `SafetyGate` returns a rich `GateResult` object, providing full observability into the decision-making process:

| Field | Description |
| :--- | :--- |
| `success` | Boolean indicating if the gate passed. |
| `risk_score` | A float (0.0 - 1.0) calculated based on operation impact. |
| `message` | Human-readable reason for the decision. |
| `blocked_operation` | The specific field or value that triggered a rejection. |

## Configuration Example

```python
config = SafetyConfig(
    max_replicas_per_service=20,
    max_estimated_cost=50.0,
    allowed_operations=["SCALE_UP", "NOTIFY"]
)
gate = SafetyGate(config)
```
