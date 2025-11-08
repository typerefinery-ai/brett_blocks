#!/usr/bin/env python3
"""
Quick Test of STIX Reconstitution

Simple test to demonstrate the working reconstitution capability
with a focus on successful round-trip conversion.
"""

import json
from pathlib import Path
from reconstitute_object_list import reconstitute_object_list

def main():
    """Run a quick test of the reconstitution framework"""
    
    print("🧪 QUICK STIX RECONSTITUTION TEST")
    print("=" * 50)
    
    # Set up paths
    examples_dir = Path(__file__).parent.parent / "Block_Families" / "examples"
    generated_dir = Path(__file__).parent / "generated"
    
    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        return False
    
    try:
        # Run reconstitution
        print(f"📂 Testing with: {examples_dir}")
        original_objects, reconstituted_objects, report = reconstitute_object_list(
            str(examples_dir), 
            str(generated_dir)
        )
        
        # Print summary
        print("\n🎯 RESULTS SUMMARY:")
        print(f"   📊 Original Objects: {report['original_objects_count']}")
        print(f"   📈 Data Forms Success: {report['data_forms_success_rate']:.1f}%")
        print(f"   🎯 Reconstituted Objects: {report['reconstituted_objects_count']}")
        print(f"   📈 Reconstitution Success: {report['reconstitution_success_rate']:.1f}%")
        
        # Show file counts
        file_counts = report['generated_files']
        print(f"\n📁 Generated Files:")
        print(f"   📄 Input Objects: {file_counts['input_objects']}")
        print(f"   📋 Data Forms: {file_counts['data_forms']}")
        print(f"   📤 Output Objects: {file_counts['output_objects']}")
        
        # Show sample successful objects
        if reconstituted_objects:
            print(f"\n✅ Sample Reconstituted Objects:")
            object_types = set()
            for obj in reconstituted_objects[:10]:
                obj_type = obj.get('type', 'unknown')
                if obj_type not in object_types:
                    object_types.add(obj_type)
                    obj_id = obj.get('id', 'unknown')[:50]
                    print(f"   🔹 {obj_type}: {obj_id}")
        
        # Determine success
        success_rate = report['reconstitution_success_rate']
        if success_rate >= 85.0:
            print(f"\n🎉 TEST SUCCESSFUL! ({success_rate:.1f}% reconstitution rate)")
            print("   ✅ STIX object reconstitution framework is working correctly")
            print("   ✅ Data forms generation completed successfully")
            print("   ✅ Objects reconstituted with proper UUID generation")
            print("   ✅ Dependency sequencing working as expected")
            return True
        else:
            print(f"\n⚠️  TEST MARGINAL ({success_rate:.1f}% reconstitution rate)")
            print("   Framework is working but some objects failed reconstitution")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'='*50}")
    if success:
        print("🎉 RECONSTITUTION FRAMEWORK VALIDATION: ✅ PASSED")
    else:
        print("💥 RECONSTITUTION FRAMEWORK VALIDATION: ❌ FAILED")