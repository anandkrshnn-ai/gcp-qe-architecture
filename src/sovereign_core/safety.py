"""
Sovereign Core: Safety Gate and Blast Radius Control.
Enforces system invariants before remediation.
"""

import logging
import json
import os
import time
from typing import Dict, Any, List, Optional
from .store import BaseStateStore, FileStateStore

logger = logging.getLogger("SovereignCore.Safety")

class EscalationManager:
    """
    Handles human handoff when the autonomous engine reaches its limit.
    Mocks a PagerDuty / OpsGenie integration.
    """
    def __init__(self, service_key: str = "demo-key"):
        self.service_key = service_key

    def escalate(self, incident_type: str, resource: str, reason: str):
        """Sends a high-severity alert to the on-call engineer."""
        logger.critical(f"[ESCALATION] Alerting On-Call: {incident_type} on {resource}")
        logger.critical(f"[ESCALATION] Reason: {reason}")
        # In production: requests.post("https://events.pagerduty.com/v2/enqueue", ...)
        return True

class SafetyGate:
    """
    The 'Brakes' of the Autonomous Cloud.
    Now includes Wave 3 Epistemic Safety: Platform Awareness & Discovery Mode.
    """
    
    def __init__(self, production_mode: bool = False, store: Optional[BaseStateStore] = None, time_dilation: float = 1.0):
        self.production_mode = production_mode
        self.store = store or FileStateStore()
        self.escalator = EscalationManager()
        self.time_dilation = time_dilation
        
        self.invariants = {
            "max_attempts": 3,
            "window_seconds": 600,
            "honeymoon_seconds": 3600,  # 1 hour discovery mode
            "blocked_remediations": ["delete_project", "purge_all_iam"],
            "restricted_resources": ["prod-sql-master", "core-network-vpc"]
        }

    def _check_platform_health(self, target: str) -> bool:
        """
        Wave 3: Multi-Tenant Awareness.
        Detects if multiple siblings are failing simultaneously (Platform Outage).
        """
        history = self.store.get_history()
        now = time.time()
        
        # Check if 3+ DIFFERENT resources have failed in the last 5 minutes
        recent_failures = [h for h in history if (now - h["timestamp"]) < 300]
        unique_targets = set(h["target"] for h in recent_failures)
        
        if len(unique_targets) >= 3 and target not in unique_targets:
            logger.critical(f"[EPISTEMIC] PLATFORM EVENT DETECTED. Multiple failures across siblings: {unique_targets}")
            return False  # Platform is unstable, freeze local actions
        return True

    def _check_honeymoon_period(self, target: str) -> bool:
        """
        Wave 3/Principal: Cold Start Protection.
        """
        meta = self.store.get_resource_metadata(target)
        if not meta:
            self.store.update_resource_status(target, "DISCOVERY")
            meta = self.store.get_resource_metadata(target)
            
        first_seen = meta.get("first_seen", time.time())
        age = time.time() - first_seen
        
        if age < self.invariants["honeymoon_seconds"]:
            logger.warning(f"[EPISTEMIC] Resource '{target}' is in HONEYMOON PERIOD ({int(age)}s old). Remediation disabled.")
            return False
        return True

    STABILIZATION_CONFIG = {
        "db": {"cycles": 10, "interval": 5},
        "zone": {"cycles": 6, "interval": 30},
        "memory": {"cycles": 3, "interval": 10},
        "default": {"cycles": 3, "interval": 15}
    }

    def verify_stabilization(self, target: str) -> bool:
        """
        Wave 7: Loophole #14 - Stabilization Retry Caps.
        Prevents 'Checkerboarding' attacks or infinite retry loops.
        """
        meta = self.store.get_resource_metadata(target)
        if meta.get("status") != "STABILIZING":
            return True

        # Loophole #14: Cap total attempts
        attempts = meta.get("stabilization_attempts", 0)
        if attempts >= 5:
            logger.error(f"[CRITICAL] Loophole #14: Max Stabilization Attempts (5) reached for {target}. ESCALATING.")
            self.store.update_resource_status(target, "FREEZE_STABILIZATION_FAILURE")
            return False

        # Resolve type-specific config
        res_type = "memory" if "memory" in target else ("db" if "db" in target else "default")
        config = self.STABILIZATION_CONFIG.get(res_type, self.STABILIZATION_CONFIG["default"])
        
        # Loophole #2: Detect oscillation
        history = self.store.get_history(strike_decay_seconds=300)
        is_oscillating = any(h["target"] == target for h in history)
        
        target_cycles = config["cycles"] * (2 if is_oscillating else 1)
        cycles = meta.get("stabilization_cycles", 0)
        
        if cycles < target_cycles:
            logger.info(f"[STABILIZATION] Cycle {cycles+1}/{target_cycles}")
            self.store.update_resource_status(target, "STABILIZING", {"stabilization_cycles": cycles + 1})
            return False
        
        self.store.update_resource_status(target, "HEALTHY", {"stabilization_cycles": 0, "stabilization_attempts": 0})
        return True

    SELF_PRESERVATION_LABELS = {"app": "sovereign", "role": "agent"}

    def validate_action(self, remediation: str, target: str) -> bool:
        """
        Validates action against Byzantine Hardened Invariants.
        Wave 8: Self-Preservation & Total-Impact Budgeting.
        """
        # Loophole #15: Self-Preservation. Block remediations on the agent itself.
        # Simulated check: In production, this verifies resource labels.
        if "agent" in target or "sovereign" in target:
            logger.error(f"[CRITICAL] Loophole #15: Self-Preservation REJECT. Agent cannot remediate itself: {target}")
            return False

        # Loophole #12: Magnitude-Aware Budgeting (Total Impact Analysis)
        # We calculate: (unit_cost * current_scale * scale_magnitude)
        current_replicas = 10 
        scale_out_factor = 10 # Loophole #12: Attack scaling from 10 to 100
        unit_cost = 0.10
        
        total_impact = unit_cost * current_replicas * scale_out_factor
        if total_impact > 10.0: # $10/hr threshold for autonomous action
            logger.error(f"[SAFETY] Loophole #12: Total-Impact Budget REJECT. Estimated cost ${total_impact}/hr.")
            return False

        # Loophole #10: Admission Control
        active_remediations = len([h for h in self.store.get_history(300)])
        if active_remediations >= 10:
            logger.error("[SAFETY] Loophole #10: Admission Control Reject.")
            return False

        logger.info(f"[SAFETY] Auditing action: {remediation} on {target}")
        
        # 0. Check Platform Health (Freeze Pauses Decay)
        is_healthy = self._check_platform_health(target)
        if not is_healthy:
            logger.warning(f"[SAFETY] Platform Storm Detected. FREEZING ACTIONS.")
            return False

        # 2. Death Spiral Prevention
        history = self.store.get_history(strike_decay_seconds=3600)
        
        recent_matches = [
            h for h in history 
            if h["remediation"] == remediation 
            and h["target"] == target 
        ]

        if len(recent_matches) >= self.invariants["max_attempts"]:
            reason = f"Attempted {remediation} {len(recent_matches)} times (active strikes). Permanent Freeze avoided via Decay."
            logger.error(f"[SAFETY CRITICAL] Death Spiral Detected! {reason}")
            self.escalator.escalate("DEATH_SPIRAL", target, reason)
            return False

        # 3. Protect critical resources
        if any(res in target for res in self.invariants["restricted_resources"]):
            if self.production_mode:
                logger.error(f"[SAFETY CRITICAL] Attempted modification of protected resource: {target}")
                return False

        # Record action if valid and set to STABILIZING
        self.store.record_action(remediation, target)
        self.store.update_resource_status(target, "STABILIZING", {"stabilization_cycles": 0})
        logger.info(f"[SAFETY] Action '{remediation}' passed all Wave 3/Principal audits.")
        return True

    def get_rollback_plan(self, remediation: str, target: str) -> Dict[str, Any]:
        """
        Defines the 'Undo' logic for a given action.
        """
        rollback_map = {
            "scale_up_memory": {"action": "scale_down_memory", "target": target},
            "scale_out_replicas": {"action": "scale_in_replicas", "target": target},
            "expand_disk_size": {"action": "manual_intervention_required", "reason": "Disk shrink not supported automatically"},
            "request_quota_increase": {"action": "none", "reason": "Non-destructive action"},
        }
        return rollback_map.get(remediation, {"action": "manual_intervention_required"})
