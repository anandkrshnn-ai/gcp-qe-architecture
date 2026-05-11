# Proving Grounds: Validating Production Reality

To reach a **95+/100** score, this repository must move from "Simulation" to "Verified Execution." This document outlines how to generate the evidence required to prove this system is battle-ready.

## 1. Live GKE Log Verification
To prove the `SovereignClient` handles real GCP data:
1. **Authenticate**: Run `gcloud auth application-default login`.
2. **Execute**: Run `python run_demo.py --scenario oomkill --mode hybrid`.
3. **Evidence**: Capture the terminal output where the client successfully initializes the `google-cloud-logging` SDK and retrieves real results. 

## 2. Terraform Plan Validation
To prove the IaC is deployable:
1. **Init**: `cd terraform && terraform init`.
2. **Plan**: `terraform plan -out=tfplan`.
3. **Show**: `terraform show -no-color tfplan > ../evidence/TERRAFORM_PLAN_VALIDATED.txt`.

## 3. OpenTelemetry Trace Evidence
To prove observability:
1. **Run**: Execute the analyzer.
2. **Evidence**: Capture the console output showing the `Trace ID` (e.g., `tr-1778436169`) and span markers.

## 4. Full OODA Loop Demonstration
To prove the Actuator:
1. **Dry-Run**: Run the full demo.
2. **Evidence**: The output must show the generated `kubectl patch` command correctly mapping to the detected `oomkill` root cause.

## 5. Formal Safety & Epistemic Validation (Wave 3)
To satisfy a Principal Architect-level audit, we prove the system handles platform-level failure modes and uncertainty:

1.  **Remote Attestation & Identity**:
    - **Evidence**: Captured JWT Handshake proving Root of Trust verification before log access.
2.  **Uncertainty Quantification (The Oracle Fix)**:
    - **Scenario**: `uncertain_oom`.
    - **Evidence**: `ConflictScore: 60%` reported. Agent correctly aborts remediation due to conflicting evidence (Batch Job vs OOM).
3.  **Platform Event Awareness**:
    - **Scenario**: `platform_outage`.
    - **Evidence**: Agent detects 3+ sibling failures and enters `FREEZE_MODE`. Action aborted to prevent local interference with a platform-wide issue.
4.  **Honeymoon Period (Discovery Mode)**:
    - **Scenario**: `new_resource`.
    - **Evidence**: Agent refuses remediation for a resource seen for the first time, enforcing a mandatory learning baseline.
5.  **DeepScrub & Tracing**:
    - **Evidence**: Recursive PII redaction verified and all Epistemic decisions mapped to unique OTLP-style Trace IDs.

---

### 🛡️ The "Principal's Pledge"
By completing these validation steps, you demonstrate not just the ability to write code, but the **Operational Discipline** required to manage production infrastructure at scale.
