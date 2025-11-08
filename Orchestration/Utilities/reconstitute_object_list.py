#!/usr/bin/env python3
"""
STIX Object Reconstitution Module

This module handles the complete round-trip conversion process:
1. Load STIX objects from input directories
2. Convert to data forms using create_data_forms_from_stix_objects
3. Reconstitute STIX objects from data forms and reconstitution data
4. Handle dependency sequencing and reference restoration

The reconstituted objects should be identical to the originals except for UUIDs.
"""

import json
import uuid
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import sys

# Import from the same directory
from .convert_object_list_to_data_forms import create_data_forms_from_stix_objects


class STIXReconstitutionEngine:
    """Engine for reconstituting STIX objects from data forms"""
    
    def __init__(self, generated_dir: Path):
        """Initialize with the generated directory path"""
        self.generated_dir = Path(generated_dir)
        self.input_dir = self.generated_dir / "input_objects"
        self.data_forms_dir = self.generated_dir / "data_forms"
        self.output_dir = self.generated_dir / "output_objects"
        
        # Ensure directories exist
        for dir_path in [self.input_dir, self.data_forms_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_truncated_id(self, stix_id: str) -> str:
        """
        Get truncated ID from a STIX ID for consistent file naming.
        Example: 'identity--ce31dd38-f69b-45ba-9bcd-2a208bbf8017' -> 'ce31dd38'
        """
        if '--' in stix_id:
            uuid_part = stix_id.split('--')[1]
            return uuid_part[:8]
        return stix_id[:8]
    
    def clear_generated_directories(self):
        """Clear all generated subdirectories"""
        print("🧹 Clearing generated directories...")
        
        for dir_path in [self.input_dir, self.data_forms_dir, self.output_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print("   ✅ All generated directories cleared")
    
    def load_stix_objects_from_directory(self, input_directory: Path) -> List[Dict[str, Any]]:
        """
        Load all STIX objects from input directory and subdirectories.
        Copy them to input_objects directory for later comparison.
        """
        print(f"📂 Loading STIX objects from: {input_directory}")
        
        stix_objects = []
        copied_files = 0
        
        # Recursively find all JSON files
        for json_file in input_directory.rglob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle both single objects and lists of objects
                if isinstance(data, list):
                    for obj in data:
                        if isinstance(obj, dict) and 'type' in obj and 'id' in obj:
                            stix_objects.append(obj)
                            
                            # Copy to input_objects directory with truncated ID
                            truncated_id = self.get_truncated_id(obj['id'])
                            copy_filename = f"{obj['type']}_{truncated_id}.json"
                            copy_path = self.input_dir / copy_filename
                            
                            with open(copy_path, 'w', encoding='utf-8') as cf:
                                json.dump(obj, cf, indent=2, ensure_ascii=False)
                            copied_files += 1
                            
                elif isinstance(data, dict) and 'type' in data and 'id' in data:
                    stix_objects.append(data)
                    
                    # Copy to input_objects directory with truncated ID
                    truncated_id = self.get_truncated_id(data['id'])
                    copy_filename = f"{data['type']}_{truncated_id}.json"
                    copy_path = self.input_dir / copy_filename
                    
                    with open(copy_path, 'w', encoding='utf-8') as cf:
                        json.dump(data, cf, indent=2, ensure_ascii=False)
                    copied_files += 1
                    
            except Exception as e:
                print(f"   ⚠️  Could not load {json_file}: {e}")
        
        print(f"   ✅ Loaded {len(stix_objects)} STIX objects")
        print(f"   📋 Copied {copied_files} objects to input_objects directory")
        
        return stix_objects
    
    def generate_data_forms(self, stix_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate data forms from STIX objects using Mode 2"""
        print(f"🔄 Generating data forms for {len(stix_objects)} objects...")
        
        try:
            result = create_data_forms_from_stix_objects(
                stix_objects=stix_objects,
                test_directory=str(self.data_forms_dir)
            )
            
            report = result.get('report', {})
            print(f"   ✅ Data forms generation completed")
            print(f"   📊 Success rate: {report.get('success_rate', 0):.1f}%")
            print(f"   📁 Created {len(result.get('created_files', []))} data form files")
            print(f"   🔗 Reference tracking entries: {len(result.get('extracted_references', []))}")
            
            if report.get('failed', 0) > 0:
                print(f"   ❌ Failed objects: {report.get('failed', 0)}")
                for error in report.get('errors', [])[:3]:  # Show first 3 errors
                    print(f"      - {error.get('object_id', 'unknown')}: {error.get('error', 'unknown error')}")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Data forms generation failed: {str(e)}")
            raise
    
    def load_reconstitution_data(self) -> Dict[str, Any]:
        """Load the reconstitution data generated by the data forms function"""
        recon_file = self.data_forms_dir / "reconstitution_data.json"
        
        if not recon_file.exists():
            raise FileNotFoundError(f"Reconstitution data file not found: {recon_file}")
        
        with open(recon_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_new_uuid(self, original_id: str, id_mapping: Dict[str, str]) -> str:
        """Generate a new UUID while preserving type prefix"""
        if original_id in id_mapping:
            return id_mapping[original_id]
        
        # Extract type prefix
        if '--' in original_id:
            type_prefix = original_id.split('--')[0]
            new_uuid = str(uuid.uuid4())
            new_id = f"{type_prefix}--{new_uuid}"
        else:
            new_id = str(uuid.uuid4())
        
        id_mapping[original_id] = new_id
        return new_id
    
    def load_referenced_objects(self, reference_info: Dict[str, Any], 
                                  reconstituted_objects_lookup: Dict[str, Dict[str, Any]],
                                  id_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Load referenced objects for multi-input block processing.
        
        Returns a dict keyed by reference field name, where each value is the 
        reconstituted STIX object that was referenced.
        
        This implements Step 1: Load referenced objects based on the dependency graph
        """
        if not reference_info.get('has_references', False):
            return {}
        
        extracted_refs = reference_info.get('extracted_references', {})
        referenced_objects = {}
        
        for field_path, ref_data in extracted_refs.items():
            # Skip the 'id' field - that's a self-reference, not an embedded reference
            if field_path == 'id':
                continue
            
            if ref_data.get('type') == 'single':
                # Load the single referenced object
                original_ref_id = ref_data.get('original_value')
                if original_ref_id and original_ref_id in reconstituted_objects_lookup:
                    referenced_objects[field_path] = reconstituted_objects_lookup[original_ref_id]
                    
            elif ref_data.get('type') == 'list':
                # Load multiple referenced objects (preserve order)
                original_ref_ids = ref_data.get('original_values', [])
                ref_objects = []
                for original_ref_id in original_ref_ids:
                    if original_ref_id in reconstituted_objects_lookup:
                        ref_objects.append(reconstituted_objects_lookup[original_ref_id])
                if ref_objects:
                    referenced_objects[field_path] = ref_objects
        
        return referenced_objects
    
    def restore_references_to_data_form(self, data_form: Dict[str, Any], 
                                      reference_info: Dict[str, Any], 
                                      id_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Restore references to a data form using the reference tracking information.
        
        This implements Step 3: Restore the reference fields that were extracted.
        It replaces empty strings/arrays with the new UUIDs from id_mapping.
        
        CRITICAL: This looks up existing mappings, does NOT generate new ones.
        Referenced objects must have been processed first (dependency ordering).
        """
        
        if not reference_info.get('has_references', False):
            return data_form
        
        extracted_refs = reference_info.get('extracted_references', {})
        
        # Create a deep copy to avoid modifying the original
        import copy
        restored_form = copy.deepcopy(data_form)
        
        # Get the actual form data (unwrap the form_name if present)
        form_name = list(restored_form.keys())[0] if isinstance(restored_form, dict) and len(restored_form) == 1 else None
        if form_name and isinstance(restored_form.get(form_name), dict):
            form_data = restored_form[form_name]
        else:
            form_data = restored_form
        
        # Helper to get new UUID from mapping (don't generate if missing)
        def get_mapped_uuid(original_ref: str) -> str:
            # DEBUG logging for sequence references
            if original_ref.startswith('sequence--'):
                print(f"         [DEBUG] Mapping {original_ref}: {'FOUND' if original_ref in id_mapping else 'NOT FOUND'}")
                if original_ref in id_mapping:
                    print(f"         [DEBUG] → {id_mapping[original_ref]}")
            
            if original_ref in id_mapping:
                return id_mapping[original_ref]
            else:
                # Reference not yet mapped - generate it now
                # This can happen for forward references or optional deps
                print(f"         [WARNING] Reference {original_ref} not in mapping, generating new UUID")
                return self.generate_new_uuid(original_ref, id_mapping)
        
        for field_path, ref_data in extracted_refs.items():
            # Skip the 'id' field - that's handled separately
            if field_path == 'id':
                continue
            
            # Navigate to the correct location in the data form
            # The field_path can be simple ("provided_by_ref") or complex ("extensions.ext-id.field")
            path_parts = field_path.split('.')
            final_field = path_parts[-1] if path_parts else field_path
            
            # Check if this is an extension field path
            if field_path.startswith('extensions.'):
                # Handle extension fields by navigating the full path
                current_obj = form_data
                try:
                    for i, part in enumerate(path_parts[:-1]):
                        if '[' in part and ']' in part:
                            # Handle array indexing like "email_addresses[0]"
                            array_name, index_str = part.split('[')
                            index = int(index_str.rstrip(']'))
                            if array_name in current_obj:
                                current_obj = current_obj[array_name][index]
                        else:
                            if part in current_obj:
                                current_obj = current_obj[part]
                    
                    # Now restore the reference at the final location
                    if ref_data.get('type') == 'list':
                        original_values = ref_data.get('original_values', [])
                        new_values = [get_mapped_uuid(ref) for ref in original_values]
                        current_obj[final_field] = new_values
                    elif ref_data.get('type') == 'single':
                        original_value = ref_data.get('original_value')
                        if original_value:
                            new_value = get_mapped_uuid(original_value)
                            current_obj[final_field] = new_value
                except (KeyError, IndexError, TypeError) as e:
                    # Path navigation failed
                    if field_path.startswith('extensions.'):
                        print(f"         [WARNING] Failed to navigate extension path: {field_path}")
                        print(f"         [WARNING] Error: {type(e).__name__}: {e}")
                continue  # Skip to next field
            
            # For non-extension fields, search in all sections of the form (base_required, base_optional, object, sub)
            found = False
            for section in ['base_required', 'base_optional', 'object', 'sub']:
                if section in form_data and final_field in form_data[section]:
                    if ref_data.get('type') == 'list':
                        # Restore list of references with new UUIDs
                        original_values = ref_data.get('original_values', [])
                        new_values = [get_mapped_uuid(ref) for ref in original_values]
                        form_data[section][final_field] = new_values
                        found = True
                        break
                        
                    elif ref_data.get('type') == 'single':
                        # Restore single reference with new UUID
                        original_value = ref_data.get('original_value')
                        if original_value:
                            new_value = get_mapped_uuid(original_value)
                            form_data[section][final_field] = new_value
                            found = True
                            break
            
            # Special handling for 'sub' section with embedded references in arrays
            if not found and 'sub' in form_data:
                # Try to find the reference in sub section arrays
                # e.g., email_addresses[0].email_address_ref
                for array_name, array_data in form_data['sub'].items():
                    if isinstance(array_data, list):
                        for item in array_data:
                            if isinstance(item, dict) and final_field in item:
                                if ref_data.get('type') == 'single':
                                    original_value = ref_data.get('original_value')
                                    if original_value:
                                        new_value = get_mapped_uuid(original_value)
                                        item[final_field] = new_value
                                        found = True
                                        break
                        if found:
                            break
            
            if not found:
                # Handle complex paths for extension fields and nested structures
                # Navigate through the path_parts to find the target location
                current_obj = form_data
                try:
                    for i, part in enumerate(path_parts[:-1]):
                        if '[' in part and ']' in part:
                            # Handle array indexing like "email_addresses[0]"
                            array_name, index_str = part.split('[')
                            index = int(index_str.rstrip(']'))
                            if array_name in current_obj:
                                current_obj = current_obj[array_name][index]
                        else:
                            if part in current_obj:
                                current_obj = current_obj[part]
                    
                    # Now restore the reference at the final location
                    if ref_data.get('type') == 'list':
                        original_values = ref_data.get('original_values', [])
                        new_values = [get_mapped_uuid(ref) for ref in original_values]
                        current_obj[final_field] = new_values
                    elif ref_data.get('type') == 'single':
                        original_value = ref_data.get('original_value')
                        if original_value:
                            new_value = get_mapped_uuid(original_value)
                            current_obj[final_field] = new_value
                except (KeyError, IndexError, TypeError) as e:
                    # Path navigation failed - field might not exist in this data form
                    # This can happen for optional fields that weren't in the original
                    if field_path.startswith('extensions.'):
                        print(f"         [WARNING] Failed to navigate path: {field_path}")
                        print(f"         [WARNING] Error: {type(e).__name__}: {e}")
                    pass
        
        return restored_form
    
    def create_stix_object_from_data_form(self, data_form: Dict[str, Any], 
                                        form_name: str, 
                                        new_object_id: str) -> Dict[str, Any]:
        """Create a STIX object from a data form"""
        
        stix_obj = {}
        
        # Extract the actual form data (skip the form_name wrapper if present)
        if form_name in data_form:
            form_data = data_form[form_name]
        else:
            form_data = data_form
        
        # Process base_required fields
        if 'base_required' in form_data:
            for field, value in form_data['base_required'].items():
                if field == 'id':
                    stix_obj[field] = new_object_id
                elif field in ['created', 'modified'] and (not value or value == ""):
                    # Generate new timestamps for auto-generated fields
                    from datetime import datetime
                    stix_obj[field] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                else:
                    stix_obj[field] = value
        
        # Process base_optional fields (exclude None values)
        if 'base_optional' in form_data:
            for field, value in form_data['base_optional'].items():
                if value is not None and value != "" and value != []:
                    stix_obj[field] = value
        
        # Process object fields
        if 'object' in form_data:
            for field, value in form_data['object'].items():
                if value is not None and value != "" and value != []:
                    stix_obj[field] = value
        
        # Process extensions
        if 'extensions' in form_data and form_data['extensions']:
            stix_obj['extensions'] = {}
            for ext_id, ext_data in form_data['extensions'].items():
                if ext_data:  # Only include non-empty extensions
                    stix_obj['extensions'][ext_id] = ext_data
        
        # Process sub-objects (embedded objects)
        if 'sub' in form_data and form_data['sub']:
            # Sub-objects get merged directly into extensions or appropriate locations
            for key, sub_data in form_data['sub'].items():
                if sub_data:
                    # If we have extensions, try to add to the appropriate extension
                    if 'extensions' in stix_obj:
                        for ext_id, ext_data in stix_obj['extensions'].items():
                            if key in ext_data or isinstance(ext_data, dict):
                                ext_data[key] = sub_data
                                break
                    else:
                        # Otherwise add directly to the object
                        stix_obj[key] = sub_data
        
        return stix_obj
    
    def reconstitute_stix_objects(self, recon_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reconstitute STIX objects from data forms using reconstitution data.
        
        Implements the multi-input block pattern:
        1. Load referenced objects for each object based on dependency graph
        2. Pass multiple inputs to blocks (data form + referenced objects keyed by field name)
        3. Restore reference fields that were extracted during data form generation
        """
        print("🔄 Reconstituting STIX objects from data forms...")
        
        creation_sequence = recon_data.get('creation_sequence', [])
        detailed_refs = recon_data.get('detailed_reference_extraction', [])
        id_to_form_mapping = recon_data.get('id_to_form_name_mapping', {})
        
        # Create lookup for reference information by object ID
        ref_lookup = {item['object_id']: item for item in detailed_refs}
        
        reconstituted_objects = []
        reconstituted_objects_lookup = {}  # Maps original ID to reconstituted object
        id_mapping = {}  # Maps old IDs to new IDs
        
        print(f"   📋 Processing {len(creation_sequence)} objects in dependency order")
        
        for seq_entry in creation_sequence:
            try:
                obj_id = seq_entry['object_id']
                filename = seq_entry['filename']
                form_name = seq_entry['form_name']
                
                # Load the data form
                form_file = self.data_forms_dir / filename
                if not form_file.exists():
                    print(f"   ⚠️  Data form file not found: {filename}")
                    continue
                
                with open(form_file, 'r', encoding='utf-8') as f:
                    data_form = json.load(f)
                
                # Generate new object ID
                new_obj_id = self.generate_new_uuid(obj_id, id_mapping)
                
                # DEBUG: Log ID mapping for sequence objects
                if obj_id.startswith('sequence--'):
                    print(f"      [DEBUG] Processing {obj_id}")
                    print(f"      [DEBUG] New UUID: {new_obj_id}")
                    print(f"      [DEBUG] Current id_mapping has {len(id_mapping)} entries")
                
                # Get reference information for this object
                ref_info = ref_lookup.get(obj_id, {})
                
                # Step 1: Load referenced objects based on dependency graph
                # This creates the multi-input structure that Python blocks expect
                referenced_objects = self.load_referenced_objects(
                    ref_info, 
                    reconstituted_objects_lookup, 
                    id_mapping
                )
                
                # Step 2: Multi-input block pattern (conceptual for now)
                # In actual block execution, we would pass:
                # {
                #     "data_form": data_form,
                #     "provided_by_ref": <identity_object>,  # if this field exists
                #     "email_address_ref": <email_object>,   # if this field exists
                #     # ... etc for all embedded reference fields
                # }
                # 
                # For now, we're doing direct reconstitution, but the referenced_objects
                # dict is structured exactly as blocks would receive it.
                
                # Step 3: Restore references with new UUIDs
                restored_form = self.restore_references_to_data_form(data_form, ref_info, id_mapping)
                
                # Create STIX object from data form
                stix_obj = self.create_stix_object_from_data_form(restored_form, form_name, new_obj_id)
                
                # Store in lookup for dependent objects (keyed by ORIGINAL ID)
                reconstituted_objects_lookup[obj_id] = stix_obj
                reconstituted_objects.append(stix_obj)
                
                # Save individual reconstituted object with truncated ID
                truncated_id = self.get_truncated_id(new_obj_id)
                obj_filename = f"{stix_obj['type']}_{truncated_id}_reconstituted.json"
                obj_path = self.output_dir / obj_filename
                
                with open(obj_path, 'w', encoding='utf-8') as f:
                    json.dump(stix_obj, f, indent=2, ensure_ascii=False)
                
                print(f"   ✅ Reconstituted: {stix_obj['type']} -> {obj_filename}")
                
            except Exception as e:
                print(f"   ❌ Failed to reconstitute {obj_id}: {str(e)}")
                continue
        
        print(f"   🎯 Successfully reconstituted {len(reconstituted_objects)} objects")
        
        # Save all reconstituted objects as a single file
        all_objects_path = self.output_dir / "all_reconstituted_objects.json"
        with open(all_objects_path, 'w', encoding='utf-8') as f:
            json.dump(reconstituted_objects, f, indent=2, ensure_ascii=False)
        
        return reconstituted_objects
    
    def run_full_reconstitution(self, input_directory: Path) -> Tuple[List[Dict], List[Dict], Dict]:
        """
        Run the complete reconstitution process:
        1. Load STIX objects
        2. Generate data forms
        3. Reconstitute objects
        
        Returns: (original_objects, reconstituted_objects, reconstitution_report)
        """
        print("🚀 Starting full reconstitution process...\n")
        
        try:
            # Step 1: Clear directories
            self.clear_generated_directories()
            
            # Step 2: Load STIX objects
            original_objects = self.load_stix_objects_from_directory(input_directory)
            if not original_objects:
                raise ValueError("No STIX objects found in input directory")
            
            # Step 3: Generate data forms
            data_forms_result = self.generate_data_forms(original_objects)
            
            # Step 4: Load reconstitution data
            recon_data = self.load_reconstitution_data()
            
            # Step 5: Reconstitute objects
            reconstituted_objects = self.reconstitute_stix_objects(recon_data)
            
            # Create summary report
            report = {
                'input_directory': str(input_directory),
                'original_objects_count': len(original_objects),
                'data_forms_success_rate': data_forms_result['report'].get('success_rate', 0),
                'reconstituted_objects_count': len(reconstituted_objects),
                'reconstitution_success_rate': (len(reconstituted_objects) / len(original_objects) * 100) if original_objects else 0,
                'generated_files': {
                    'input_objects': len(list(self.input_dir.glob('*.json'))),
                    'data_forms': len(list(self.data_forms_dir.glob('*_data_form.json'))),
                    'output_objects': len(list(self.output_dir.glob('*.json')))
                }
            }
            # Include the raw reconstitution metadata to help downstream matching
            try:
                report['reconstitution_data'] = recon_data
            except Exception:
                report['reconstitution_data'] = {}
            
            print(f"\n🎉 Reconstitution process completed!")
            print(f"   📊 Original objects: {report['original_objects_count']}")
            print(f"   📈 Data forms success: {report['data_forms_success_rate']:.1f}%")
            print(f"   🎯 Reconstituted objects: {report['reconstituted_objects_count']}")
            print(f"   📈 Reconstitution success: {report['reconstitution_success_rate']:.1f}%")
            
            return original_objects, reconstituted_objects, report
            
        except Exception as e:
            print(f"\n❌ Reconstitution process failed: {str(e)}")
            raise


def reconstitute_object_list(input_directory: str, generated_directory: str) -> Tuple[List[Dict], List[Dict], Dict]:
    """
    Main function to reconstitute STIX objects from an input directory.
    
    Args:
        input_directory: Path to directory containing STIX objects
        generated_directory: Path to directory for generated files
        
    Returns:
        Tuple of (original_objects, reconstituted_objects, report)
    """
    
    engine = STIXReconstitutionEngine(generated_directory)
    return engine.run_full_reconstitution(Path(input_directory))


if __name__ == "__main__":
    """Test the reconstitution module"""
    
    # Test with examples directory
    input_dir = Path(__file__).parent.parent / "Block_Families" / "examples"
    generated_dir = Path(__file__).parent / "generated"
    
    if input_dir.exists():
        print("🧪 Testing reconstitution with examples directory...")
        try:
            original, reconstituted, report = reconstitute_object_list(str(input_dir), str(generated_dir))
            print(f"\n✅ Test completed successfully!")
            print(f"Report: {report}")
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
    else:
        print(f"❌ Examples directory not found: {input_dir}")