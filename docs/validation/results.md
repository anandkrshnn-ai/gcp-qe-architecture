# Validation Results

Every release of the incident analysis demo is verified using automated test suites.

## Automated Test Suite

**Last Run**: 2026-05-30  
**Status**: 100% PASSING  

### Execution Summary
The following core modules are verified:
- `voting.py`: Quorum and signature verification.
- `safety_gate.py`: Quota and boundary enforcement.
- `analyzer.py`: Sanitization and AI integration.

```text
tests\post_incident\test_recovery.py ..                                  [ 10%]
tests\pre_actuation\test_adversarial.py ....                             [ 30%]
tests\pre_actuation\test_property_based.py ...                           [ 45%]
tests\pre_deploy\test_authenticity.py ...                                [ 60%]
tests\pre_deploy\test_kms_signer.py ..                                   [ 70%]
tests\pre_deploy\test_safety.py ......                                   [100%]
============================= 20 passed in 7.38s ==============================
```

## Verified Scenarios

We use unit, integration, and property-based tests to verify the following scenarios:

| Scenario | Trigger | Safety Outcome | Status |
| :--- | :--- | :--- | :--- |
| **OOMKill Remediation** | Log: `Critical: OOMKilling pod` | **APPROVED**: Scale-up within quota | ✅ VERIFIED |
| **Credential Leak** | Finding containing `AIza...` | **SANITIZED**: Redacted key | ✅ VERIFIED |
| **Replay Attack** | Used nonce detected in cache | **BLOCKED**: Nonce reused | ✅ VERIFIED |
| **Quota Violation** | Proposed replicas > `max_replicas` | **BLOCKED**: Resource limit exceeded | ✅ VERIFIED |
| **Signature Forgery** | Tampered JSON payload | **BLOCKED**: Invalid signature | ✅ VERIFIED |

## Performance Benchmarks

| Operation | Latency (Simulated) | Latency (Real Gemini) |
| :--- | :--- | :--- |
| **Analysis** | < 10ms | 4s - 8s |
| **Quorum Check** | < 5ms | N/A (Local Cryptography) |
| **Safety Gate** | < 1ms | N/A (Deterministic) |
