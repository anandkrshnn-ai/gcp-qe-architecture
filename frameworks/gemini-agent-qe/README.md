# Gemini Agent Quality Engineering

Uses **Gemini 3.1 Pro** for intelligent Root Cause Analysis on GCP logs.

**Status**: Working prototype

### How to Run
```bash
pip install google-cloud-logging vertexai
python tools/gemini-rca-agent.py
```

### Integration Examples
See [examples/gemini-rca-in-incident/](../../examples/gemini-rca-in-incident/) for a full incident-to-remediation workflow using this agent.
