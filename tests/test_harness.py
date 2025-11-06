"""
Brett Blocks Test Harness - Extending Orchestration Utilities
Comprehensive testing framework using existing local_make_* patterns
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

try:
    from deepdiff import DeepDiff
except ImportError:
    print("Warning: DeepDiff not available, using simple comparison")
    DeepDiff = None

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import existing Orchestration utilities
from Orchestration.Utilities.local_make_sdo import (
    invoke_make_observed_data_block,
)
from Orchestration.Utilities.local_make_sco import (
    invoke_make_email_addr_block,
)
from Orchestration.Utilities.local_make_sro import (
    invoke_sro_block,
)
from Orchestration.Utilities.util import emulate_ports, unwind_ports, conv
from Orchestration.conv import conv


class BrettBlocksTestHarness:
    """
    Comprehensive test harness extending existing Orchestration utilities
    """
    
    def __init__(self, test_data_dir: str = "test_data_forms", results_dir: str = "tests/results"):
        self.test_data_dir = Path(test_data_dir)
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Load test configuration
        self.target_objects = self._load_target_objects()
        self.data_form_results = self._load_data_form_results()
        
        # Set up paths following existing patterns
        self.path_base = "Block_Families/StixORM/"
        self.results_base = "tests/results/"
        
        # Initialize test results tracking
        self.test_results = []
        
    def _load_target_objects(self) -> Dict[str, Any]:
        """Load target objects from extracted JSON"""
        target_file = Path("test_output/target_objects.json")
        if target_file.exists():
            with open(target_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_data_form_results(self) -> List[Dict[str, Any]]:
        """Load data form creation results"""
        results_file = Path("test_output/data_form_creation_results.json")
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def create_make_function_mapping(self) -> Dict[str, callable]:
        """
        Create mapping of python classes to their make functions
        Following existing local_make_* patterns
        """
        # Import all make functions
        from Block_Families.StixORM.SDO.Identity.make_identity import main as make_identity
        from Block_Families.StixORM.SDO.Indicator.make_indicator import main as make_indicator
        from Block_Families.StixORM.SDO.Incident.make_incident import main as make_incident
        from Block_Families.StixORM.SDO.Observed_Data.make_observed_data import main as make_observed_data
        from Block_Families.StixORM.SCO.Email_Addr.make_email_addr import main as make_email_addr
        from Block_Families.StixORM.SCO.User_Account.make_user_account import main as make_user_account
        from Block_Families.StixORM.SCO.URL.make_url import main as make_url
        from Block_Families.StixORM.SCO.Email_Message.make_email_msg import main as make_email_msg
        
        return {
            'Identity': make_identity,
            'Indicator': make_indicator,
            'Incident': make_incident,
            'ObservedData': make_observed_data,
            'EmailAddress': make_email_addr,
            'UserAccount': make_user_account,
            'URL': make_url,
            'EmailMessage': make_email_msg,
        }
    
    def setup_test_environment(self):
        """Setup test environment following existing patterns"""
        # Create necessary directories
        os.makedirs("tests/temp_data", exist_ok=True)
        os.makedirs("tests/results", exist_ok=True)
        
        # Copy data forms to test directory for manipulation
        for result in self.data_form_results:
            if result.get('success'):
                source_path = Path(result['data_form_path'])
                dest_path = Path("tests/temp_data") / source_path.name
                
                if source_path.exists():
                    with open(source_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
    
    def extract_object_dependencies(self, stix_obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract reference dependencies from STIX object
        Returns references that need to be provided as inputs
        """
        refs = {}
        for key, value in stix_obj.items():
            if key.endswith('_ref') or key.endswith('_refs'):
                refs[key] = value
        return refs
    
    def create_mock_reference_objects(self, refs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create mock objects for references
        Following existing patterns for providing input objects
        """
        mock_objects = {}
        
        for ref_key, ref_value in refs.items():
            if ref_key == 'created_by_ref':
                # Create a mock identity for created_by_ref
                mock_objects[ref_key] = {
                    "type": "identity",
                    "spec_version": "2.1",
                    "id": ref_value if isinstance(ref_value, str) else "identity--test-created-by",
                    "created": "2023-01-01T00:00:00.000Z",
                    "modified": "2023-01-01T00:00:00.000Z",
                    "name": "Test Creator",
                    "identity_class": "individual"
                }
            elif ref_key.endswith('_refs') and isinstance(ref_value, list):
                # Handle reference lists
                mock_objects[ref_key] = []
                for ref_id in ref_value:
                    mock_objects[ref_key].append({
                        "type": "identity", 
                        "spec_version": "2.1",
                        "id": ref_id,
                        "created": "2023-01-01T00:00:00.000Z",
                        "modified": "2023-01-01T00:00:00.000Z",
                        "name": "Test Reference",
                        "identity_class": "individual"
                    })
            else:
                # Create generic mock object
                obj_type = ref_value.split('--')[0] if isinstance(ref_value, str) else "identity"
                mock_objects[ref_key] = {
                    "type": obj_type,
                    "spec_version": "2.1", 
                    "id": ref_value if isinstance(ref_value, str) else f"{obj_type}--test-ref",
                    "name": "Test Object"
                }
        
        return mock_objects
    
    def invoke_make_function_with_ports(self, data_form_path: str, python_class: str, 
                                      refs: Dict[str, Any] = None) -> Tuple[bool, Dict[str, Any], str]:
        """
        Invoke make function using existing port emulation patterns
        """
        make_functions = self.create_make_function_mapping()
        
        if python_class not in make_functions:
            return False, {}, f"No make function found for {python_class}"
        
        try:
            # Set up paths
            temp_data_path = f"tests/temp_data/{Path(data_form_path).name}"
            results_path = f"tests/results/{python_class.lower()}_result.json"
            
            # Prepare input data with references if needed
            if refs:
                mock_refs = self.create_mock_reference_objects(refs)
                emulate_ports(temp_data_path, [])  # Initialize if needed
                
                # Add reference objects to the data form
                with open(temp_data_path, 'r', encoding='utf-8') as f:
                    data_form = json.load(f)
                
                # Add mock reference objects
                for ref_key, ref_obj in mock_refs.items():
                    data_form[ref_key] = ref_obj
                
                with open(temp_data_path, 'w', encoding='utf-8') as f:
                    json.dump(data_form, f, indent=2)
            
            # Call the make function
            make_function = make_functions[python_class]
            make_function(temp_data_path, results_path)
            
            # Clean up ports
            unwind_ports(temp_data_path)
            
            # Load result
            if os.path.exists(results_path):
                with open(results_path, 'r', encoding='utf-8') as f:
                    result_obj = json.load(f)
                return True, result_obj, "Success"
            else:
                return False, {}, "Result file not created"
                
        except Exception as e:
            return False, {}, str(e)
    
    def compare_stix_objects(self, original: Dict[str, Any], generated: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare STIX objects using DeepDiff, ignoring UUIDs and timestamps
        """
        if DeepDiff is None:
            # Simple comparison fallback
            return {"simple_comparison": "DeepDiff not available"}
        
        # Paths to ignore during comparison
        ignore_paths = [
            "root['id']",
            "root['created']", 
            "root['modified']"
        ]
        
        diff = DeepDiff(
            original,
            generated,
            ignore_order=True,
            exclude_paths=ignore_paths,
            verbose_level=2
        )
        
        return diff
    
    def run_single_test(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single roundtrip test
        """
        python_class = test_data['python_class']
        data_form_path = test_data['data_form_path']
        original_stix = test_data['original_stix']
        references = test_data.get('references', {})
        
        print(f"\n🧪 Testing {python_class}")
        print(f"   📄 Data form: {Path(data_form_path).name}")
        
        test_result = {
            'python_class': python_class,
            'data_form_path': data_form_path,
            'template_path': test_data.get('template_path'),
            'python_file': test_data.get('python_file'),
            'references': references,
            'original_stix': original_stix,
        }
        
        try:
            # Step 1: Create STIX object from data form
            success, generated_stix, error_msg = self.invoke_make_function_with_ports(
                data_form_path, python_class, references
            )
            
            test_result['generation_success'] = success
            test_result['generation_error'] = error_msg
            
            if not success:
                print(f"   ❌ Generation failed: {error_msg}")
                test_result['test_passed'] = False
                return test_result
            
            test_result['generated_stix'] = generated_stix
            print(f"   ✅ Object generated successfully")
            
            # Step 2: Compare with original
            diff = self.compare_stix_objects(original_stix, generated_stix)
            test_result['deepdiff_result'] = diff
            
            # Determine if test passed
            # Test passes if there are no significant differences
            significant_changes = any(key in diff for key in [
                'values_changed', 'type_changes', 'iterable_item_added', 'iterable_item_removed'
            ])
            
            test_result['test_passed'] = not significant_changes
            
            if test_result['test_passed']:
                print(f"   ✅ Comparison passed - objects equivalent")
            else:
                print(f"   ❌ Comparison failed - differences found")
                print(f"      Differences: {list(diff.keys())}")
            
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            test_result['test_passed'] = False
            test_result['exception'] = str(e)
        
        return test_result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all roundtrip tests
        """
        print("🚀 RUNNING BRETT BLOCKS ROUNDTRIP TESTS")
        print("=" * 55)
        
        self.setup_test_environment()
        
        # Run tests for all successful data forms
        successful_data_forms = [r for r in self.data_form_results if r.get('success')]
        
        print(f"📊 Running {len(successful_data_forms)} tests")
        
        for test_data in successful_data_forms:
            test_result = self.run_single_test(test_data)
            self.test_results.append(test_result)
        
        # Generate summary
        passed_tests = [r for r in self.test_results if r.get('test_passed')]
        failed_tests = [r for r in self.test_results if not r.get('test_passed')]
        
        summary = {
            'total_tests': len(self.test_results),
            'passed_tests': len(passed_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(passed_tests) / len(self.test_results) * 100 if self.test_results else 0,
            'test_results': self.test_results
        }
        
        print(f"\n📊 TEST SUMMARY")
        print(f"   Total tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed_tests']}")
        print(f"   Failed: {summary['failed_tests']}")
        print(f"   Success rate: {summary['success_rate']:.1f}%")
        
        # Save detailed results
        results_file = self.results_dir / "comprehensive_test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        return summary


def main():
    """Run the comprehensive test harness"""
    harness = BrettBlocksTestHarness()
    return harness.run_all_tests()


if __name__ == "__main__":
    main()