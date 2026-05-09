"""
Diagnostic toolset for the Sovereign SRE agent.
In a production NemoClaw environment, these would be proxied to the real GKE API.
"""

import re

def mask_pii(text: str) -> str:
    """Masks basic PII (emails, IPs) from diagnostic data."""
    # Mask Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    # Mask IP Addresses
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[REDACTED_IP]', text)
    return text

def fetch_logs(pod_name: str, window_minutes: int = 15) -> str:
    """Fetches structured logs from a specific GKE pod."""
    # Bounds check
    window_minutes = min(max(window_minutes, 1), 60)
    
    raw_logs = f"LOGS for {pod_name} (Last {window_minutes}m): user test@example.com logged in from 192.168.1.1"
    return mask_pii(raw_logs)

def inspect_environment(pod_name: str) -> dict:
    """Retrieves environment variables and configuration for a pod."""
    return {
        "pod_name": pod_name,
        "env": {
            "DB_HOST": "10.0.0.5",
            "MAX_CONNECTIONS": "100",
            "JAVA_OPTS": "-Xmx2g"
        }
    }

def check_resource_usage(pod_name: str) -> dict:
    """Checks CPU and Memory usage metrics for a pod."""
    return {
        "pod_name": pod_name,
        "cpu_usage": "85%",
        "memory_usage": "1.9GB",
        "limit": "2GB"
    }

def query_k8s_events(namespace: str = "default") -> list:
    """Queries Kubernetes events for the given namespace."""
    return [
        {"type": "Warning", "reason": "OOMKilling", "message": "Memory limit exceeded"},
        {"type": "Normal", "reason": "ScalingReplicaSet", "message": "Scaled up replica set"}
    ]

# Tool definitions for Vertex AI Function Calling
TOOL_DEFINITIONS = [
    {
        "name": "fetch_logs",
        "description": "Fetch structured logs from a specific pod in the cluster.",
        "parameters": {
            "type": "object",
            "properties": {
                "pod_name": {"type": "string"},
                "window_minutes": {"type": "integer", "default": 15}
            },
            "required": ["pod_name"]
        }
    },
    {
        "name": "inspect_environment",
        "description": "Get environment variables and configuration for a pod.",
        "parameters": {
            "type": "object",
            "properties": {
                "pod_name": {"type": "string"}
            },
            "required": ["pod_name"]
        }
    },
    {
        "name": "check_resource_usage",
        "description": "Get CPU and Memory usage metrics for a pod.",
        "parameters": {
            "type": "object",
            "properties": {
                "pod_name": {"type": "string"}
            },
            "required": ["pod_name"]
        }
    },
    {
        "name": "query_k8s_events",
        "description": "Query Kubernetes events in a namespace.",
        "parameters": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "default": "default"}
            }
        }
    }
]
