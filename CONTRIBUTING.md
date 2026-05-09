# Contributing to GCP QE Architecture

Thank you for your interest in contributing! This project aims to be a high-quality, executable reference for Quality Engineering on GCP.

## How to Contribute

### 1. Reporting Bugs
- Open a GitHub Issue.
- Provide logs, steps to reproduce, and any relevant simulator output.

### 2. Suggesting Enhancements
- Open a Feature Request issue.
- Focus on practical, functional patterns that solve real GCP QE pain points.

### 3. Pull Requests
All PRs must:
- Follow the existing folder structure.
- Include/update relevant documentation in `guides/`.
- Ensure the demo (`run_demo.py`) still works or is updated to reflect new patterns.

## Local Setup
1. Clone the repo: `git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture.git`
2. Install Python dependencies: `pip install -r requirements.txt`.
3. Install Terraform (v1.10+).

## Code Style
- **Python**: Standard PEP8.
- **Terraform**: Follow the [Google Terraform Style Guide](https://googlecloudplatform.github.io/terraform-validator/docs/style_guide).

## Quality Gates
Contributions should be validated locally:
- `python run_demo.py oomkill` (Ensure PoC remains functional)
- `terraform validate` (For IaC changes)

---
By contributing, you agree that your contributions will be licensed under the project's LICENSE.
