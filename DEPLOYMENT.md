# Deploying Safety Patterns (GCP)

This repository provides an **Architectural Reference** for agent safety. It is a research PoC, not a production-ready product. To adapt these patterns to your own Google Cloud environment, follow these steps.

## 1. Prerequisites
- Python 3.9+
- `pip install cryptography pydantic pytest`

## 2. Adapting the Core
The safety mechanisms are located in `src/safety_core/`. To use them in a real environment:

### A. Implementing the Analyzer
Replace the deterministic heuristics in `SafetyAnalyzer.analyze_logs` with your own logic (e.g., querying Cloud Logging via the Python SDK).

### B. Distributing Keys
In a production setting, agent RSA private keys should be stored in **Secret Manager** or backed by **Cloud HSM**. The `ConsensusGuardian` would be a central service (or distributed cluster) that holds the public keys of authorized agents.

### C. Integrating with Actuators
The `SafetyRemediator` currently logs actions. In production, you would connect this to:
- **Kubernetes Python Client**: To apply patches to GKE.
- **Cloud Run Admin API**: To scale services.
- **Pub/Sub**: To trigger external automation.

## 3. Running Verification
Always run the verification suite before deploying any changes to the safety core:

```bash
$env:PYTHONPATH = "src"
python -m pytest tests/test_safety_core.py
```

## 4. Operational Considerations
- **Quorum Threshold**: Defaults to 66% (2/3). Adjust this in `ConsensusGuardian` based on your fleet size.
- **Safety Quotas**: Update `SafetyConfig` in `src/safety_core/safety_gate.py` to match your organization's risk tolerance.
