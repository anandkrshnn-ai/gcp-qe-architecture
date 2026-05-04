# RAG Evaluation Report

**Date**: [YYYY-MM-DD]
**Overall Average Score**: [e.g., 0.85]
**Hallucination Rate**: [e.g., 5%]

**Key Findings**:
- Faithfulness remains high across simple queries.
- Relevance drops when context is excessively long (>5000 tokens).
- Occasional hallucinations noted in specific edge cases (e.g., policy dates).

**Recommendations**:
- Implement prompt-based grounding for date-related queries.
- Improve chunking strategy to reduce context noise.
- Add more negative test cases to the evaluation dataset.
