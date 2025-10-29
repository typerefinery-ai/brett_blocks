#!/usr/bin/env python3
"""
Test script for debugging get_unattached.py
This script will call get_unattached and both pretty print the output and save it to JSON
"""

import sys
import os
import json
from pprint import pprint

# Add the parent directory to the path so we can import the modules
sys.path.append('../')
sys.path.append('./Block_Families/OS_Triage/Viz_Dataviews/')

# Change to the Orchestration directory since that's where the script expects to run
original_cwd = os.getcwd()
orchestration_dir = os.path.join(os.getcwd(), 'Orchestration')
if os.path.exists(orchestration_dir):
    os.chdir(orchestration_dir)
    print(f"Changed working directory to: {os.getcwd()}")

try:
    from Block_Families.OS_Triage.Viz_Dataviews.get_unattached import main as get_unattached, get_unattached as get_unattached_func
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure the path to get_unattached.py is correct")
    sys.exit(1)

def test_get_unattached():
    """Test the get_unattached function with debugging output"""
    
    print("=" * 60)
    print("TESTING GET_UNATTACHED FUNCTION")
    print("=" * 60)
    
    # Set up paths similar to the notebook
    data_path = ""  # Empty string as used in notebook
    output_file = "test_unattached_output.json"
    
    print(f"Input path: '{data_path}'")
    print(f"Output path: '{output_file}'")
    print()
    
    try:
        print("Calling get_unattached function directly...")
        unattached_data = get_unattached_func()
        
        print("\n" + "=" * 40)
        print("DIRECT FUNCTION CALL RESULTS:")
        print("=" * 40)
        print(f"Type of result: {type(unattached_data)}")
        
        if isinstance(unattached_data, dict):
            print(f"Keys in result: {list(unattached_data.keys())}")
            if 'nodes' in unattached_data:
                print(f"Number of nodes: {len(unattached_data['nodes'])}")
            if 'edges' in unattached_data:
                print(f"Number of edges: {len(unattached_data['edges'])}")
        
        print("\nFull output (pretty printed):")
        pprint(unattached_data, width=120, depth=3)
        
        # Save to JSON file
        with open(output_file, 'w') as f:
            json.dump(unattached_data, f, indent=2)
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Error calling get_unattached function directly: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    
    try:
        print("Calling get_unattached main function...")
        get_unattached(data_path, "test_unattached_main_output.json")
        
        # Try to read the output file
        if os.path.exists("test_unattached_main_output.json"):
            with open("test_unattached_main_output.json", 'r') as f:
                main_result = json.load(f)
            
            print("\n" + "=" * 40)
            print("MAIN FUNCTION CALL RESULTS:")
            print("=" * 40)
            print(f"Type of result: {type(main_result)}")
            
            if isinstance(main_result, dict):
                print(f"Keys in result: {list(main_result.keys())}")
                if 'nodes' in main_result:
                    print(f"Number of nodes: {len(main_result['nodes'])}")
                if 'edges' in main_result:
                    print(f"Number of edges: {len(main_result['edges'])}")
            
            print("\nFull output (pretty printed):")
            pprint(main_result, width=120, depth=3)
            
        else:
            print("Main function output file was not created")
            
    except Exception as e:
        print(f"Error calling get_unattached main function: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

def check_required_files():
    """Check if the required context files exist"""
    print("Checking for required context files...")
    print(f"Current working directory: {os.getcwd()}")
    
    context_dir = "./generated/os-triage/context_mem"
    context_map_file = os.path.join(context_dir, "context_map.json")
    
    print(f"Context directory: {context_dir}")
    print(f"Context directory exists: {os.path.exists(context_dir)}")
    print(f"Context map file: {context_map_file}")
    print(f"Context map file exists: {os.path.exists(context_map_file)}")
    
    if os.path.exists(context_map_file):
        try:
            with open(context_map_file, 'r') as f:
                context_map = json.load(f)
            print(f"Context map contents: {context_map}")
            
            if 'current_incident' in context_map:
                incident_dir = os.path.join(context_dir, context_map['current_incident'])
                print(f"Current incident directory: {incident_dir}")
                print(f"Incident directory exists: {os.path.exists(incident_dir)}")
                
                if os.path.exists(incident_dir):
                    print("Files in incident directory:")
                    for file in os.listdir(incident_dir):
                        print(f"  - {file}")
                        
        except Exception as e:
            print(f"Error reading context map: {e}")
    
    print()

def cleanup():
    """Restore original working directory"""
    global original_cwd
    if 'original_cwd' in globals():
        os.chdir(original_cwd)
        print(f"Restored working directory to: {os.getcwd()}")

if __name__ == "__main__":
    try:
        print("Starting get_unattached.py test script")
        print()
        
        check_required_files()
        test_get_unattached()
    finally:
        cleanup()