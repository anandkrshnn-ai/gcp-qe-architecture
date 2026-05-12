# Property-Based Testing

Standard unit tests only verify what the developer expects. **Property-Based Testing** verifies the system against thousands of randomized adversarial scenarios.

## Overview

We use the `Hypothesis` library to prove that the `ConsensusGuardian` and `SafetyGate` are resilient under extreme conditions. Instead of testing a single static finding, we generate thousands of randomized finding objects with varying timestamps, nonces, and signatures.

## Key Properties Verified

### 1. Temporal Drift Resilience
**Property**: The system must reject any proposal where the timestamp drift exceeds ±60 seconds from "now."
- **Verification**: Hypothesis generates valid and invalid timestamps across a wide range. The guardian correctly identifies and rejects the drifts.

### 2. Signature Integrity
**Property**: Any modification to the signed finding JSON (even a single character) must result in a signature verification failure.
- **Verification**: We generate valid signatures and then programmatically "tamper" with the payload. The system is proven to block all tested tamper scenarios.

### 3. Nonce Collision Resistance
**Property**: Reusing a nonce within the TTL window must trigger a mandatory block.
- **Verification**: Hypothesis simulates concurrent requests with duplicate nonces. The `TTLCache` prevents command-injection via replay attacks.

## Why This Matters

For autonomous agents, "edge cases" are the norm. By using property-based testing, we achieve:
- **Verified Resilience**: 1,000+ test cases per property covering extreme input ranges.
- **Adversarial Hardening**: Discovery of logic flaws that manual unit tests often miss.
- **Traceable Assurance**: Moving from "it works in simulation" to "**demonstrably sound under tested properties**."

```python
# Example Hypothesis Test (Simplified)
@given(st.integers(min_value=1, max_value=1000))
def test_quorum_thresholds(n):
    # Proves quorum logic consistency for 'n' agent signatures
    ...
```
