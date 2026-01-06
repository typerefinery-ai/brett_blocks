"""
Test Step 3 sequence chaining in isolation
"""
import os
import sys
import json

# Add path for imports
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

from Utilities.local_make_general import invoke_make_sequence_block, invoke_chain_sequence_block, invoke_save_incident_context_block

# Setup paths
results_base = "./Results/"
os.makedirs(results_base + "step3/context", exist_ok=True)

# Create a simple task object
task_obj = {
    "type": "task",
    "spec_version": "2.1",
    "id": "task--test-step3-12345678-1234-1234-1234-123456789abc",
    "created": "2025-01-15T08:15:00.000Z",
    "modified": "2025-01-15T08:15:00.000Z",
    "name": "Handle User Report",
    "description": "Investigate user-reported suspicious email"
}

print("=" * 60)
print("TESTING STEP 3 SEQUENCE CHAINING")
print("=" * 60)

try:
    print("\n1. Creating sequence object...")
    sequence_data_path = "SDO/Sequence/sequence_anecdote.json"
    results_path = "step3/sequence_task_anecdote.json"

    seq_handle_report = invoke_make_sequence_block(
        sequence_data_path,
        results_path,
        step_type="single_step",
        sequence_type="task",
        sequenced_object=task_obj["id"],
        on_completion=None,
        on_success=None,
        on_failure=None,
        next_steps=None
    )

    print(f"✅ Sequence created: {seq_handle_report['id']}")
    print(f"   - Step type: {seq_handle_report.get('step_type', 'N/A')}")
    print(f"   - Sequence type: {seq_handle_report.get('sequence_type', 'N/A')}")

    print("\n2. Chaining sequence to Step 2 workflow...")
    print(f"   Input: {results_base + results_path}")
    chain_results_path = results_base + "step3/chain_sequence_result.json"
    print(f"   Output: {chain_results_path}")
    
    print("\n   Calling invoke_chain_sequence_block...")
    result = invoke_chain_sequence_block(results_base + results_path, chain_results_path)
    
    print(f"✅ Sequence chained: {result}")

    print("\n3. Saving to incident context...")
    sequence_results_obj_path = results_base + results_path
    sequence_results_context_path = results_base + "step3/context/sequence_anecdote_context.json"

    result = invoke_save_incident_context_block(
        sequence_results_obj_path,
        sequence_results_context_path
    )

    print(f"✅ Sequence saved to incident: {result}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ TEST FAILED")
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
