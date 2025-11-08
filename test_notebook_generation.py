#!/usr/bin/env python3
"""
Test notebook generation with real STIX objects from examples directory.
This will generate a notebook that creates objects and saves to unattached context.
"""

import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Orchestration.Utilities.reconstitute_and_generate_notebooks import reconstitute_and_generate


def load_example_objects(max_objects=10):
    """Load a sample of STIX objects from the examples directory"""
    examples_dir = Path('Block_Families/examples')
    objects = []
    
    # Load a variety of object types
    example_files = [
        'aaa_indicator.json',
        'campaign.json',
        'identity.json',
        'locations.json',
        'note.json',
    ]
    
    for filename in example_files:
        file_path = examples_dir / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle different file structures
                    if isinstance(data, dict):
                        if 'objects' in data:
                            # Bundle format
                            for obj in data['objects']:
                                if len(objects) < max_objects:
                                    objects.append(obj)
                        elif 'type' in data:
                            # Single object
                            if len(objects) < max_objects:
                                objects.append(data)
                    elif isinstance(data, list):
                        # Array of objects
                        for obj in data:
                            if isinstance(obj, dict) and 'type' in obj and len(objects) < max_objects:
                                objects.append(obj)
                                
                if len(objects) >= max_objects:
                    break
                    
            except Exception as e:
                print(f"⚠️  Error loading {filename}: {e}")
    
    return objects


def main():
    """Generate and test notebook creation"""
    print("=" * 70)
    print("NOTEBOOK GENERATION TEST - Unattached Context")
    print("=" * 70)
    
    # Step 1: Load example objects
    print("\n📂 Step 1: Loading example STIX objects...")
    objects = load_example_objects(max_objects=10)
    
    if not objects:
        print("❌ No objects loaded!")
        return False
    
    print(f"✅ Loaded {len(objects)} STIX objects")
    
    # Show what we loaded
    type_counts = {}
    for obj in objects:
        obj_type = obj.get('type', 'unknown')
        type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
    
    print(f"\n📊 Object types:")
    for obj_type, count in sorted(type_counts.items()):
        print(f"   - {obj_type}: {count}")
    
    # Step 2: Generate notebook
    print(f"\n📓 Step 2: Generating notebook...")
    
    results = reconstitute_and_generate(
        mode='notebook',
        stix_objects=objects,
        notebook_name='Test_Unattached_Context',
        context_type='unattached',
        notebook_title='Test: Create Objects in Unattached Context',
        notebook_description=(
            'Auto-generated test notebook that creates STIX objects from data forms '
            'and saves them to unattached context memory.'
        )
    )
    
    # Step 3: Check results
    print(f"\n🔍 Step 3: Checking results...")
    
    if not results['success']:
        print("❌ Notebook generation failed!")
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   {error}")
        return False
    
    print(f"✅ Notebook generation successful!")
    print(f"\n📊 Results:")
    print(f"   - Notebook path: {results.get('notebook_path')}")
    print(f"   - Data forms created: {results.get('data_forms_created')}")
    print(f"   - Generated files: {len(results.get('generated_files', []))}")
    
    # Step 4: Verify notebook exists
    notebook_path = Path(results['notebook_path'])
    if notebook_path.exists():
        print(f"\n✅ Notebook file verified: {notebook_path}")
        file_size = notebook_path.stat().st_size
        print(f"   - File size: {file_size:,} bytes")
        
        # Load and show notebook structure
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        cell_count = len(notebook.get('cells', []))
        print(f"   - Cell count: {cell_count}")
        
        # Count cell types
        markdown_cells = sum(1 for c in notebook['cells'] if c['cell_type'] == 'markdown')
        code_cells = sum(1 for c in notebook['cells'] if c['cell_type'] == 'code')
        print(f"   - Markdown cells: {markdown_cells}")
        print(f"   - Code cells: {code_cells}")
        
    else:
        print(f"❌ Notebook file not found: {notebook_path}")
        return False
    
    # Step 5: Check data forms were created
    print(f"\n📁 Step 4: Verifying data forms...")
    
    stixorm_dir = Path('Block_Families/StixORM')
    data_forms = list(stixorm_dir.rglob('*_data_form.json'))
    
    print(f"✅ Found {len(data_forms)} data form files")
    
    if data_forms:
        print(f"\n📋 Sample data forms:")
        for df in data_forms[:5]:  # Show first 5
            relative_path = df.relative_to(stixorm_dir)
            print(f"   - {relative_path}")
        if len(data_forms) > 5:
            print(f"   ... and {len(data_forms) - 5} more")
    
    # Success summary
    print(f"\n" + "=" * 70)
    print("✅ TEST PASSED!")
    print("=" * 70)
    print(f"\n📓 Generated notebook: {notebook_path}")
    print(f"📊 Objects processed: {len(objects)}")
    print(f"📁 Data forms created: {results.get('data_forms_created')}")
    print(f"\n💡 Next steps:")
    print(f"   1. Open the notebook: {notebook_path}")
    print(f"   2. Execute the cells to create objects in unattached context")
    print(f"   3. Verify objects are saved to context memory")
    
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
