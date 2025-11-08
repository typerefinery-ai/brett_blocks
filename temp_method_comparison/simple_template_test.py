#!/usr/bin/env python3
"""
Simple Template Discovery Test
"""

import json
import sys
from pathlib import Path

# Add utilities to path
sys.path.append(str(Path(__file__).parent.parent / "Orchestration" / "Utilities"))
from convert_object_list_to_data_forms import discover_class_templates, create_data_forms_from_stix_objects

def test_template_discovery():
    """Test template discovery and simple conversion"""
    
    print("🔍 Testing template discovery...")
    
    # Set up paths
    base_path = Path.cwd()
    if base_path.name == "temp_method_comparison":
        base_path = base_path.parent
    if base_path.name == "Orchestration":
        base_path = base_path.parent
    
    stixorm_path = base_path / "Block_Families" / "StixORM"
    print(f"StixORM path: {stixorm_path}")
    
    # Discover templates
    available_templates = discover_class_templates(stixorm_path)
    print(f"\nFound {len(available_templates)} templates:")
    
    for stix_type, template_info in list(available_templates.items())[:10]:  # Show first 10
        print(f"  {stix_type}: {template_info['template_path']}")
    
    if 'identity' in available_templates:
        print(f"\n✅ Identity template found: {available_templates['identity']['template_path']}")
        
        # Debug: Print the template structure
        identity_template = available_templates['identity']
        print(f"\n🔍 Debug - Template structure:")
        print(f"   class_name: {identity_template.get('class_name')}")
        print(f"   category: {identity_template.get('category')}")
        print(f"   directory: {identity_template.get('directory')}")
        
        # Check template_data structure
        template_data = identity_template.get('template_data', {})
        print(f"   template_data keys: {list(template_data.keys())}")
        
        if 'Identity_template' in template_data:
            inner_template = template_data['Identity_template']
            print(f"   Identity_template keys: {list(inner_template.keys())}")
            print(f"   _type: {inner_template.get('_type')}")
        
        # Test with a simple identity object
        test_objects = [{
            "type": "identity",
            "spec_version": "2.1",
            "id": "identity--test-1111-1111-1111-111111111111",
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Test Identity",
            "identity_class": "organization"
        }]
        
        print(f"\n🧪 Testing conversion with identity object...")
        
        # Add debugging - check what the main function is doing with paths
        print(f"\n🔍 Debug - Path detection in main function:")
        
        # Simulate the main function's path logic
        main_base_path = Path.cwd()
        print(f"   Original cwd: {main_base_path}")
        print(f"   cwd.name: {main_base_path.name}")
        
        if main_base_path.name == "Orchestration":
            main_base_path = main_base_path.parent
            print(f"   Adjusted to parent: {main_base_path}")
        
        main_stixorm_path = main_base_path / "Block_Families" / "StixORM"
        print(f"   Main function stixorm_path: {main_stixorm_path}")
        print(f"   Main stixorm path exists: {main_stixorm_path.exists()}")
        
        if main_stixorm_path != stixorm_path:
            print(f"   ❌ PATH MISMATCH! Main function using wrong path")
            print(f"     Discovery used: {stixorm_path}")
            print(f"     Main func using: {main_stixorm_path}")
        else:
            print(f"   ✅ Paths match")
        
        # Create test directory
        test_dir = Path("simple_test_output")
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
        test_dir.mkdir(exist_ok=True)
        
        # Test conversion
        try:
            result = create_data_forms_from_stix_objects(
                stix_objects=test_objects,
                test_directory=str(test_dir)
            )
            
            print(f"✅ Conversion successful!")
            print(f"   Total objects: {result['report']['total_objects']}")
            print(f"   Successful: {result['report']['successful']}")
            print(f"   Failed: {result['report']['failed']}")
            
            if result['report']['failed'] > 0:
                print(f"   Errors: {result['report']['errors']}")
            
            if result['report']['successful'] > 0:
                print(f"   Created files: {len(result['created_files'])}")
                for file_info in result['created_files']:
                    print(f"     - {file_info['filename']}")
                    
                print(f"   Reference tracking entries: {len(result.get('extracted_references', []))}")
                
                # Check for reconstitution data
                recon_file = test_dir / "reconstitution_data.json"
                if recon_file.exists():
                    print(f"✅ Reconstitution data file created")
                    with open(recon_file, 'r', encoding='utf-8') as f:
                        recon_data = json.load(f)
                    print(f"   Metadata: {recon_data.get('metadata', {})}")
                else:
                    print(f"❌ Reconstitution data file missing")
        
        except Exception as e:
            print(f"❌ Conversion failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print(f"\n❌ Identity template not found!")
        print(f"Available types: {list(available_templates.keys())[:20]}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_template_discovery()
    exit(0 if success else 1)