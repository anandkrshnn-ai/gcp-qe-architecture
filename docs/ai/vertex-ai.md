# Vertex AI & Gemini Integration

The architecture utilizes **Gemini 1.5 Pro** via the Vertex AI SDK for high-fidelity incident root-cause analysis.

## Hardened AI Integration

Unlike standard LLM implementations, the `VertexAIAnalyzer` is designed for production-grade reliability and security.

### 1. Deterministic JSON Mode
We utilize Gemini's `application/json` response MIME type to ensure that the AI's analysis is strictly formatted for our `Finding` Pydantic model. This eliminates "text garbage" and simplifies the automated remediation pipeline.

### 2. Exhaustive Safety Filters
To maintain professional autonomy and prevent malicious prompt injection from logs, we implement strict `SafetySetting` configurations across all categories:

| Category | Threshold |
| :--- | :--- |
| **Hate Speech** | `BLOCK_ONLY_HIGH` |
| **Dangerous Content** | `BLOCK_ONLY_HIGH` |
| **Harassment** | `BLOCK_ONLY_HIGH` |
| **Sexually Explicit** | `BLOCK_ONLY_HIGH` |

### 3. Enterprise System Instructions
The analyzer injects a non-negotiable system prompt that forces the model into an "SRE Automation Agent" persona, prioritizing factual log analysis over creative generation.

## Real-Mode Execution

When the `--real` flag is provided to the demo, the system transitions from simulation to live GCP calls:

```python
model = GenerativeModel("gemini-1.5-pro")
response = model.generate_content(
    prompt,
    generation_config={"response_mime_type": "application/json"},
    safety_settings=safety_settings
)
```

## Authentication (ADC)
The implementation supports **Application Default Credentials (ADC)**. When running on GKE or locally with `gcloud auth application-default login`, the analyzer automatically inherits the correct service account permissions for the target project.
