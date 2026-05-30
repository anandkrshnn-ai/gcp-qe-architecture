This repository provides a clean, simplified educational demonstration for agent safety. To run or adapt these patterns, follow these steps.

## 1. Prerequisites
- Python 3.9+
- `pip install cryptography pydantic cachetools pytest`

## 2. Adapting the Core
The safety mechanisms are located in `src/safety/`. To use them in a simulation or real environment:

### A. Implementing the Analyzer
Replace the deterministic heuristics in `VertexAIAnalyzer` (or your analyzer class) with your own logic (e.g., querying Google Cloud Logging via the Python SDK).

### B. Distributing Keys
In a production setting, agent RSA private keys should be stored in **Secret Manager** or backed by **Cloud KMS**. The `VotingValidator` would be a central service that holds the public keys of authorized agents.

### C. Integrating with Actuators
The `DryRunRemediator` currently prints actions. In production, you would connect this to:
- **Kubernetes Python Client**: To apply patches to GKE.
- **Cloud Run Admin API**: To scale services.
- **Pub/Sub**: To trigger external automation.

## 3. Running Verification
Always run the verification suite before committing any changes:

```bash
python -m pytest
```

## 4. Operational Considerations
- **Voting Quorum Threshold**: Defaults to 66% (2/3). Adjust this in `VotingValidator` based on your needs.
- **Safety Quotas**: Update `SafetyConfig` in `src/safety/safety_gate.py` to match your simulation needs.
