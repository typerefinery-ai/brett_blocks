#!/usr/bin/env python3
"""
Test Reconstitution Capability

This script tests the enhanced create_data_forms_from_stix_objects function
to ensure it provides sufficient data for proper reconstitution sequencing
and reference restoration.
"""

import json
import sys
import shutil
from pathlib import Path
from collections import defaultdict

# Add utilities to path
sys.path.append(str(Path(__file__).parent.parent / "Orchestration" / "Utilities"))
from convert_object_list_to_data_forms import create_data_forms_from_stix_objects


def create_complex_test_dataset(available_templates):
    """
    Create a complex test dataset with multiple reference types and dependencies
    using only the templates that are actually available.
    """
    
    print(f"📋 Available templates: {list(available_templates.keys())}")
    
    test_objects = []
    
    # Base identifiers for creating predictable IDs
    base_ids = {
        'identity': 'identity--11111111-1111-1111-1111-111111111111',
        'indicator': 'indicator--22222222-2222-2222-2222-222222222222', 
        'incident': 'incident--33333333-3333-3333-3333-333333333333',
        'anecdote': 'anecdote--44444444-4444-4444-4444-444444444444',
        'event': 'event--55555555-5555-5555-5555-555555555555',
        'sequence': 'sequence--66666666-6666-6666-6666-666666666666',
        'task': 'task--77777777-7777-7777-7777-777777777777',
        'sighting': 'sighting--88888888-8888-8888-8888-888888888888',
        'relationship': 'relationship--99999999-9999-9999-9999-999999999999'
    }
    
    # Level 1: No dependencies - Identity (if available)
    if 'identity' in available_templates:
        test_objects.append({
            "type": "identity",
            "spec_version": "2.1", 
            "id": base_ids['identity'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Test Organization",
            "identity_class": "organization"
        })
    
    # Level 2: Simple dependencies - Indicator referencing identity (if both available)
    if 'indicator' in available_templates and 'identity' in available_templates:
        test_objects.append({
            "type": "indicator",
            "spec_version": "2.1",
            "id": base_ids['indicator'],
            "created": "2023-01-01T00:00:00.000Z", 
            "modified": "2023-01-01T00:00:00.000Z",
            "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
            "labels": ["malicious-activity"],
            "created_by_ref": base_ids['identity']
        })
    
    # Level 2: Anecdote with reference (if both available)
    if 'anecdote' in available_templates and 'identity' in available_templates:
        test_objects.append({
            "type": "anecdote",
            "spec_version": "2.1",
            "id": base_ids['anecdote'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Detection Event",
            "description": "Suspicious activity detected",
            "created_by_ref": base_ids['identity']
        })
    
    # Level 3: Incident with multiple references (if available)
    if 'incident' in available_templates and 'identity' in available_templates:
        incident_obj = {
            "type": "incident", 
            "spec_version": "2.1",
            "id": base_ids['incident'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z", 
            "name": "Test Security Incident",
            "created_by_ref": base_ids['identity']
        }
        
        # Add extensions if anecdote and event are available
        if 'anecdote' in available_templates and 'event' in available_templates:
            incident_obj["extensions"] = {
                "extension-definition--7cc33dd6-f6a1-489b-98ea-522d351d71b9": {
                    "extension_type": "new-sdo",
                    "anecdotes": [base_ids['anecdote']],
                    "context_labels": ["network", "endpoint"],
                    "event_refs": [base_ids['event']]
                }
            }
        
        test_objects.append(incident_obj)
    
    # Level 2: Event with references (if available)
    if 'event' in available_templates and 'identity' in available_templates:
        event_obj = {
            "type": "event", 
            "spec_version": "2.1",
            "id": base_ids['event'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Network Event",
            "description": "Suspicious network activity",
            "created_by_ref": base_ids['identity']
        }
        
        # Add sighting reference if available
        if 'sighting' in available_templates:
            event_obj["sighting_refs"] = [base_ids['sighting']]
        
        test_objects.append(event_obj)
    
    # Level 1: Sighting (if available)
    if 'sighting' in available_templates and 'identity' in available_templates:
        sighting_obj = {
            "type": "sighting",
            "spec_version": "2.1",
            "id": base_ids['sighting'], 
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "created_by_ref": base_ids['identity']
        }
        
        # Add indicator reference if available
        if 'indicator' in available_templates:
            sighting_obj["sighting_of_ref"] = base_ids['indicator']
            sighting_obj["where_sighted_refs"] = [base_ids['identity']]
        
        test_objects.append(sighting_obj)
    
    # Level 4: Sequence with task dependencies (if available)
    if 'sequence' in available_templates and 'task' in available_templates and 'identity' in available_templates:
        sequence_obj = {
            "type": "sequence",
            "spec_version": "2.1",
            "id": base_ids['sequence'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Response Sequence",
            "created_by_ref": base_ids['identity'],
            "sequence_refs": [base_ids['task']]
        }
        
        # Add incident reference if available
        if 'incident' in available_templates:
            sequence_obj["sequenced_object"] = base_ids['incident']
        
        test_objects.append(sequence_obj)
    
    # Level 3: Task (if available)
    if 'task' in available_templates and 'identity' in available_templates:
        test_objects.append({
            "type": "task", 
            "spec_version": "2.1",
            "id": base_ids['task'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Analysis Task",
            "created_by_ref": base_ids['identity']
        })
    
    # Level 2: Relationship (if available)
    if 'relationship' in available_templates and 'identity' in available_templates:
        relationship_obj = {
            "type": "relationship",
            "spec_version": "2.1",
            "id": base_ids['relationship'],
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "relationship_type": "indicates",
            "source_ref": base_ids['identity'],
            "target_ref": base_ids['identity'],
            "created_by_ref": base_ids['identity']
        }
        
        # Use indicator as source if available
        if 'indicator' in available_templates:
            relationship_obj["source_ref"] = base_ids['indicator']
        
        test_objects.append(relationship_obj)
    
    print(f"   Created {len(test_objects)} objects using available templates")
    return test_objects


def analyze_reconstitution_data(reconstitution_file: Path):
    """
    Analyze the reconstitution data to verify it contains all necessary elements
    for proper object recreation and sequencing.
    """
    
    with open(reconstitution_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== RECONSTITUTION DATA ANALYSIS ===\n")
    
    # 1. Verify metadata completeness
    metadata = data.get('metadata', {})
    print(f"📊 Total Objects: {metadata.get('total_objects', 0)}")
    print(f"📋 Objects with References: {metadata.get('objects_with_references', 0)}")  
    print(f"📝 Objects without References: {metadata.get('objects_without_references', 0)}")
    print(f"🔗 Total Extracted References: {metadata.get('total_extracted_references', 0)}")
    print()
    
    # 2. Verify ID mapping completeness
    id_mapping = data.get('id_to_filename_mapping', {})
    form_mapping = data.get('id_to_form_name_mapping', {})
    print(f"🗂️  ID → Filename Mappings: {len(id_mapping)}")
    print(f"📑 ID → Form Name Mappings: {len(form_mapping)}")
    
    if len(id_mapping) != len(form_mapping):
        print("❌ ERROR: Mapping counts don't match!")
    else:
        print("✅ Mapping completeness verified")
    print()
    
    # 3. Analyze dependency graph
    dependency_graph = data.get('dependency_graph', {})
    print(f"🌐 Dependency Graph Entries: {len(dependency_graph)}")
    
    objects_without_deps = [obj_id for obj_id, info in dependency_graph.items() 
                           if not info.get('depends_on', [])]
    objects_with_deps = [obj_id for obj_id, info in dependency_graph.items()
                        if info.get('depends_on', [])]
    
    print(f"🏁 Objects without dependencies: {len(objects_without_deps)}")
    print(f"🔗 Objects with dependencies: {len(objects_with_deps)}")
    print()
    
    # 4. Verify creation sequence
    creation_sequence = data.get('creation_sequence', [])
    print(f"📋 Creation Sequence Length: {len(creation_sequence)}")
    
    if creation_sequence:
        print("📝 Creation Sequence Order:")
        for i, item in enumerate(creation_sequence[:5]):  # Show first 5
            deps_count = len(item.get('dependencies', []))
            print(f"  {item.get('sequence_order', i+1)}. {item.get('object_type')} ({deps_count} deps)")
        
        if len(creation_sequence) > 5:
            print(f"  ... ({len(creation_sequence) - 5} more)")
    print()
    
    # 5. Analyze detailed reference extraction
    detailed_refs = data.get('detailed_reference_extraction', [])
    print(f"🔍 Detailed Reference Entries: {len(detailed_refs)}")
    
    reference_types = defaultdict(int)
    field_patterns = defaultdict(int)
    
    for ref_entry in detailed_refs:
        if ref_entry.get('has_references', False):
            extracted = ref_entry.get('extracted_references', {})
            for field_path, ref_data in extracted.items():
                ref_type = ref_data.get('type', 'unknown')
                reference_types[ref_type] += 1
                
                # Analyze field patterns
                if field_path.endswith('_ref'):
                    field_patterns['_ref fields'] += 1
                elif field_path.endswith('_refs'):
                    field_patterns['_refs fields'] += 1
                else:
                    field_patterns['embedded STIX IDs'] += 1
    
    print("📊 Reference Type Distribution:")
    for ref_type, count in reference_types.items():
        print(f"  {ref_type}: {count}")
    
    print("\n📊 Field Pattern Distribution:")
    for pattern, count in field_patterns.items():
        print(f"  {pattern}: {count}")
    print()
    
    # 6. Check reconstitution instructions
    instructions = data.get('reconstitution_instructions', {})
    print(f"📋 Reconstitution Instructions: {len(instructions)} steps")
    for step, instruction in instructions.items():
        print(f"  {step}: {instruction}")
    print()
    
    # 7. Verify critical requirements
    print("=== CRITICAL REQUIREMENTS VERIFICATION ===")
    
    requirements_met = []
    requirements_failed = []
    
    # Requirement 1: All extracted IDs tracked with field names and order
    all_refs_detailed = True
    for ref_entry in detailed_refs:
        if ref_entry.get('has_references', False):
            extracted = ref_entry.get('extracted_references', {})
            for field_path, ref_data in extracted.items():
                if ref_data.get('type') == 'list':
                    if 'original_values' not in ref_data or 'order_matters' not in ref_data:
                        all_refs_detailed = False
                        break
                elif ref_data.get('type') == 'single':
                    if 'original_value' not in ref_data:
                        all_refs_detailed = False
                        break
    
    if all_refs_detailed:
        requirements_met.append("✅ All extracted references tracked with field names and order")
    else:
        requirements_failed.append("❌ Some references missing detailed tracking")
    
    # Requirement 2: STIX ID → filename mapping exists for all objects
    all_objects_mapped = len(id_mapping) == metadata.get('total_objects', 0)
    if all_objects_mapped:
        requirements_met.append("✅ Complete STIX ID → filename mapping")
    else:
        requirements_failed.append("❌ Incomplete STIX ID → filename mapping")
    
    # Requirement 3: Dependency sequencing exists
    sequence_exists = len(creation_sequence) > 0
    if sequence_exists:
        requirements_met.append("✅ Creation sequence generated for dependency management")
    else:
        requirements_failed.append("❌ No creation sequence found")
    
    # Requirement 4: Data form paths included
    paths_included = all('data_form_path' in entry for entry in detailed_refs)
    if paths_included:
        requirements_met.append("✅ Data form file paths included")
    else:
        requirements_failed.append("❌ Missing data form file paths")
    
    print("\n🎯 REQUIREMENTS STATUS:")
    for req in requirements_met:
        print(f"  {req}")
    for req in requirements_failed:
        print(f"  {req}")
    
    success_rate = len(requirements_met) / (len(requirements_met) + len(requirements_failed)) * 100
    print(f"\n📈 Overall Requirements Satisfaction: {success_rate:.1f}%")
    
    return success_rate >= 100.0


def test_reconstitution_capability():
    """
    Main test function for reconstitution capability
    """
    
    print("🧪 TESTING RECONSTITUTION CAPABILITY\n")
    print("=" * 60)
    
    # Import the required functions
    from convert_object_list_to_data_forms import discover_class_templates
    
    # Discover available templates first
    print("🔍 Discovering available class templates...")
    
    # Set up paths same as the main function
    base_path = Path.cwd()
    if base_path.name == "temp_method_comparison":
        base_path = base_path.parent
    if base_path.name == "Orchestration":
        base_path = base_path.parent
    
    stixorm_path = base_path / "Block_Families" / "StixORM"
    print(f"   StixORM path: {stixorm_path}")
    
    if not stixorm_path.exists():
        print("❌ StixORM directory not found!")
        print(f"   Expected path: {stixorm_path}")
        print(f"   Current working directory: {Path.cwd()}")
        return False
    
    # Discover templates
    available_templates = discover_class_templates(stixorm_path)
    print(f"   Found {len(available_templates)} templates: {list(available_templates.keys())}")
    
    if not available_templates:
        print("❌ No templates discovered! Cannot proceed with test.")
        return False
    
    # Create test dataset using only available templates
    print("\n📋 Creating test dataset with available templates...")
    test_objects = create_complex_test_dataset(available_templates)
    
    if not test_objects:
        print("❌ No test objects could be created with available templates!")
        return False
    
    # Create test directory
    test_dir = Path("reconstitution_test_output")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(exist_ok=True)
    
    # Test the enhanced function in Mode 2
    print("\n🔧 Running enhanced create_data_forms_from_stix_objects in Mode 2...")
    try:
        result = create_data_forms_from_stix_objects(
            stix_objects=test_objects,
            test_directory=str(test_dir)
        )
        
        print("✅ Function executed successfully")
        
        # Verify basic results
        report = result.get('report', {})
        print(f"\n📊 Processing Report:")
        print(f"   Total Objects: {report.get('total_objects', 0)}")
        print(f"   Successful: {report.get('successful', 0)}")
        print(f"   Failed: {report.get('failed', 0)}")
        print(f"   Success Rate: {report.get('success_rate', 0):.1f}%")
        
        if report.get('failed', 0) > 0:
            print(f"   Errors: {report.get('errors', [])}")
        
        created_files = result.get('created_files', [])
        print(f"\n📁 Created Files: {len(created_files)}")
        
        # Check for reconstitution data files
        reconstitution_file = test_dir / "reconstitution_data.json"
        sequence_file = test_dir / "creation_sequence.json"
        
        if reconstitution_file.exists():
            print("✅ Reconstitution data file created")
        else:
            print("❌ Missing reconstitution data file")
            return False
        
        if sequence_file.exists():
            print("✅ Creation sequence file created")
        else:
            print("❌ Missing creation sequence file") 
            return False
        
        # Analyze the reconstitution data
        print(f"\n" + "=" * 60)
        success = analyze_reconstitution_data(reconstitution_file)
        
        # Additional validation - check creation sequence file
        print(f"\n" + "=" * 60)
        print("=== CREATION SEQUENCE VALIDATION ===\n")
        
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence = json.load(f)
        
        print(f"📋 Sequence entries: {len(sequence)}")
        
        if sequence:
            print("\n🔄 First 3 sequence entries:")
            for i, entry in enumerate(sequence[:3]):
                deps = entry.get('dependencies', [])
                print(f"  {entry.get('sequence_order')}. {entry.get('object_type')} "
                      f"({len(deps)} dependencies)")
                if deps:
                    print(f"     Depends on: {deps[:2]}{'...' if len(deps) > 2 else ''}")
        
        print(f"\n🎯 RECONSTITUTION CAPABILITY TEST: {'✅ PASSED' if success else '❌ FAILED'}")
        return success
        
    except Exception as e:
        print(f"❌ Function execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_reconstitution_capability()
    if success:
        print(f"\n🎉 All tests passed! Reconstitution capability is fully functional.")
    else:
        print(f"\n💥 Tests failed! Reconstitution capability needs improvement.")
    
    exit(0 if success else 1)