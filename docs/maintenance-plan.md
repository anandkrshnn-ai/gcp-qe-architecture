# 90-Day Maintenance Plan (Sustainability)

To keep this repository a high-authority, living reference, follow this sustainable maintenance schedule.

## Phase 1: Monthly Updates (Days 1–90)
**Goal**: Keep the core components functional and documentation fresh.

- **Check Dependencies**: Monthly `pip install --upgrade` and `terraform init -upgrade` checks for modules.
- **Log Review**: Review the [Real-World Usage](../docs/real-world-usage.md) logs and add 1 new entry per month based on work outcomes.
- **Broken Link Check**: Run a monthly link check across the documentation.

## Phase 2: Quarterly Deep-Dives (Every 3 Months)
**Goal**: Add one major new technical highlight.

- **Quarter 1 Goal**: Expand **Agentic AI** section with tool-calling examples (MCP server).
- **Quarter 2 Goal**: Add **Cross-Cloud Quality** patterns (e.g., GKE to AWS RDS latency testing).
- **Quarter 3 Goal**: Implement **Automated Chaos Gates** in the Cloud Build pipeline.

## Phase 3: Community & Visibility
**Goal**: Transition from "personal repo" to "industry reference."

- **Blog Post**: Write 1 technical blog post (on Medium/LinkedIn) linking to a Case Study in this repo.
- **GitHub Updates**: Maintain a professional `ROADMAP.md` and respond to any issues/PRs within 72 hours.
- **Internal Sharing**: Present a Case Study from this repo in a team/org level tech-talk.

## Maintenance Checklist (Quick)
| Task | Frequency | Last Done |
|------|-----------|-----------|
| Terraform Version Upgrade | Quarterly | May 2026 |
| Gemini Model Update (e.g. 3.1 -> 3.x) | As Released | May 2026 |
| Python Dependency Audit | Monthly | May 2026 |
| Real-World Entry Addition | Monthly | May 2026 |

**Long-term Success Metric**: The repo should remain "executable" and provide value to a new QE hire in their first week.
