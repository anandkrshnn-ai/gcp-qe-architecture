# ⚠️ Deprecated Directory

> **This directory is superseded.** The active k6 performance test suite is located at:
> **[`../k6-performance/`](../k6-performance/)**

## What's in the Active Directory

| Script | Purpose |
|--------|---------|
| `cloud-run-load-test.js` | Standard load test — 100 VUs, P95 SLO gate |
| `cold-start-test.js` | Cold-start validation — tests `min_instances=0` latency |

The `load-test.js` file in this directory is an older version retained for historical reference only.
It uses a different BASE_URL convention (`TARGET_URL`) and does not include the SLO-aligned
thresholds or the cold-start scenario added in the active suite.

**Do not use this directory for new test work.**
