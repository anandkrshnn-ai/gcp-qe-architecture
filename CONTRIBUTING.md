# Contributing to GCP QE Architecture

Thank you for your interest in contributing! This project aims to be a high-quality, executable reference for Quality Engineering on GCP.

## How to Contribute

### 1. Reporting Bugs
- Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.yml).
- Provide logs, screenshots, and steps to reproduce.

### 2. Suggesting Enhancements
- Open an issue using the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.yml).
- Explain the "Why" and "How" of the proposed change.

### 3. Pull Requests
All PRs must:
- Follow the existing folder structure.
- Include/update relevant documentation in `docs/` or `guides/`.
- Ensure all tests pass (`pytest`).
- Include a **reproducible artifact** (e.g., a terraform plan, a tool output log) in the `evidence/` directory.

## Local Setup
1. Clone the repo: `git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture.git`
2. Install Python dependencies: `pip install -r requirements.txt` (Note: ensure you use a virtual environment).
3. Install Terraform (v1.10+).

## Code Style
- **Python**: We use `ruff` for linting and `pytest` for testing. Run `ruff check .` before committing.
- **Terraform**: Follow the [Google Terraform Style Guide](https://googlecloudplatform.github.io/terraform-validator/docs/style_guide).

## Quality Gates
Every contribution is validated through GitHub Actions:
- Terraform Validation
- Python Linting & Testing
- MkDocs Build validation

---
By contributing, you agree that your contributions will be licensed under the project's LICENSE.
