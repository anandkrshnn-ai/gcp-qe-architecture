# Multi-Agent Voting: Identity & Verification

The voting pattern simulates how autonomous remediation actions can require a **multi-agent, verifiable vote** before execution.

## 1. Identity Propagation & Workload Identity
In this demonstration, each agent is associated with an identity.
- **Verification**: The `VotingValidator` verifies that the `agent_id` in the signature matches the registered agent.
- **Benefit**: Ensures only authorized agents can vote on incident analysis proposals.

## 2. Key Lifecycle & Secret Management
Private keys can be backed by Google Cloud KMS or stored in Secret Manager.
- **Storage**: Keys are provisioned as RSA keys.
- **Cloud KMS Integration**: The KMS signer supports signing digests using Google Cloud KMS asymmetric keys with local fallback for local development or sandbox simulations.

## 3. Quorum Dynamics
The voting threshold is proportional to the registered agents.
- **Quorum**: A proposal is approved only if a majority (e.g. 66%) of registered agents provide valid signatures.

## 4. Compliance Evidence
Voting results are serialized into **Canonical JSON** and logged. This provides a timeline of:
1. Who proposed the action.
2. Who voted / signed it.
3. The exact proposal state.
