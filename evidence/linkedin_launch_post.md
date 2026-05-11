🚀 Just open-sourced a focused research PoC: Agentic Incident Analyzer with Multi-Agent Consensus.

Built this to explore how AI agents can safely assist SRE teams in regulated GCP environments — without giving them direct production access.

Core loop:
→ Ingest incident logs/metrics
→ Gemini 1.5 Pro reasoning (structured function calling)
→ Multi-agent consensus voting
→ Generate + dry-run validate Kubernetes JSON patches
→ Chaos testing to prove resilience against corrupted/faulty data

Includes:
- Hardened GKE Terraform (Confidential Nodes + gVisor)
- Full safety guardrails
- One-command demo (`make demo` and `make chaos`)

Not production software — a deliberate research project to push my understanding of agentic SRE patterns.

Repo: https://github.com/anandkrshnn-ai/gcp-qe-architecture

Would love thoughtful feedback from SRE, Platform Engineering, and Agentic AI folks.

#GCP #Kubernetes #SRE #AgenticAI #GoogleCloud #PlatformEngineering
