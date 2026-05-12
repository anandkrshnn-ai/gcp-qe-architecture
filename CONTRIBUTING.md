# Contributing to Agent Safety Patterns

First, thank you for considering contributing to this reference architecture. This project is maintained as a **Principal Architect Reference Implementation**, meaning we prioritize **deterministic safety**, **cryptographic integrity**, and **empirical verification** over rapid feature iteration.

## Architectural Principles

1. **Defense-in-Depth**: Every autonomous action must pass through at least three layers of verification (Consensus, Model Armor, and Safety Gate).
2. **Deterministic Outcomes**: Use Pydantic and strict schema validation to ensure agentic outputs are predictable.
3. **Verifiable Telemetry**: All high-signal events must be logged as structured JSON compatible with Google Cloud Logging.
4. **Adversarial Resilience**: New features must include property-based tests (Hypothesis) to prove resilience against edge cases.

## Development Workflow

1. **Fork and Branch**: Create a feature branch for your changes.
2. **Environment Setup**:
   ```bash
   pip install -e ".[dev,gcp]"
   ```
3. **Testing**:
   Every PR must pass the full test suite:
   ```bash
   export PYTHONPATH=src
   pytest -v
   ```
4. **Documentation**:
   If you change the core logic, update the corresponding deep-dive in `docs/`. Preview changes with:
   ```bash
   mkdocs serve
   ```

## Pull Request Standards

- **Atomic Commits**: Use clear, descriptive commit messages.
- **Coverage**: Maintain or improve the current coverage (~88%+).
- **Safety**: Ensure no secrets or PII are exposed in logs or code.

## Code of Conduct

We follow standard professional engineering ethics. Be respectful, be thorough, and build for safety first.
