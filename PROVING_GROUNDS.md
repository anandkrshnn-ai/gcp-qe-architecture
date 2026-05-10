# Proving Grounds: Validating Production Reality

To reach a **95+/100** score, this repository must move from "Simulation" to "Verified Execution." This document outlines how to generate the evidence required to prove this system is battle-ready.

## 1. Live GKE Log Verification
To prove the `SovereignClient` handles real GCP data:
1. **Authenticate**: Run `gcloud auth application-default login`.
2. **Execute**: Run `python run_demo.py oomkill --reasoning`.
3. **Evidence**: Capture the terminal output where the client successfully initializes the `google-cloud-logging` SDK and retrieves real results. 
   - *Save this as `evidence/LIVE_LOG_VERIFICATION.txt`.*

## 2. Terraform Plan Validation
To prove the IaC is deployable:
1. **Init**: `cd terraform && terraform init`.
2. **Plan**: `terraform plan -out=tfplan`.
3. **Show**: `terraform show -no-color tfplan > ../evidence/TERRAFORM_PLAN_VALIDATED.txt`.
   - *This proves the modules are structurally sound against the GCP provider.*

## 3. OpenTelemetry Trace Evidence
To prove observability:
1. **Setup**: Configure an OTLP exporter to Google Cloud Trace.
2. **Run**: Execute the analyzer.
3. **Evidence**: Take a screenshot of the **Cloud Trace Waterfall** showing the `analyze_incident` span.
   - *Save this as `evidence/OTEL_TRACE_SNAPSHOT.png`.*

## 4. Full OODA Loop Demonstration
To prove the Actuator:
1. **Dry-Run**: Run the full demo.
2. **Evidence**: The output must show the generated `kubectl patch` command correctly mapping to the detected `oomkill` root cause.

---

### 🛡️ The "Principal's Pledge"
By completing these four validation steps, you demonstrate not just the ability to write code, but the **Operational Discipline** required to manage production infrastructure at scale.
