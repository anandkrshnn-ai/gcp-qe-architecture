import pytest
import unittest.mock as mock
from src.safety_core.quality_intelligence.authenticity import AuthenticityScorer, AuthenticityRisk

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

@pytest.mark.skipif(not HAS_TORCH, reason="torch not installed")
def test_calculate_style_cpc_math():
    scorer = AuthenticityScorer()
    
    # Create mock logits and labels
    # bsz=1, seq_len=2, vocab=3
    logits_score = torch.tensor([[[1.0, 0.1, 0.1], [0.1, 1.0, 0.1]]])
    logits_ref = torch.tensor([[[1.0, 0.1, 0.1], [0.1, 1.0, 0.1]]])
    labels = torch.tensor([[0, 1]]) # Matching the max logit indices
    
    discrepancy = scorer.calculate_style_cpc(logits_score, logits_ref, labels)
    
    # If logits_score == logits_ref and labels match the max logits, 
    # the discrepancy should be positive (high likelihood relative to mean)
    assert discrepancy.item() > 0

def test_risk_threshold_mapping():
    scorer = AuthenticityScorer(low_threshold=0.2, high_threshold=0.8)
    
    assert scorer.get_risk_flag(0.1) == AuthenticityRisk.LOW
    assert scorer.get_risk_flag(0.5) == AuthenticityRisk.MEDIUM
    assert scorer.get_risk_flag(0.9) == AuthenticityRisk.HIGH
    assert scorer.get_risk_flag(-1.0) == AuthenticityRisk.LOW

def test_score_proposal_advisory_mode():
    scorer = AuthenticityScorer()
    result = scorer.score_proposal("Test remediation description", None)
    
    assert "authenticity_score" in result
    assert "authenticity_risk_flag" in result
    assert result["evidence"]["status"] == "ADVISORY_ONLY"
    assert result["evidence"]["method"] == "Style-CPC (AAAI 2025)"
