#!/usr/bin/env python3
"""
STIX Reconstitution Test Runner

This script runs comprehensive tests of the STIX object reconstitution process:
1. Clears generated directories
2. Loads STIX objects from Block_Families/examples
3. Runs full reconstitution pipeline
4. Compares input vs output objects using DeepDiff
5. Reports on successes and failures

The comparison ignores UUID differences but validates structural integrity.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from deepdiff import DeepDiff
import traceback

# Import our reconstitution module from Orchestration.Utilities
import sys
from pathlib import Path

# Add parent directory to path to import from Orchestration
sys.path.insert(0, str(Path(__file__).parent.parent))

from Orchestration.Utilities.reconstitute_object_list import reconstitute_object_list


class STIXReconstitutionTestRunner:
    """Comprehensive test runner for STIX reconstitution"""
    
    def __init__(self):
        """Initialize the test runner"""
        self.project_root = Path(__file__).parent.parent
        self.test_dir = Path(__file__).parent
        self.generated_dir = self.test_dir / "generated"
        self.examples_dir = self.project_root / "Block_Families" / "examples"
        
        # Results tracking
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'comparison_results': [],
            'detailed_failures': []
        }
    
    def normalize_object_for_comparison(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a STIX object for comparison by removing/normalizing fields
        that are expected to differ (like UUIDs and timestamps).
        """
        import copy
        normalized = copy.deepcopy(obj)
        
        # Replace UUID-based IDs with normalized placeholders
        if 'id' in normalized:
            obj_type = normalized.get('type', 'unknown')
            normalized['id'] = f"{obj_type}--normalized-uuid"
        
        # Normalize timestamps to a standard format for comparison
        for time_field in ['created', 'modified']:
            if time_field in normalized:
                normalized[time_field] = "2023-01-01T00:00:00.000Z"
        
        # Recursively normalize references
        def normalize_references(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    # Standard reference fields ending with _ref or _refs
                    if key.endswith('_ref') and isinstance(value, str) and '--' in value:
                        # Normalize single reference
                        ref_type = value.split('--')[0]
                        data[key] = f"{ref_type}--normalized-uuid"
                    elif key.endswith('_refs') and isinstance(value, list):
                        # Normalize reference list
                        normalized_refs = []
                        for ref in value:
                            if isinstance(ref, str) and '--' in ref:
                                ref_type = ref.split('--')[0]
                                normalized_refs.append(f"{ref_type}--normalized-uuid")
                            else:
                                normalized_refs.append(ref)
                        data[key] = normalized_refs
                    # Special sequence reference fields that don't follow _ref naming
                    elif key in ['on_completion', 'on_success', 'on_failure', 'sequenced_object'] and isinstance(value, str) and '--' in value:
                        ref_type = value.split('--')[0]
                        data[key] = f"{ref_type}--normalized-uuid"
                    # next_steps is a list of sequence references
                    elif key == 'next_steps' and isinstance(value, list):
                        normalized_refs = []
                        for ref in value:
                            if isinstance(ref, str) and '--' in ref:
                                ref_type = ref.split('--')[0]
                                normalized_refs.append(f"{ref_type}--normalized-uuid")
                            else:
                                normalized_refs.append(ref)
                        data[key] = normalized_refs
                    elif isinstance(value, (dict, list)):
                        normalize_references(value)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, (dict, list)):
                        normalize_references(item)
        
        normalize_references(normalized)
        return normalized
    
    def compare_objects(self, original: Dict[str, Any], reconstituted: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare an original object with its reconstituted version.
        Returns comparison results including any differences.
        """
        
        # Normalize both objects for fair comparison
        norm_original = self.normalize_object_for_comparison(original)
        norm_reconstituted = self.normalize_object_for_comparison(reconstituted)
        
        # Perform deep comparison with DeepDiff
        diff = DeepDiff(
            norm_original, 
            norm_reconstituted,
            ignore_order=True,
            exclude_paths=["root['id']", "root['created']", "root['modified']"]
        )
        
        return {
            'original_id': original.get('id', 'unknown'),
            'reconstituted_id': reconstituted.get('id', 'unknown'),
            'original_type': original.get('type', 'unknown'),
            'differences': dict(diff) if diff else {},
            'is_identical': len(diff) == 0,
            'comparison_summary': self.summarize_differences(diff)
        }
    
    def summarize_differences(self, diff) -> str:
        """Create a human-readable summary of differences"""
        if not diff:
            return "Objects are structurally identical"
        
        summary_parts = []
        
        if 'values_changed' in diff:
            count = len(diff['values_changed'])
            summary_parts.append(f"{count} value(s) changed")
        
        if 'dictionary_item_added' in diff:
            count = len(diff['dictionary_item_added'])
            summary_parts.append(f"{count} field(s) added")
        
        if 'dictionary_item_removed' in diff:
            count = len(diff['dictionary_item_removed'])
            summary_parts.append(f"{count} field(s) removed")
        
        if 'iterable_item_added' in diff:
            count = len(diff['iterable_item_added'])
            summary_parts.append(f"{count} list item(s) added")
        
        if 'iterable_item_removed' in diff:
            count = len(diff['iterable_item_removed'])
            summary_parts.append(f"{count} list item(s) removed")
        
        return "; ".join(summary_parts) if summary_parts else "Unknown differences"
    
    def build_original_to_reconstituted_map(self, reconstituted_objects: List[Dict], reconstitution_report: Dict) -> Dict[str, Dict]:
        """
        Build a mapping from original object_id -> reconstituted object using
        the creation_sequence available in the reconstitution metadata. The
        reconstituted_objects list is produced in the same order as the
        creation_sequence, so we can zip them together deterministically.
        """
        mapping = {}
        recon_data = reconstitution_report.get('reconstitution_data', {}) if reconstitution_report else {}
        creation_sequence = recon_data.get('creation_sequence', []) if recon_data else []

        for idx, seq_entry in enumerate(creation_sequence):
            original_id = seq_entry.get('object_id')
            if idx < len(reconstituted_objects):
                mapping[original_id] = reconstituted_objects[idx]

        return mapping
    
    def run_comparison_tests(self, original_objects: List[Dict], reconstituted_objects: List[Dict], reconstitution_report: Dict) -> Dict[str, Any]:
        """Run comprehensive comparison tests between original and reconstituted objects"""
        print("\n🔍 Running comparison tests...\n")
        # Build mapping from original_id -> reconstituted object using creation_sequence
        mapping = self.build_original_to_reconstituted_map(reconstituted_objects, reconstitution_report)

        comparison_results = []
        unmatched_originals = []

        for original_obj in original_objects:
            orig_id = original_obj.get('id')
            reconstituted_obj = mapping.get(orig_id)

            self.test_results['total_tests'] += 1

            if reconstituted_obj:
                comparison = self.compare_objects(original_obj, reconstituted_obj)
                comparison_results.append(comparison)

                if comparison['is_identical']:
                    self.test_results['passed_tests'] += 1
                    print(f"   ✅ {comparison['original_type']}: {comparison['comparison_summary']}")
                else:
                    self.test_results['failed_tests'] += 1
                    print(f"   ❌ {comparison['original_type']}: {comparison['comparison_summary']}")
                    self.test_results['detailed_failures'].append({
                        'original_id': comparison['original_id'],
                        'type': comparison['original_type'],
                        'differences': comparison['differences'],
                        'summary': comparison['comparison_summary']
                    })
            else:
                unmatched_originals.append(original_obj)
                self.test_results['failed_tests'] += 1

        # Report unmatched originals
        if unmatched_originals:
            print(f"\n   ⚠️  {len(unmatched_originals)} original objects had no reconstituted counterparts:")
            for obj in unmatched_originals[:5]:
                print(f"      - {obj.get('type', 'unknown')}: {obj.get('id', 'unknown ID')}")
            if len(unmatched_originals) > 5:
                print(f"      ... and {len(unmatched_originals) - 5} more")

        self.test_results['comparison_results'] = comparison_results

        return {
            'total_comparisons': len(comparison_results),
            'identical_objects': len([r for r in comparison_results if r['is_identical']]),
            'different_objects': len([r for r in comparison_results if not r['is_identical']]),
            'unmatched_originals': len(unmatched_originals),
            'comparison_details': comparison_results
        }
    
    def generate_detailed_report(self, reconstitution_report: Dict, comparison_report: Dict) -> str:
        """Generate a comprehensive test report"""
        
        report_lines = [
            "=" * 80,
            "STIX RECONSTITUTION TEST REPORT",
            "=" * 80,
            "",
            "📊 RECONSTITUTION SUMMARY:",
            f"   Input Directory: {reconstitution_report.get('input_directory', 'Unknown')}",
            f"   Original Objects: {reconstitution_report.get('original_objects_count', 0)}",
            f"   Data Forms Success Rate: {reconstitution_report.get('data_forms_success_rate', 0):.1f}%",
            f"   Reconstituted Objects: {reconstitution_report.get('reconstituted_objects_count', 0)}",
            f"   Reconstitution Success Rate: {reconstitution_report.get('reconstitution_success_rate', 0):.1f}%",
            "",
            "📁 GENERATED FILES:",
            f"   Input Objects: {reconstitution_report.get('generated_files', {}).get('input_objects', 0)}",
            f"   Data Forms: {reconstitution_report.get('generated_files', {}).get('data_forms', 0)}",
            f"   Output Objects: {reconstitution_report.get('generated_files', {}).get('output_objects', 0)}",
            "",
            "🔍 COMPARISON RESULTS:",
            f"   Total Comparisons: {comparison_report.get('total_comparisons', 0)}",
            f"   Identical Objects: {comparison_report.get('identical_objects', 0)}",
            f"   Different Objects: {comparison_report.get('different_objects', 0)}",
            f"   Unmatched Originals: {comparison_report.get('unmatched_originals', 0)}",
            f"   Unmatched Reconstituted: {comparison_report.get('unmatched_reconstituted', 0)}",
            "",
            "🎯 TEST STATISTICS:",
            f"   Total Tests: {self.test_results['total_tests']}",
            f"   Passed Tests: {self.test_results['passed_tests']}",
            f"   Failed Tests: {self.test_results['failed_tests']}",
            f"   Success Rate: {(self.test_results['passed_tests'] / max(self.test_results['total_tests'], 1) * 100):.1f}%",
        ]
        
        # Add failure details if any
        if self.test_results['detailed_failures']:
            report_lines.extend([
                "",
                "❌ DETAILED FAILURES:",
                ""
            ])
            
            for failure in self.test_results['detailed_failures'][:10]:  # Show first 10 failures
                report_lines.extend([
                    f"   Object: {failure['type']} ({failure['original_id']})",
                    f"   Issue: {failure['summary']}",
                    ""
                ])
            
            if len(self.test_results['detailed_failures']) > 10:
                remaining = len(self.test_results['detailed_failures']) - 10
                report_lines.append(f"   ... and {remaining} more failures")
        
        report_lines.extend([
            "",
            "=" * 80
        ])
        
        return "\n".join(report_lines)
    
    def save_test_results(self, reconstitution_report: Dict, comparison_report: Dict):
        """Save test results and reports to files"""
        
        # Convert any non-serializable objects to strings
        def make_json_serializable(obj):
            if hasattr(obj, '__dict__'):
                return str(obj)
            elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
                try:
                    return list(obj)
                except:
                    return str(obj)
            else:
                return obj
        
        # Clean the data for JSON serialization
        def clean_for_json(data):
            if isinstance(data, dict):
                return {k: clean_for_json(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [clean_for_json(item) for item in data]
            else:
                try:
                    # Test if it's JSON serializable
                    json.dumps(data)
                    return data
                except (TypeError, ValueError):
                    return make_json_serializable(data)
        
        # Save detailed test results
        results_file = self.generated_dir / "test_results.json"
        cleaned_results = clean_for_json({
            'reconstitution_report': reconstitution_report,
            'comparison_report': comparison_report,
            'test_statistics': self.test_results
        })
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_results, f, indent=2, ensure_ascii=False)
        
        # Save human-readable report
        report_text = self.generate_detailed_report(reconstitution_report, comparison_report)
        report_file = self.generated_dir / "test_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"\n📝 Test results saved:")
        print(f"   📊 JSON results: {results_file}")
        print(f"   📄 Text report: {report_file}")
    
    def run_full_test_suite(self) -> bool:
        """Run the complete test suite"""
        print("🚀 Starting STIX Reconstitution Test Suite\n")
        print("=" * 60)
        
        try:
            # Verify examples directory exists
            if not self.examples_dir.exists():
                print(f"❌ Examples directory not found: {self.examples_dir}")
                print("   Please ensure Block_Families/examples directory exists with STIX objects")
                return False
            
            print(f"📂 Using examples directory: {self.examples_dir}")
            print(f"📁 Generated files directory: {self.generated_dir}")
            
            # Run reconstitution
            print("\n" + "=" * 60)
            original_objects, reconstituted_objects, reconstitution_report = reconstitute_object_list(
                str(self.examples_dir), 
                str(self.generated_dir)
            )
            
            # Run comparisons
            print("\n" + "=" * 60)
            comparison_report = self.run_comparison_tests(original_objects, reconstituted_objects, reconstitution_report)
            
            # Generate and display report
            print("\n" + "=" * 60)
            report_text = self.generate_detailed_report(reconstitution_report, comparison_report)
            print(report_text)
            
            # Save results
            self.save_test_results(reconstitution_report, comparison_report)
            
            # Determine overall success
            success_rate = (self.test_results['passed_tests'] / max(self.test_results['total_tests'], 1)) * 100
            overall_success = success_rate >= 80.0  # 80% threshold for success
            
            if overall_success:
                print(f"\n🎉 TEST SUITE PASSED! Success rate: {success_rate:.1f}%")
            else:
                print(f"\n💥 TEST SUITE FAILED! Success rate: {success_rate:.1f}%")
            
            return overall_success
            
        except Exception as e:
            print(f"\n❌ Test suite failed with exception: {str(e)}")
            traceback.print_exc()
            return False


def main():
    """Main entry point for the test runner"""
    runner = STIXReconstitutionTestRunner()
    success = runner.run_full_test_suite()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()