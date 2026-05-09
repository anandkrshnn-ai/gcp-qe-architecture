"""
Sovereign SRE v2: Advanced Multi-Agent Orchestration with Reflection.
Pattern: Orchestrator -> Diagnostician -> Reviewer -> Healer
"""

class ADKAgent:
    def __init__(self, role):
        self.role = role

class Orchestrator(ADKAgent):
    def __init__(self):
        super().__init__("Orchestrator")
        self.diagnostician = Diagnostician()
        self.reviewer = Reviewer()
        self.healer = Healer()

    def handle_incident(self, alert_data):
        print(f"[*] [ORCHESTRATOR] Incident Detected: {alert_data['alert_name']}")
        
        # Loop until Reviewer is satisfied (Self-Correction Pattern)
        attempts = 0
        max_attempts = 3
        current_diagnosis = None
        
        while attempts < max_attempts:
            attempts += 1
            print(f"--- Attempt {attempts} ---")
            
            # 1. Diagnose
            current_diagnosis = self.diagnostician.analyze(alert_data, feedback=current_diagnosis)
            
            # 2. Review (Reflection)
            review_result = self.reviewer.critique(current_diagnosis)
            
            if review_result["status"] == "APPROVED":
                print("[*] [ORCHESTRATOR] Diagnosis approved by Reviewer.")
                break
            else:
                print(f"[!] [ORCHESTRATOR] Reviewer rejected diagnosis: {review_result['reason']}")
                # Pass feedback back to diagnostician for next loop
                current_diagnosis = review_result

        # 3. Heal
        if attempts < max_attempts:
            self.healer.propose_fix(current_diagnosis)
        else:
            print("[!] [ORCHESTRATOR] FAILED to reach stable diagnosis. Escalating to Human SRE.")

class Diagnostician(ADKAgent):
    def __init__(self):
        super().__init__("Diagnostician")

    def analyze(self, alert_data, feedback=None):
        if feedback and feedback.get("status") == "REJECTED":
            print("[*] [DIAGNOSTICIAN] Incorporating feedback: 'Check deeper for Java Native Memory'...")
            return {"root_cause": "Java Native Memory Leak", "confidence": 0.98}
        
        print("[*] [DIAGNOSTICIAN] Initial Hypothesis: Heap exhaustion.")
        return {"root_cause": "Heap Exhaustion", "confidence": 0.75}

class Reviewer(ADKAgent):
    """Reflective agent that critiques hypotheses to find edge cases."""
    def __init__(self):
        super().__init__("Reviewer")

    def critique(self, diagnosis):
        if diagnosis.get("root_cause") == "Heap Exhaustion":
            return {
                "status": "REJECTED", 
                "reason": "Heap usage is flat. Did you check Direct/Native buffers?",
                "original_diagnosis": diagnosis
            }
        return {"status": "APPROVED", "diagnosis": diagnosis}

class Healer(ADKAgent):
    def __init__(self):
        super().__init__("Healer")

    def propose_fix(self, diagnosis):
        print(f"[*] [HEALER] Generating fix for: {diagnosis['diagnosis']['root_cause']}")
        print("[*] [IAC] Terraform: Updating jemalloc configuration for Native Memory optimization.")

if __name__ == "__main__":
    incident = {"alert_name": "Container Restart Loop"}
    sre = Orchestrator()
    sre.handle_incident(incident)
