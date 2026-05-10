# Sovereign-GCP Master Demo Report
Date: 2026-05-10 22:37

| Incident | Root Cause | Confidence | Proposed Action |
| :--- | :--- | :--- | :--- |
| oomkill | Pod OOMKill | 95.0% | Increase resource.limits.memory in K8s manifest. |
| latency | Service Timeout (60s) | 92.0% | Increase Cloud Run timeout or optimize downstream query latency. |
| dns_failure | Not Found | 0.0% | N/A |
| quota_exhaustion | Not Found | 0.0% | N/A |
| iam_denied | Not Found | 0.0% | N/A |
| storage_full | Not Found | 0.0% | N/A |
| db_fail | Not Found | 0.0% | N/A |
| cert_expired | Not Found | 0.0% | N/A |
