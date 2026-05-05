# Architecture Decision Record (ADR)

**ADR-[NUMBER]: [SHORT TITLE OF DECISION]**

| Field | Value |
|-------|-------|
| **Status** | Proposed / Accepted / Deprecated / Superseded |
| **Date** | YYYY-MM-DD |
| **Author(s)** | Name(s) |
| **Reviewers** | Name(s) |
| **Supersedes** | ADR-[NUMBER] (if applicable) |

---

## Context

*Describe the situation, problem, or requirement that necessitated a decision. Include relevant constraints:*

- *Technical constraints (existing systems, language choices, platform limitations)*
- *Business constraints (timeline, budget, compliance requirements)*
- *Organizational constraints (team skills, operational capacity)*
- *Non-functional requirements at stake (performance targets, SLO implications)*

*Example: Our Cloud Run services are experiencing cold start latency spikes that breach the P95 < 500ms SLO. We need to decide how to mitigate this while balancing cost (min-instances > 0 incur idle charges) with reliability.*

---

## Decision

*State the decision made. Be specific and unambiguous. This section should be readable in isolation.*

**We will [action] by [mechanism] to [outcome].**

*Example: We will set `min_instances = 1` on all Tier 1 Cloud Run services and `min_instances = 0` on Tier 2/3 services, enforced via a Terraform module variable with a required justification comment for any override.*

---

## Options Considered

### Option 1: [Name]
**Description**: [What this option entails]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Estimated Impact**: [Performance / Cost / Operational complexity]

---

### Option 2: [Name]
**Description**: [What this option entails]

**Pros**:
- [Advantage 1]

**Cons**:
- [Disadvantage 1]

**Estimated Impact**: [Performance / Cost / Operational complexity]

---

### Option 3: [Name] *(if applicable)*
**Description**: [What this option entails]

---

## Rationale

*Explain why the chosen option was selected over the alternatives. Reference specific constraints from the Context section. Include any data, benchmarks, or proof-of-concepts that supported the decision.*

*Example: Option 1 was selected because our load testing showed P95 latency of 2.4s with min_instances=0 and 142ms with min_instances=1 under representative Tier 1 traffic patterns. The cost delta is $X/month, which is justified by the SLO compliance requirement.*

---

## Consequences

### Positive
- [Expected benefit 1]
- [Expected benefit 2]

### Negative / Trade-offs
- [Known trade-off 1 and how it is mitigated]
- [Known trade-off 2 and how it is mitigated]

### Risks
- [Risk 1]: [Likelihood] / [Mitigation]
- [Risk 2]: [Likelihood] / [Mitigation]

---

## Implementation Notes

*Technical specifics for engineers implementing this decision:*

```hcl
# Example: Terraform variable enforcement
variable "min_instances" {
  type        = number
  description = "Minimum Cloud Run instances. Tier 1 services require >= 1."
  default     = 0

  validation {
    condition     = var.min_instances >= 0
    error_message = "min_instances must be non-negative."
  }
}
```

*Relevant files/modules affected*:
- `reference-implementations/terraform-baseline/modules/cloud-run/main.tf`
- `reference-implementations/terraform-baseline/environments/*/main.tf`

---

## Review Notes

*Record significant discussion points from the review. This section documents the reasoning behind any changes made from the initial proposal.*

| Reviewer | Comment | Resolution |
|----------|---------|------------|
| [Name] | [Comment] | [How it was addressed] |

---

## References

- [Link to relevant documentation, RFCs, or prior art]
- [Link to performance benchmarks or test results]
- [Link to related ADRs]

---

*For the full ADR log, see [docs/decisions/](../docs/decisions/).*
