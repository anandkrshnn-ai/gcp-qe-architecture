# Lessons Learned

Reflections on building and applying the GCP QE Architecture.

1. **Modular Terraform saves huge time but requires discipline**: Separating compute from network and state management allowed for rapid environment replication, but naming conventions must be strictly followed.
2. **Gemini Agent is powerful but needs good prompt engineering**: Moving from simple prompts to structured JSON-mode prompts with role-based context improved reliability by over 50%.
3. **Chaos experiments are most valuable when tied to SLOs**: Running a pod-kill experiment is just "breaking things" unless you can measure the exact impact on your availability error budget.
4. **Evidence (screenshots, outputs) is crucial for credibility**: In a professional portfolio, showing *how* a tool ran is just as important as the code itself.
5. **Real usage beats theoretical content**: Applying the production readiness checklist to a real project revealed more gaps than any theoretical review ever could.

*Updated regularly based on actual application in my role as QA Architect Manager.*
