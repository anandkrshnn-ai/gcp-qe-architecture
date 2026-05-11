# Operational Runbook: Sovereign-GCP (v0.1.0)

This runbook defines the **Operational Contract** between the Sovereign Engine and the Cloud Operators. It specifies the "Steering and Braking" parameters for autonomous remediation.

---

## 1. The Operational Contract (SLO/SLA)

| Condition | Automatic Response | Escalation Path | Max Time to Escalate |
|-----------|--------------------|-----------------|----------------------|
| **Conflict Score > 0.4** | `MONITOR_AND_WAIT` | Log only (Slack) | N/A |
| **Conflict Score > 0.7** | `ABORT_ACTION` | PagerDuty (Low) | 5 mins |
| **Strike Threshold (3)** | `PERMANENT_FREEZE` | PagerDuty (High) | 2 mins |
| **Pipeline Skew (>60s)** | `MONITOR_AND_WAIT` | Log only | N/A |
| **Persistent Skew (5x)** | `FREEZE_PIPELINE` | PagerDuty (Critical) | 2 mins |
| **Stabilization Fail (2x)** | `DISABLE_RESOURCE` | PagerDuty (Critical) | 5 mins |

---

## 2. Resource-Typed Stabilization
We do not use a "one-size-fits-all" verification. Stabilization windows are scaled by the complexity of the resource state.

| Resource Type | Cycles | Interval | Total Window | Rationale |
|---------------|--------|----------|--------------|-----------|
| **Memory/CPU** | 3 | 10s | 30s | Rapid signal feedback. |
| **Zone/Network**| 6 | 30s | 3 mins | High propagation delay. |
| **DB/Data** | 10 | 5s | 50s | High frequency state check. |

---

## 3. Strike Decay & Half-Life
Strikes represent "active warnings" against a resource. To prevent permanent paralysis from transient history, we use **Exponential Decay**.

*   **Half-Life**: 1 Hour. A strike's "weight" halves every hour the resource remains healthy.
*   **Strike Reset**: If `Current_Strikes < 0.5`, the Safety Gate fully clears the history for that resource.
*   **Manual Override**: Operators can call `sovereign --reset-strikes <resource_id>` to force-clear history.

---

## 4. Security & Attestation
*   **Session TTL**: 15 minutes.
*   **Capability Scoping**: Tokens are issued with the minimal capability set required for the specific agent role (e.g., `REMEDIATE_MEMORY`).
*   **Anomaly Rotation**: The session is **immediately rotated** if:
    *   The agent attempts to access a resource outside its scope.
    *   A conflict score of 1.0 is reached (Suspicious Evidence).
    *   Unauthorized network egress is detected.

---

## 6. The 'Loophole' Safeguards (Wave 6)

### L1: Triple-Source Validation
To prevent **False Agreement** between logs and metrics, the agent now validates against a third, independent oracle (GCP Cloud Audit Logs). 
*   **Trigger**: If Logs+Metrics agree but Audit Logs DISAGREE, Conflict Score is forced to 0.9.

### L2: Oscillation Detection
To prevent **Looping Remediations** on memory leaks or thundering herds:
*   **Logic**: If a resource has failed within the last 5 minutes, the Stabilization Window is **doubled** (N=6 or N=20).

### L3: Blind-Wait Escalation
*   **Timeout**: If `MONITOR_AND_WAIT` persists for >10 cycles (~5 mins), the system declares a `PIPELINE_STORM` and freezes all autonomous activity.

### L10: Admission Control
*   **Cap**: Max 10 concurrent remediation actions. 
*   **Priority**: High-criticality resources (Zones, DBs) preempt batch workloads in the queue.

### L11: Immutable Audit Log (WAL)
Every state change is recorded as an **Immutable Event**.
*   **Audit**: Run `sovereign-log --replay <timestamp>` to verify decision logic.

### L1: Force-Sync Reconciliation
*   **Trigger**: Any `MONITOR_AND_WAIT` period > 10 cycles (~5 mins) triggers an automatic **Force-Sync**.
*   **Action**: The agent bypasses the telemetry pipeline and queries the GCP Resource Manager API directly for the source of truth.

### L3: Signed State (Byzantine Integrity)
*   **Verification**: The State Store view materializer rejects any entry that lacks a valid HMAC/RSA signature from the agent's TEE hardware key.
*   **Security**: Forging strikes or statuses in the database will trigger an immediate `BYZANTINE_TAMPER` quarantine.

### BFT-1: Fleet Quorum Consensus
*   **Threshold**: All remediation actions require signatures from `(2f + 1)` agents (e.g., 3 of 4).
*   **Safety**: A single compromised agent cannot execute unauthorized actions or bypass safety gates.

### BFT-2: State Equivocation Detection
*   **Verification**: Agents perform **Quorum Reads** across state replicas. If replica hashes disagree, the agent triggers a `STATE_EQUIVOCATION` alarm and freezes.

### BFT-6: Merkle-Chained Audit Log
*   **Structure**: Every entry in the Write-Ahead Log (WAL) contains the hash of the previous signature.
*   **Integrity**: Historical record tampering is detectable by any fleet node during synchronization.

### BFT-9: Proof-of-Execution
*   **Receipt**: Followers must return a **Signed Execution Receipt** (hashed from the Cloud API's actual response).
*   **Validation**: The Leader rejects any "Lazy Follower" (BFT-9) that acknowledges receipt but fails to prove execution.
