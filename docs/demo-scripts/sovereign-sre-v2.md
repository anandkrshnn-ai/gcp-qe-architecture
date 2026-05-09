# Demo Script: Sovereign SRE v2 — The Future of Self-Healing Cloud

**Goal**: A 3-minute high-impact video demonstration for your LinkedIn/Portfolio.

---

## 🎬 Scene 1: The Alert (0:00 - 0:45)
*   **Visual**: Show a Cloud Monitoring Dashboard with a red spike in latency for `transaction-engine`.
*   **Script**: "Imagine it's 3 AM. A critical transaction engine in your GCP environment just breached its SLO. Usually, this means waking up an SRE. But in 2026, we do things differently."
*   **Action**: Show the EventArc trigger firing in the logs.

## 🧠 Scene 2: The Multi-Agent Reasoning (0:45 - 1:45)
*   **Visual**: Switch to the `sovereign-sre-v2` terminal output.
*   **Script**: "Meet Sovereign SRE v2. It’s a multi-agent system built on the Vertex AI ADK. Notice how the **Orchestrator** wakes up and delegates tasks. The **Diagnostician** queries AlloyDB for historical patterns, while the **Healer** generates a Terraform plan to scale the memory limits."
*   **Highlight**: Point out the **Model Armor** safety scan—"We aren't just running AI; we're running it behind a security firewall."

## 🛡️ Scene 3: The Secure Sandbox (1:45 - 2:30)
*   **Visual**: Show the Mermaid architecture diagram from the Case Study.
*   **Script**: "Security is the core. The agent is isolated in a **GKE Agent Sandbox** (gVisor), meaning it has zero access to the host kernel. It uses Workload Identity to interact with GCP, so there are no static keys to steal."
*   **Action**: Show the "Human-in-the-Loop" approval prompt in Slack/Teams.

## ✅ Scene 4: Resolution & Value (2:30 - 3:00)
*   **Visual**: Show the dashboard returning to green and the generated RCA report.
*   **Script**: "In less than 3 minutes, the root cause was identified, the fix was proposed, and the system is back to healthy. We've reduced MTTR by 85% in a fully regulated, sovereign environment. This is the new standard for Quality Engineering."
*   **Call to Action**: "Check out the full implementation and security audits in the repo."

---

## 💡 Recording Tips
1.  **Use Zoom-in/Zoom-out**: Focus on the code snippets and the "SUCCESS" JSON blocks.
2.  **Highlight the 'Evidence' Folder**: Show the Security Audits in the repo to prove it's production-ready.
3.  **Clear Voiceover**: Use a confident, architect-level tone.
