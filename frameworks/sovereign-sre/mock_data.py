"""
Simulated production failure scenarios for the Sovereign SRE prototype.
"""

SCENARIOS = {
    "oom_kill": {
        "alert": "SLO Burn Rate Alert: transaction-engine latency > 500ms",
        "events": [
            {"type": "Warning", "reason": "BackOff", "message": "Back-off restarting failed container"},
            {"type": "Warning", "reason": "OOMKilling", "message": "Memory limit exceeded for pod transaction-engine-v1-8f92"}
        ],
        "logs": [
            "2026-05-01T14:20:01Z INFO Starting transaction processing...",
            "2026-05-01T14:21:45Z DEBUG Allocated 500MB for batch 123",
            "2026-05-01T14:22:10Z DEBUG Allocated 500MB for batch 124",
            "2026-05-01T14:22:30Z ERROR java.lang.OutOfMemoryError: Java heap space"
        ],
        "metrics": {
            "cpu": "45%",
            "memory": "1.95GB",
            "limit": "2GB"
        },
        "env": {
            "JAVA_OPTS": "-Xmx2g",
            "BATCH_SIZE": "10000"
        },
        "expected_rca": "Memory leak in batch processing; heap size (2GB) insufficient for current batch size (10000)."
    }
}
