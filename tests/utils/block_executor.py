"""
Block Executor - Execute StixORM blocks with reference restoration
"""
from pathlib import Path
from typing import Dict, Any
import json
import importlib
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from Orchestration.Utilities.reconstitute_object_list import STIXReconstitutionEngine


class BlockExecutor:
    """Execute StixORM blocks with reference restoration"""
    
    def __init__(
        self, 
        stixorm_path: Path, 
        data_forms_dir: Path, 
        output_dir: Path
    ):
        """
        Initialize block executor
        
        Args:
            stixorm_path: Path to Block_Families/StixORM/
            data_forms_dir: Path to tests/generated/ (contains data forms)
            output_dir: Path to tests/generated/output_objects/
        """
        self.stixorm_path = Path(stixorm_path)
        self.data_forms_dir = Path(data_forms_dir)
        self.output_dir = Path(output_dir)
        self.reconstituted_objects = {}  # Cache for dependency resolution
        
        # Initialize the reconstitution engine
        generated_dir = self.data_forms_dir  # Already pointing to generated dir
        self.recon_engine = STIXReconstitutionEngine(generated_dir)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def execute_block(
        self, 
        stix_obj: Dict, 
        metadata: Any, 
        reconstitution_data: Dict
    ) -> Dict[str, Any]:
        """
        Execute a single block
        
        Process:
        1. Load data form from data_forms_dir
        2. Get reference info from reconstitution_data
        3. Restore references to data form
        4. Load embedded objects as inputs
        5. Dynamically import and call make_*.py block
        6. Save output
        7. Cache result for dependency resolution
        
        Args:
            stix_obj: Original STIX object
            metadata: ParseContent metadata
            reconstitution_data: Reference restoration metadata
            
        Returns:
            Reconstituted STIX object
        """
        obj_id = stix_obj['id']
        
        # 1. Find and load data form
        data_form = self._load_data_form(obj_id, metadata, stix_obj)
        if data_form is None:
            raise ValueError(f"Data form not found for {obj_id}")
        
        # 2. Get reference restoration info
        ref_info = self._get_ref_info(obj_id, reconstitution_data)
        
        # 3. Restore references using the reconstitution engine
        restored_form = self.recon_engine.restore_references_to_data_form(
            data_form, 
            ref_info, 
            {}  # id_mapping for new UUIDs
        )
        
        # 4. Load embedded objects as inputs
        embedded_inputs = self._load_embedded_objects(ref_info)
        
        # 5. Dynamically import and call block
        result = self._invoke_make_block(
            metadata, 
            restored_form, 
            embedded_inputs
        )
        
        # 6. Save and cache
        self._save_output(obj_id, metadata, result)
        self.reconstituted_objects[obj_id] = result
        
        return result
    
    def _invoke_make_block(
        self, 
        metadata: Any, 
        data_form: Dict, 
        embedded_inputs: Dict
    ) -> Dict:
        """
        Dynamically import and invoke make_*.py block
        
        Uses importlib to load module based on metadata.python_class
        Constructs input JSON structure expected by block's main() function
        
        Args:
            metadata: ParseContent metadata
            data_form: Data form with restored references
            embedded_inputs: Embedded reference objects
            
        Returns:
            Reconstituted STIX object
        """
        # Construct module path
        group_dir = metadata.group.upper()
        module_path = f"Block_Families.StixORM.{group_dir}.{metadata.python_class}.make_{metadata.typeql.replace('-', '_')}"
        
        try:
            # Import module
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(f"Failed to import {module_path}: {e}")
        
        # Prepare input structure
        input_data = {
            f"{metadata.typeql}_form": data_form,
            **embedded_inputs  # Add embedded objects
        }
        
        # Create temp input/output files
        input_file = self.data_forms_dir / f"temp_input_{metadata.typeql}_{id(data_form)}.json"
        output_file = self.output_dir / f"temp_output_{metadata.typeql}_{id(data_form)}.json"
        
        try:
            # Write input file
            with open(input_file, 'w', encoding='utf-8') as f:
                json.dump(input_data, f, indent=2)
            
            # Call block's main() function
            module.main(str(input_file), str(output_file))
            
            # Load result
            with open(output_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            # Extract object from result (blocks return {type: [obj]} or just obj)
            if isinstance(result, dict):
                # Check if it's a wrapped result
                for key, value in result.items():
                    if isinstance(value, list) and value:
                        return value[0]
                # Otherwise return as-is
                return result
            
            return result
            
        finally:
            # Cleanup temp files
            if input_file.exists():
                input_file.unlink()
            if output_file.exists():
                output_file.unlink()
    
    def _load_embedded_objects(self, ref_info: Dict) -> Dict:
        """
        Load embedded reference objects from cache or data forms
        
        Args:
            ref_info: Reference information from reconstitution_data
            
        Returns:
            Dictionary of embedded objects
        """
        embedded = {}
        
        # Check for embedded references in ref_info
        for ref_id in ref_info.get('embedded_references', []):
            if ref_id in self.reconstituted_objects:
                embedded[ref_id] = self.reconstituted_objects[ref_id]
        
        return embedded
    
    def _load_data_form(self, object_id: str, metadata: Any, stix_obj: Dict = None) -> Dict:
        """
        Load data form for object using the same filename computation as generation
        
        Args:
            object_id: STIX object ID
            metadata: ParseContent metadata
            stix_obj: Original STIX object (needed for filename computation)
            
        Returns:
            Data form dictionary
        """
        if stix_obj is not None:
            # Import filename computation function
            import sys
            sys.path.insert(0, str(self.data_forms_dir.parent.parent / 'Orchestration' / 'Utilities'))
            from convert_object_list_to_data_forms import compute_stable_filename_from_content
            
            # Compute the correct filename
            obj_type = stix_obj.get('type', 'unknown')
            expected_filename = compute_stable_filename_from_content(stix_obj, obj_type)
            form_file = self.data_forms_dir / expected_filename
            
            if form_file.exists():
                with open(form_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Data form files have structure: {"{type}_form": {"base_required": ...}}
                    # Extract the inner form structure
                    for key in data.keys():
                        if key.endswith('_form'):
                            return data[key]
                    return data
        
        # Fallback to old method if stix_obj not provided or file not found
        # Try to find data form file
        # Forms are typically named with the object type
        form_file = self.data_forms_dir / f"{object_id}.json"
        
        if not form_file.exists():
            # Try alternate naming with typeql
            form_file = self.data_forms_dir / f"{metadata.typeql}_{object_id}.json"
        
        if not form_file.exists():
            # Try just scanning all files for matching ID
            for json_file in self.data_forms_dir.glob("*.json"):
                if json_file.name.startswith("temp_"):
                    continue
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('id') == object_id:
                            return data
                except:
                    continue
            return None
        
        with open(form_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_ref_info(self, object_id: str, reconstitution_data: Dict) -> Dict:
        """
        Get reference info for object from reconstitution data
        
        Args:
            object_id: STIX object ID
            reconstitution_data: Full reconstitution metadata
            
        Returns:
            Reference information for this object
        """
        # reconstitution_data structure varies, find our object
        if object_id in reconstitution_data:
            return reconstitution_data[object_id]
        
        # Try alternate lookups
        for key, value in reconstitution_data.items():
            if isinstance(value, dict) and value.get('id') == object_id:
                return value
        
        # Return empty ref info if not found
        return {'embedded_references': [], 'external_references': []}
    
    def _save_output(self, object_id: str, metadata: Any, result: Dict):
        """
        Save reconstituted object to output directory
        
        Args:
            object_id: STIX object ID
            metadata: ParseContent metadata
            result: Reconstituted object
        """
        output_file = self.output_dir / f"{object_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
