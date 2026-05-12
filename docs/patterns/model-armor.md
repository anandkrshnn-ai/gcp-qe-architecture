# Model Armor & Sanitization

The **Model Armor** layer provides real-time leak detection and output sanitization for agent-generated findings.

## Overview

Agentic outputs can inadvertently contain sensitive information, such as PII, internal IP addresses, or GCP API keys. The Model Armor layer acts as a "Safety Proxy" that sanitizes the finding before it is signed by the agent and sent to the consensus layer.

## Key Features

### 1. Leak Shield (Secret Redaction)
The armor scans all fields in a `Finding` for common secret patterns using high-fidelity regex scanning. 
- **GCP API Keys**: Detected via `AIza...` patterns.
- **Service Account Credentials**: Scanned for identifiable JSON fragments.
- **OpenAI Keys**: Scanned for `sk-...` prefixes.

Any detected secrets are surgically replaced with a `[REDACTED_SECRET]` placeholder.

### 2. Output Truncation & Normalization
To prevent large payloads or malformed text from breaking the consensus hash, the Model Armor layer normalizes text fields and truncates long descriptions to a safe, canonical length.

### 3. Safety Scoring
Every sanitized finding is assigned a `safety_score` (0.0 - 1.0) and an `armor_status`. This metadata is stored in the finding's `metadata` field, allowing the `ConsensusGuardian` to reject proposals that haven't been "Verified Clean."

## Implementation Pattern

The `ModelArmor` is integrated directly into the `VertexAIAnalyzer` pipeline:

```python
# Analysis Phase
raw_finding = self._generate_finding(logs)

# Sanitization Phase
clean_finding = self.armor.sanitize_finding(raw_finding)

# Signing Phase
signed_package = self.sign_finding(clean_finding)
```

## Status

| Pattern | Status | Integrity |
| :--- | :--- | :--- |
| **Secret Scanning** | ACTIVE | Regex Redaction |
| **PII Filtering** | PLANNED | Vertex AI Safety Filters |
| **Audit Compliance** | VERIFIED | Metadata Injection |
