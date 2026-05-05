from typing import List, Dict

class AgentMemory:
    """Simple conversation memory for QE Agents to maintain context across analysis steps."""
    
    def __init__(self, history_limit: int = 5):
        self.history: List[Dict] = []
        self.history_limit = history_limit

    def add_interaction(self, user_query: str, agent_response: Dict):
        self.history.append({
            "query": user_query,
            "response": agent_response
        })
        # Maintain history limit
        if len(self.history) > self.history_limit:
            self.history.pop(0)

    def get_context(self) -> str:
        if not self.history:
            return "No previous context."
        
        context_str = "Previous interactions:\n"
        for i, interaction in enumerate(self.history):
            context_str += f"{i+1}. Query: {interaction['query']}\n"
            context_str += f"   Cause: {interaction['response'].get('root_cause', 'N/A')}\n"
        return context_str

    def clear(self):
        self.history = []

# Example usage
if __name__ == "__main__":
    memory = AgentMemory()
    memory.add_interaction("Analyze GKE logs", {"root_cause": "OOMKill"})
    print(memory.get_context())
