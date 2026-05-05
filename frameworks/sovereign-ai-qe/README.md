# Sovereign AI RCA - Proof of Concept (PoC)

This prototype demonstrates how to perform Root Cause Analysis (RCA) on production logs using a **Sovereign AI stack** (Local LLM) combined with the **PTV (Private Trust Verification)** protocol.

## Why Sovereign AI?
- **Data Privacy**: Logs never leave the secure VPC boundary.
- **Compliance**: PTV provides a cryptographic audit trail of the analysis.
- **Independence**: No reliance on third-party API availability.

## Running the PoC (Local Mode)

1. **Install Ollama** (representing our Sovereign Inference Server):
   `brew install ollama` (or visit ollama.com)
2. **Pull a Sovereign Model**:
   `ollama pull llama3`
3. **Run the RCA Agent**:
   ```bash
   python frameworks/sovereign-ai-qe/tools/sovereign-rca-agent.py --logs sample_logs.json
   ```

## Architecture (GKE Deployment)
In a production sovereign environment, this agent runs on GKE GPU nodes:
- **Inference Server**: vLLM serving Llama-3-8B.
- **Attestation**: A sidecar container generating PTV manifests for each analysis.

## Sample PTV Attestation (Metadata)
```json
{
  "ptv_id": "ptv-98234-xyz",
  "model": "sovereign-llama3-8b",
  "log_hashes": ["sha256:8f92..."],
  "analysis_timestamp": "2026-05-05T12:00:00Z",
  "sovereign_boundary": "gcp-asia-south1-private-vpc",
  "integrity_status": "VERIFIED"
}
```
