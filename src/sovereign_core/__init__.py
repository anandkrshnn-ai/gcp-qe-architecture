"""
Sovereign Core: The Agentic QE Framework for GCP.
"""

from .client import SovereignClient
from .analyzer import SovereignAnalyzer, VertexAIAnalyzer

__version__ = "0.2.0"
__all__ = ["SovereignClient", "SovereignAnalyzer", "VertexAIAnalyzer"]
