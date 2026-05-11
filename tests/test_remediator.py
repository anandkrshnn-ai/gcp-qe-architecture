import pytest
from src.sovereign_core.remediator import DryRunRemediator

def test_remediator_patch_validation():
    remediator = DryRunRemediator(use_mock=True)
    
    # Valid Patch
    valid_patch = {"op": "replace", "path": "/spec/replicas", "value": 3}
    assert remediator.dry_run_patch("test-deploy", valid_patch) is True
    
    # Invalid Patch
    invalid_patch = {"foo": "bar"}
    assert remediator.dry_run_patch("test-deploy", invalid_patch) is False
