# Multi-Agent Cryptographic Consensus

This pattern ensures that no single autonomous agent can trigger state-changing operations without a verified quorum from the fleet.

## Overview

In high-stakes environments, relying on a single AI model (even Gemini 1.5 Pro) introduces risks of hallucinations or unintended tool use. The **Cryptographic Consensus** pattern requires a 2/3 majority (or configurable threshold) of independent signatures before a remediation proposal is considered valid.

## Implementation Details

### RSA-PSS Signing
Agents utilize RSA private keys to sign remediation proposals. The signing process is hardened against tampering:
- **Canonical JSON**: Proposals are serialized with sorted keys and no whitespace (`separators=(',', ':')`) to ensure hash stability across nodes.
- **SHA-256 Hashing**: The message digest is generated from the canonical JSON string.
- **PSS Padding**: Probabilistic Signature Scheme (PSS) is used for maximum security.

### Replay Protection
To prevent a malicious actor from re-submitting a previously signed finding, each proposal includes:
- **Nonce**: A 16-byte cryptographically secure random hex string.
- **TTL Cache**: The `ConsensusGuardian` maintains a 5-minute `TTLCache`. Any proposal re-using a nonce within this window is rejected with a `403 Forbidden` status.

### Temporal Integrity
All timestamps are strictly cast to `int` (Unix epoch) to eliminate floating-point precision mismatches between signing and verification nodes.

## Safety Outcomes

| Feature | Protection Provided |
| :--- | :--- |
| **Quorum Gate** | Prevents single-agent takeover or hallucination. |
| **RSA-PSS** | Ensures non-repudiability and tampering detection. |
| **Nonce Gate** | Blocks command-injection via replay attacks. |

```python
# Example Consensus Check
guardian.verify_quorum(proposal, signatures)
```
