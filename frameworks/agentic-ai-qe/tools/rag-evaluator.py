from vertexai.generative_models import GenerativeModel
import vertexai
import json

vertexai.init(project="YOUR_PROJECT_ID", location="asia-south1")
model = GenerativeModel("gemini-3.1-pro")

def evaluate_rag(query: str, context: str, response: str):
    prompt = f"""Evaluate this RAG output strictly:

Query: {query}
Context: {context[:6000]}
Response: {response}

Return valid JSON only:
{{
  "faithfulness": 0.XX,
  "relevance": 0.XX,
  "hallucination_risk": "Low/Medium/High",
  "improvements": ["...", "..."]
}}"""

    result = model.generate_content(prompt)
    print(result.text)
    return result.text

# Example usage
if __name__ == "__main__":
    evaluate_rag(
        query="What is the current status of order #12345?",
        context="Order #12345 was shipped on 2026-05-03...",
        response="Your order has been delivered."
    )
