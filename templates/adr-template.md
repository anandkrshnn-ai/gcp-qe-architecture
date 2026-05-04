# Architecture Decision Record (ADR) Template

## Title: [Short noun phrase describing the decision, e.g., "Use Cloud Spanner for Inventory Service"]

**Status:** [Draft | Proposed | Accepted | Rejected | Deprecated]
**Date:** [YYYY-MM-DD]
**Author(s):** [Names]

## Context
[Describe the context and problem statement, e.g., in a few paragraphs or using bullet points. What is the current situation? What is the problem being solved? Why does this decision need to be made now?]

## Quality & NFR Considerations
[How does this decision impact our Quality Strategy?]
*   **Performance:** [e.g., Latency impact, throughput capacity]
*   **Reliability:** [e.g., Impact on availability SLOs, multi-region failover capabilities]
*   **Testability:** [e.g., Can this be easily mocked? How will we load test this?]
*   **Security:** [e.g., Data encryption, IAM boundaries]

## Decision
[State the decision clearly. "We will use X instead of Y for Z."]

## Consequences
[What becomes easier or more difficult because of this change?]
*   **Positive:** [e.g., Enables global consistency, reduces operational overhead]
*   **Negative:** [e.g., Higher infrastructure cost, steep learning curve for developers]

## Alternatives Considered
*   **[Alternative 1]:** [Why was it not chosen?]
*   **[Alternative 2]:** [Why was it not chosen?]
