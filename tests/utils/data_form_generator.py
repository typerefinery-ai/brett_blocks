"""
Data Form Generator - Wrapper around existing data form generation utilities
"""
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from Orchestration.Utilities.convert_object_list_to_data_forms import (
    create_data_forms_from_stix_objects
)


class DataFormGenerator:
    """Generate data forms from STIX objects"""
    
    def __init__(self, stixorm_path: Path, output_dir: Path):
        """
        Initialize data form generator
        
        Args:
            stixorm_path: Path to Block_Families/StixORM/
            output_dir: Path to tests/generated/
        """
        self.stixorm_path = Path(stixorm_path)
        self.output_dir = Path(output_dir)
    
    def generate_data_forms(
        self, 
        stix_objects: List[Dict[str, Any]]
    ) -> Tuple[Dict, Dict, List]:
        """
        Generate data forms using existing utility
        
        Calls: create_data_forms_from_stix_objects() from 
               convert_object_list_to_data_forms.py
               
        Args:
            stix_objects: List of STIX objects to convert
            
        Returns:
            (data_forms_dict, reconstitution_data, creation_sequence)
        """
        print(f"Generating data forms for {len(stix_objects)} objects...")
        
        try:
            result = create_data_forms_from_stix_objects(
                stix_objects,
                str(self.output_dir)
            )
            
            # The function writes files to disk but doesn't return them in a dict
            # Load the generated data forms from disk
            data_forms = {}
            for json_file in self.output_dir.glob("*_data_form.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        form_data = json.load(f)
                        data_forms[json_file.stem] = form_data
                except Exception as e:
                    print(f"Warning: Failed to load {json_file.name}: {e}")
            
            # Load reconstitution data
            recon_file = self.output_dir / 'reconstitution_data.json'
            reconstitution_data = {}
            if recon_file.exists():
                with open(recon_file, 'r', encoding='utf-8') as f:
                    reconstitution_data = json.load(f)
            
            # Load creation sequence
            seq_file = self.output_dir / 'creation_sequence.json'
            creation_sequence = []
            if seq_file.exists():
                with open(seq_file, 'r', encoding='utf-8') as f:
                    creation_sequence = json.load(f)
            
            print(f"Successfully generated {len(data_forms)} data forms")
            
            return data_forms, reconstitution_data, creation_sequence
            
        except Exception as e:
            print(f"Error generating data forms: {e}")
            raise
    
    def save_artifacts(self, data_forms, reconstitution_data, stix_objects):
        """
        Save generated artifacts to appropriate directories
        
        Args:
            data_forms: Dictionary of data forms
            reconstitution_data: Reference restoration metadata
            stix_objects: Original STIX objects
        """
        print("Saving artifacts...")
        
        # Ensure directories exist
        (self.output_dir / 'data_forms').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'input_objects').mkdir(parents=True, exist_ok=True)
        
        # Save data forms to generated/data_forms/
        for form_name, form_data in data_forms.items():
            form_file = self.output_dir / 'data_forms' / f"{form_name}.json"
            try:
                with open(form_file, 'w', encoding='utf-8') as f:
                    json.dump(form_data, f, indent=2)
            except Exception as e:
                print(f"Warning: Failed to save {form_name}: {e}")
        
        # Save input objects to generated/input_objects/
        for obj in stix_objects:
            obj_file = self.output_dir / 'input_objects' / f"{obj['id']}.json"
            try:
                with open(obj_file, 'w', encoding='utf-8') as f:
                    json.dump(obj, f, indent=2)
            except Exception as e:
                print(f"Warning: Failed to save object {obj.get('id')}: {e}")
        
        # Save reconstitution_data.json
        recon_file = self.output_dir / 'reconstitution_data.json'
        try:
            with open(recon_file, 'w', encoding='utf-8') as f:
                json.dump(reconstitution_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save reconstitution data: {e}")
        
        print(f"Saved {len(data_forms)} data forms and {len(stix_objects)} input objects")
