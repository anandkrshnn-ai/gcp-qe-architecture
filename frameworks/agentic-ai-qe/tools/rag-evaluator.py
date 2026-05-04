from vertexai.generative_models import GenerativeModel, GenerationConfig
import vertexai
import json
from typing import Dict

vertexai.init(project="YOUR_PROJECT_ID", location="asia-south1")

model = GenerativeModel(
    "gemini-3.1-pro",
    generation_config=GenerationConfig(
        temperature=0.0,
        response_mime_type="application/json"
    )
)

def evaluate_rag_response(query: str, context: str, response: str, ground_truth: str = None) -> Dict:
    prompt = f"""You are an expert RAG Quality Evaluator.

Query: {query}
Context: {context[:7000]}
Response: {response}
Ground Truth: {ground_truth or 'Not provided'}

Evaluate strictly and return **only** valid JSON:

{{
  "faithfulness_score": 0.XX,
  "relevance_score": 0.XX,
  "answer_relevance_score": 0.XX,
  "hallucination_risk": "Low/Medium/High",
  "overall_score": 0.XX,
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "improvement_suggestions": ["...", "..."]
}}"""

    result = model.generate_content(prompt)
    evaluation = json.loads(result.text)
    return evaluation


# Example usage
if __name__ == "__main__":
    # Example to test logic
    # eval_result = evaluate_rag_response(
    #     query="What is the status of my order #ORD-78492?",
    #     context="Order #ORD-78492 was shipped on May 3rd via DTDC...",
    #     response="Your order has been delivered successfully.",
    #     ground_truth="Order was shipped but not yet delivered."
    # )
    # print(json.dumps(eval_result, indent=2))
    pass
