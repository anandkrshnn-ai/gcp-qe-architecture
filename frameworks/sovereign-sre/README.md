# Sovereign SRE Prototype

An autonomous diagnostic agent that uses NemoClaw principles to perform RCA on simulated production failures in a GCP environment.

## Overview

This prototype demonstrates how an AI agent can:
1.  **Reason** about production alerts.
2.  **Act** by calling diagnostic tools (simulated).
3.  **Observe** log and metric data from a sandboxed environment.
4.  **Analyze** the root cause and provide a signed RCA report.

## Setup

1.  Navigate to this directory:
    ```bash
    cd frameworks/sovereign-sre
    ```
2.  Install dependencies (optional for mock mode):
    ```bash
    pip install -r requirements.txt
    ```

## Execution

Run the agent in **Mock Mode** (No GCP credentials required):

```bash
python agent.py
```

## Security Design

*   **Sandboxed Execution**: The agent logic assumes it is running inside a NemoClaw-managed container.
*   **Tool Gating**: The agent can only access the functions defined in `tools.py`.
*   **Identity**: In a real deployment, this agent uses **GKE Workload Identity** for all cloud interactions.
