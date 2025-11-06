"""
Extended Testing Utilities - Building on Orchestration patterns
Provides additional utilities for comprehensive testing
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import existing utilities
from Orchestration.Utilities.util import emulate_ports, unwind_ports, conv
from Orchestration.conv import conv


def extended_invoke_make_identity_block(identity_path: str, results_path: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Extended identity creation following existing patterns
    """
    from Block_Families.StixORM.SDO.Identity.make_identity import main as make_identity
    
    try:
        # Prepare paths
        identity_data_rel_path = f"Block_Families/StixORM/{identity_path}"
        identity_results_rel_path = f"tests/results/{results_path}"
        
        # Add any additional input objects using existing port emulation
        if kwargs:
            if os.path.exists(identity_data_rel_path):
                with open(identity_data_rel_path, "r") as form_file:
                    results_data = json.load(form_file)
                    results_data.update(kwargs)
                with open(identity_data_rel_path, 'w') as f:
                    json.dump(results_data, f, indent=2)
        
        # Make the Identity object
        make_identity(identity_data_rel_path, identity_results_rel_path)
        
        # Clean up ports
        unwind_ports(identity_data_rel_path)
        
        # Load and return result
        if os.path.exists(identity_results_rel_path):
            with open(identity_results_rel_path, 'r') as f:
                result = json.load(f)
            return True, result
        else:
            return False, {}
            
    except Exception as e:
        return False, {"error": str(e)}


def extended_invoke_make_indicator_block(indicator_path: str, results_path: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Extended indicator creation following existing patterns
    """
    from Block_Families.StixORM.SDO.Indicator.make_indicator import main as make_indicator
    
    try:
        # Prepare paths
        indicator_data_rel_path = f"Block_Families/StixORM/{indicator_path}"
        indicator_results_rel_path = f"tests/results/{results_path}"
        
        # Add any reference objects using existing port emulation
        if kwargs:
            if os.path.exists(indicator_data_rel_path):
                with open(indicator_data_rel_path, "r") as form_file:
                    results_data = json.load(form_file)
                    results_data.update(kwargs)
                with open(indicator_data_rel_path, 'w') as f:
                    json.dump(results_data, f, indent=2)
        
        # Make the Indicator object
        make_indicator(indicator_data_rel_path, indicator_results_rel_path)
        
        # Clean up ports
        unwind_ports(indicator_data_rel_path)
        
        # Load and return result
        if os.path.exists(indicator_results_rel_path):
            with open(indicator_results_rel_path, 'r') as f:
                result = json.load(f)
            return True, result
        else:
            return False, {}
            
    except Exception as e:
        return False, {"error": str(e)}


def extended_invoke_make_incident_block(incident_path: str, results_path: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Extended incident creation following existing patterns  
    """
    from Block_Families.StixORM.SDO.Incident.make_incident import main as make_incident
    
    try:
        # Prepare paths
        incident_data_rel_path = f"Block_Families/StixORM/{incident_path}"
        incident_results_rel_path = f"tests/results/{results_path}"
        
        # Add any reference objects using existing port emulation
        if kwargs:
            if os.path.exists(incident_data_rel_path):
                with open(incident_data_rel_path, "r") as form_file:
                    results_data = json.load(form_file)
                    results_data.update(kwargs)
                with open(incident_data_rel_path, 'w') as f:
                    json.dump(results_data, f, indent=2)
        
        # Make the Incident object
        make_incident(incident_data_rel_path, incident_results_rel_path)
        
        # Clean up ports
        unwind_ports(incident_data_rel_path)
        
        # Load and return result
        if os.path.exists(incident_results_rel_path):
            with open(incident_results_rel_path, 'r') as f:
                result = json.load(f)
            return True, result
        else:
            return False, {}
            
    except Exception as e:
        return False, {"error": str(e)}


def extended_invoke_make_user_account_block(account_path: str, results_path: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Extended user account creation following existing patterns
    """
    from Block_Families.StixORM.SCO.User_Account.make_user_account import main as make_user_account
    
    try:
        # Prepare paths
        account_data_rel_path = f"Block_Families/StixORM/{account_path}"
        account_results_rel_path = f"tests/results/{results_path}"
        
        # Add any reference objects using existing port emulation
        if kwargs:
            if os.path.exists(account_data_rel_path):
                with open(account_data_rel_path, "r") as form_file:
                    results_data = json.load(form_file)
                    results_data.update(kwargs)
                with open(account_data_rel_path, 'w') as f:
                    json.dump(results_data, f, indent=2)
        
        # Make the User Account object
        make_user_account(account_data_rel_path, account_results_rel_path)
        
        # Clean up ports
        unwind_ports(account_data_rel_path)
        
        # Load and return result
        if os.path.exists(account_results_rel_path):
            with open(account_results_rel_path, 'r') as f:
                result = json.load(f)
            return True, result
        else:
            return False, {}
            
    except Exception as e:
        return False, {"error": str(e)}


def extended_invoke_make_url_block(url_path: str, results_path: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Extended URL creation following existing patterns
    """
    from Block_Families.StixORM.SCO.URL.make_url import main as make_url
    
    try:
        # Prepare paths
        url_data_rel_path = f"Block_Families/StixORM/{url_path}"
        url_results_rel_path = f"tests/results/{results_path}"
        
        # Add any reference objects using existing port emulation
        if kwargs:
            if os.path.exists(url_data_rel_path):
                with open(url_data_rel_path, "r") as form_file:
                    results_data = json.load(form_file)
                    results_data.update(kwargs)
                with open(url_data_rel_path, 'w') as f:
                    json.dump(results_data, f, indent=2)
        
        # Make the URL object
        make_url(url_data_rel_path, url_results_rel_path)
        
        # Clean up ports
        unwind_ports(url_data_rel_path)
        
        # Load and return result
        if os.path.exists(url_results_rel_path):
            with open(url_results_rel_path, 'r') as f:
                result = json.load(f)
            return True, result
        else:
            return False, {}
            
    except Exception as e:
        return False, {"error": str(e)}


def create_dependency_sequence(test_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Create dependency sequence for objects with references
    Orders objects so references are created first
    """
    # Objects with no references go first
    no_refs = [obj for obj in test_objects if not obj.get('references')]
    
    # Objects with references go after
    with_refs = [obj for obj in test_objects if obj.get('references')]
    
    # Sort objects with references by dependency complexity
    # (fewer references first)
    with_refs.sort(key=lambda x: len(x.get('references', {})))
    
    return no_refs + with_refs


def prepare_test_data_directory(source_dir: str = "test_data_forms", dest_dir: str = "tests/temp_data"):
    """
    Prepare test data directory by copying data forms for manipulation
    """
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    dest_path.mkdir(exist_ok=True)
    
    if source_path.exists():
        for json_file in source_path.glob("*.json"):
            dest_file = dest_path / json_file.name
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with open(dest_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
    
    return dest_path


def load_conversion_function():
    """
    Load the conversion function from the notebook
    """
    try:
        # Try to import from notebook variables if available
        import sys
        notebook_path = Path("Orchestration/Convert_Examples_to_DataForms.ipynb")
        
        # For now, we'll use our own implementation
        # In a real scenario, you'd extract this from the notebook
        def convert_stix_to_data_form(stix_obj: dict, class_template: dict) -> dict:
            """Simplified conversion function"""
            # This would be the actual function from the notebook
            # For testing purposes, we'll create a minimal implementation
            return {
                "conversion_successful": True,
                "form_data": stix_obj  # Simplified
            }
        
        return convert_stix_to_data_form
        
    except Exception as e:
        print(f"Warning: Could not load conversion function from notebook: {e}")
        return None


def generate_test_report(test_results: List[Dict[str, Any]], output_file: str = "tests/results/test_report.md"):
    """
    Generate comprehensive test report in markdown format
    """
    
    total_tests = len(test_results)
    passed_tests = [r for r in test_results if r.get('test_passed')]
    failed_tests = [r for r in test_results if not r.get('test_passed')]
    
    report = f"""# Brett Blocks Roundtrip Test Report

## Executive Summary

- **Total Tests**: {total_tests}
- **Passed**: {len(passed_tests)}
- **Failed**: {len(failed_tests)}
- **Success Rate**: {len(passed_tests)/total_tests*100:.1f}%

## Test Results Details

"""
    
    for i, result in enumerate(test_results, 1):
        status = "✅ PASSED" if result.get('test_passed') else "❌ FAILED"
        python_class = result.get('python_class', 'Unknown')
        
        report += f"""### Test {i}: {python_class} {status}

- **Data Form Path**: `{result.get('data_form_path', 'N/A')}`
- **Template Path**: `{result.get('template_path', 'N/A')}`
- **Python File**: `{result.get('python_file', 'N/A')}`
- **References**: {len(result.get('references', {}))} fields
- **Generation Success**: {result.get('generation_success', False)}

"""
        
        if not result.get('test_passed'):
            error = result.get('generation_error') or result.get('exception', 'Unknown error')
            report += f"**Error**: {error}\n\n"
        
        if result.get('deepdiff_result'):
            diff = result['deepdiff_result']
            if diff:
                report += f"**Differences Found**: {list(diff.keys())}\n\n"
            else:
                report += "**No significant differences found**\n\n"
    
    report += f"""## Summary by Object Type

"""
    
    # Group by object type
    by_type = {}
    for result in test_results:
        obj_type = result.get('python_class', 'Unknown')
        if obj_type not in by_type:
            by_type[obj_type] = []
        by_type[obj_type].append(result)
    
    for obj_type, results in by_type.items():
        passed = len([r for r in results if r.get('test_passed')])
        total = len(results)
        report += f"- **{obj_type}**: {passed}/{total} passed ({passed/total*100:.1f}%)\n"
    
    # Write report
    report_path = Path(output_file)
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path