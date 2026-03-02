"""Integration test for automate contract entrypoint."""
import json
import subprocess
import os
import pytest


@pytest.mark.skip(reason="speckle_automate runner requires specific environment setup")
def test_automate_entrypoint_contract():
    # Prepare dummy input data
    automation_context = {"run_id": "test", "other": "data"}
    function_inputs = {"source_model_id": "test-source-id", "target_model_id": "test-target-id"}
    # Write temp files
    with open("automation_context.json", "w") as f:
        json.dump(automation_context, f)
    with open("function_inputs.json", "w") as f:
        json.dump(function_inputs, f)
    # Run contract entrypoint
    result = subprocess.run([
        "python", "main.py",
        json.dumps(automation_context),
        json.dumps(function_inputs)
    ], capture_output=True, text=True)
    # Clean up temp files
    os.remove("automation_context.json")
    os.remove("function_inputs.json")
    # Check result
    assert result.returncode == 0
    assert "error" not in result.stdout.lower()
