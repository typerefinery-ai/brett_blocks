#!/usr/bin/env python3
"""
STIX Object Reconstitution and Notebook Generation Module

This module provides two operational modes:

MODE 1 (Test): Reconstitute STIX objects from data forms for testing
MODE 2 (Notebook Generation): Generate executable notebooks that create objects using data forms

In Mode 2, the system:
1. Stores data forms alongside their templates in Block_Families/StixORM/
2. Generates Jupyter notebooks in Orchestration/ directory
3. Creates notebooks that invoke blocks to create objects in sequence
4. Saves objects to specified context memory locations (unattached, incident, company, or user)
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Literal
import sys
from datetime import datetime

# Import the reconstitution engine from the same directory
from .reconstitute_object_list import reconstitute_object_list


class NotebookGenerator:
    """Generates Jupyter notebooks for creating STIX objects from data forms"""
    
    # Context type mapping to save functions
    CONTEXT_SAVE_FUNCTIONS = {
        'unattached': 'invoke_save_unattached_context_block',
        'incident': 'invoke_save_incident_context_block',
        'company': 'invoke_save_company_context_block',
        'user': 'invoke_save_user_context_block'
    }
    
    CONTEXT_SAVE_PATHS = {
        'unattached': 'Block_Families/OS_Triage/Save_Context/save_unattached_context.py',
        'incident': 'Block_Families/OS_Triage/Save_Context/save_incident_context.py',
        'company': 'Block_Families/OS_Triage/Save_Context/save_company_context.py',
        'user': 'Block_Families/OS_Triage/Save_Context/save_user_context.py'
    }
    
    def __init__(self, orchestration_dir: Path):
        """Initialize notebook generator with target directory"""
        self.orchestration_dir = Path(orchestration_dir)
        self.orchestration_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_notebook(
        self,
        notebook_name: str,
        creation_sequence: List[Dict[str, Any]],
        detailed_references: List[Dict[str, Any]],
        context_type: Literal['unattached', 'incident', 'company', 'user'],
        title: str = None,
        description: str = None
    ) -> Path:
        """
        Generate a Jupyter notebook that creates STIX objects in sequence
        
        Args:
            notebook_name: Name of the notebook file (without .ipynb extension)
            creation_sequence: List of objects in dependency order
            detailed_references: Reference tracking data
            context_type: Where to save objects (unattached, incident, company, user)
            title: Notebook title (optional, defaults to notebook_name)
            description: Notebook description (optional)
            
        Returns:
            Path to the generated notebook file
        """
        if title is None:
            title = notebook_name.replace('_', ' ').title()
        
        if description is None:
            description = f"Auto-generated notebook to create STIX objects and save to {context_type} context"
        
        # Build notebook cells
        cells = []
        
        # Title cell
        cells.append(self._create_markdown_cell(
            f"# {title}\n\n{description}\n\n"
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Context Type**: {context_type}\n"
            f"**Object Count**: {len(creation_sequence)}\n\n"
            "This notebook creates STIX objects using data forms and saves them to context memory."
        ))
        
        # Setup cells
        cells.extend(self._create_setup_cells())
        
        # Import utilities cell
        cells.append(self._create_imports_cell(context_type))
        
        # Group objects by type for organized creation
        objects_by_type = self._group_objects_by_type(creation_sequence)
        
        # Create cells for each object type
        for obj_type, objects in objects_by_type.items():
            cells.append(self._create_type_section_cell(obj_type, len(objects)))
            cells.extend(self._create_object_creation_cells(objects, obj_type, context_type))
        
        # Summary cell
        cells.append(self._create_summary_cell(len(creation_sequence), context_type))
        
        # Build notebook JSON
        notebook_data = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.11.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 2
        }
        
        # Save notebook
        notebook_path = self.orchestration_dir / f"{notebook_name}.ipynb"
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        return notebook_path
    
    def _create_markdown_cell(self, content: str) -> Dict:
        """Create a markdown cell"""
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": content.split('\n')
        }
    
    def _create_code_cell(self, code: str) -> Dict:
        """Create a code cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.split('\n')
        }
    
    def _create_setup_cells(self) -> List[Dict]:
        """Create initial setup cells"""
        cells = []
        
        # Environment setup
        cells.append(self._create_markdown_cell(
            "## A.1 Environment Setup\n\n"
            "Initialize STIX libraries and import required modules."
        ))
        
        cells.append(self._create_code_cell(
            "# Install required STIX libraries\n"
            "import sys\n"
            "!{sys.executable} -m pip install stixorm\n\n"
            "# Import core STIX 2.1 objects\n"
            "from stixorm.module.authorise import import_type_factory\n"
            "from stixorm.module.definitions.stix21 import *\n\n"
            "# Import processing utilities\n"
            "from stixorm.module.typedb_lib.instructions import ResultStatus, Result\n"
            "from stixorm.module.parsing import parse_objects\n\n"
            "# Initialize import factory\n"
            "import_type = import_type_factory.get_all_imports()\n\n"
            "# Setup logging\n"
            "import logging\n"
            "logger = logging.getLogger(__name__)\n"
            "logger.setLevel(logging.INFO)\n\n"
            "print('✅ STIX libraries initialized')"
        ))
        
        # Path configuration
        cells.append(self._create_markdown_cell(
            "## A.2 Path Configuration\n\n"
            "Configure Python paths and working directory."
        ))
        
        cells.append(self._create_code_cell(
            "# Configure Python path for relative imports\n"
            "import sys\n"
            "sys.path.append('../')\n"
            "import os\n\n"
            "cwd = os.getcwd()\n"
            "print(f'✅ Working directory: {cwd}')\n"
            "print('✅ Python path configured')"
        ))
        
        return cells
    
    def _create_imports_cell(self, context_type: str) -> Dict:
        """Create cell with utility imports"""
        save_function = self.CONTEXT_SAVE_FUNCTIONS[context_type]
        
        code = (
            "import json\n"
            "import os\n\n"
            "# Import Brett Blocks utility functions\n"
            f"from Utilities.local_make_general import {save_function}, invoke_make_object_from_data_form_block\n"
            "from Utilities.util import emulate_ports, unwind_ports, conv\n\n"
            "# Import STIX object creation utilities\n"
            "from Utilities.local_make_sdo import *\n"
            "from Utilities.local_make_sco import *\n"
            "from Utilities.local_make_sro import *\n\n"
            "# Configure base paths\n"
            "path_base = '../Block_Families/StixORM/'\n"
            "results_base = '../Orchestration/Results/'\n\n"
            "# Ensure generated directory exists\n"
            "os.makedirs(results_base + 'generated/context', exist_ok=True)\n\n"
            "print('✅ Brett Blocks utilities imported')\n"
            f"print('✅ Context type: {context_type}')"
        )
        
        return self._create_code_cell(code)
    
    def _group_objects_by_type(self, creation_sequence: List[Dict]) -> Dict[str, List[Dict]]:
        """Group objects by their STIX type"""
        grouped = {}
        for obj in creation_sequence:
            form_name = obj['form_name']
            if form_name not in grouped:
                grouped[form_name] = []
            grouped[form_name].append(obj)
        return grouped
    
    def _create_type_section_cell(self, obj_type: str, count: int) -> Dict:
        """Create a markdown cell for an object type section"""
        type_display = obj_type.replace('-', ' ').replace('_', ' ').title()
        return self._create_markdown_cell(
            f"## Create {type_display} Objects\n\n"
            f"Creating {count} {type_display} object(s) and saving to context memory."
        )
    
    def _create_object_creation_cells(
        self,
        objects: List[Dict],
        obj_type: str,
        context_type: str
    ) -> List[Dict]:
        """Create cells for creating objects of a specific type"""
        cells = []
        save_function = self.CONTEXT_SAVE_FUNCTIONS[context_type]
        
        for i, obj in enumerate(objects, 1):
            filename = obj['filename']
            obj_id = obj['object_id']
            
            # Extract the data form path from filename
            # Data forms are stored alongside templates in Block_Families/StixORM/
            data_form_path = self._get_data_form_path(obj_type, filename)
            
            # Determine the block invocation function
            invoke_function = self._get_invoke_function(obj_type)
            
            # Create description cell
            cells.append(self._create_markdown_cell(
                f"### {obj_type.title()} #{i}\n\n"
                f"Create object from data form: `{filename}`"
            ))
            
            # Create code cell
            code = (
                f"# Load data form and create object\n"
                f"data_form_path = '{data_form_path}'\n"
                f"results_path = 'generated/{obj_type}_{i}.json'\n\n"
                f"print(f'📝 Creating {obj_type} from data form...')\n\n"
                f"# Create object from data form using utility block\n"
                f"obj_{i} = invoke_make_object_from_data_form_block(data_form_path, results_path)\n\n"
                f"# Configure context type\n"
                f"context_type = {{'context_type': '{context_type}'}}\n\n"
                f"# Define storage paths\n"
                f"obj_path = results_base + results_path\n"
                f"context_path = results_base + 'generated/context/{obj_type}_{i}_context.json'\n\n"
                f"# Save to {context_type} context\n"
                f"result = {save_function}(obj_path, context_path, context_type)\n\n"
                f"print(f'✅ {obj_type} #{i} created successfully')\n"
                f"print(f'   Object: {{obj_path}}')\n"
                f"print(f'   Context saved: {{result}}')"
            )
            
            cells.append(self._create_code_cell(code))
        
        return cells
    
    def _get_data_form_path(self, obj_type: str, filename: str) -> str:
        """Get the path to a data form file relative to the STIX ORM directory"""
        # Map STIX types to their directory structure
        # SCO objects go in SCO/<Type>/
        # SDO objects go in SDO/<Type>/
        # SRO objects go in SRO/<Type>/
        
        if obj_type in ['ipv4-addr', 'ipv6-addr', 'email-addr', 'domain-name', 'url', 
                        'file', 'directory', 'process', 'network-traffic', 'user-account',
                        'windows-registry-key', 'x509-certificate', 'artifact', 'autonomous-system',
                        'mac-addr', 'mutex', 'software']:
            category = 'SCO'
        elif obj_type in ['relationship', 'sighting']:
            category = 'SRO'
        else:
            category = 'SDO'
        
        # Convert type name to directory format (e.g., 'email-addr' -> 'Email_Addr')
        type_dir = self._type_to_directory(obj_type)
        
        return f"{category}/{type_dir}/{filename}"
    
    def _type_to_directory(self, obj_type: str) -> str:
        """Convert STIX type to directory name format"""
        # Convert 'email-addr' to 'Email_Addr', 'attack-pattern' to 'Attack_Pattern', etc.
        parts = obj_type.split('-')
        return '_'.join(word.capitalize() for word in parts)
    
    def _get_invoke_function(self, obj_type: str) -> str:
        """Get the invoke function name for a STIX type"""
        # Map types to their invoke functions
        type_to_function = {
            # SDO
            'attack-pattern': 'invoke_make_attack_pattern_block',
            'campaign': 'invoke_make_campaign_block',
            'course-of-action': 'invoke_make_course_of_action_block',
            'grouping': 'invoke_make_grouping_block',
            'identity': 'invoke_make_identity_block',
            'incident': 'invoke_make_incident_block',
            'indicator': 'invoke_make_indicator_block',
            'infrastructure': 'invoke_make_infrastructure_block',
            'intrusion-set': 'invoke_make_intrusion_set_block',
            'location': 'invoke_make_location_block',
            'malware': 'invoke_make_malware_block',
            'malware-analysis': 'invoke_make_malware_analysis_block',
            'note': 'invoke_make_note_block',
            'observed-data': 'invoke_make_observed_data_block',
            'opinion': 'invoke_make_opinion_block',
            'report': 'invoke_make_report_block',
            'threat-actor': 'invoke_make_threat_actor_block',
            'tool': 'invoke_make_tool_block',
            'vulnerability': 'invoke_make_vulnerability_block',
            # SCO
            'artifact': 'invoke_make_artifact_block',
            'autonomous-system': 'invoke_make_autonomous_system_block',
            'directory': 'invoke_make_directory_block',
            'domain-name': 'invoke_make_domain_name_block',
            'email-addr': 'invoke_make_email_addr_block',
            'email-message': 'invoke_make_e_msg_block',
            'file': 'invoke_make_file_block',
            'ipv4-addr': 'invoke_make_ipv4_addr_block',
            'ipv6-addr': 'invoke_make_ipv6_addr_block',
            'mac-addr': 'invoke_make_mac_addr_block',
            'mutex': 'invoke_make_mutex_block',
            'network-traffic': 'invoke_make_network_traffic_block',
            'process': 'invoke_make_process_block',
            'software': 'invoke_make_software_block',
            'url': 'invoke_make_url_block',
            'user-account': 'invoke_make_user_account_block',
            'windows-registry-key': 'invoke_make_windows_registry_key_block',
            'x509-certificate': 'invoke_make_x509_certificate_block',
            # SRO
            'relationship': 'invoke_sro_block',
            'sighting': 'invoke_sighting_block',
        }
        
        return type_to_function.get(obj_type, 'invoke_make_generic_block')
    
    def _create_summary_cell(self, object_count: int, context_type: str) -> Dict:
        """Create a summary cell at the end of the notebook"""
        return self._create_markdown_cell(
            f"## Summary\n\n"
            f"✅ Successfully created {object_count} STIX objects\n"
            f"✅ All objects saved to {context_type} context\n\n"
            "All objects are now available in context memory for use in investigations and analysis."
        )


def reconstitute_and_generate(
    mode: Literal['test', 'notebook'],
    stix_objects: List[Dict[str, Any]] = None,
    data_forms_dir: Path = None,
    reconstitution_data_file: Path = None,
    output_dir: Path = None,
    notebook_name: str = None,
    context_type: Literal['unattached', 'incident', 'company', 'user'] = 'unattached',
    notebook_title: str = None,
    notebook_description: str = None
) -> Dict[str, Any]:
    """
    Main function supporting both test and notebook generation modes
    
    MODE 1 (test): Reconstitute objects for testing
        Required: data_forms_dir, reconstitution_data_file, output_dir
        
    MODE 2 (notebook): Generate notebooks for object creation
        Required: stix_objects, notebook_name, context_type
        Optional: notebook_title, notebook_description
        
    Returns:
        Dict with results including success status and generated files
    """
    results = {
        'mode': mode,
        'success': False,
        'generated_files': [],
        'errors': []
    }
    
    if mode == 'test':
        # Mode 1: Test reconstitution
        if not all([data_forms_dir, reconstitution_data_file, output_dir]):
            results['errors'].append("Test mode requires: data_forms_dir, reconstitution_data_file, output_dir")
            return results
        
        try:
            # Use existing reconstitution function
            success = reconstitute_object_list(
                data_forms_dir=data_forms_dir,
                reconstitution_data_file=reconstitution_data_file,
                output_dir=output_dir
            )
            
            results['success'] = success
            if success:
                results['generated_files'] = list(output_dir.glob('*.json'))
                
        except Exception as e:
            results['errors'].append(f"Reconstitution failed: {str(e)}")
            
    elif mode == 'notebook':
        # Mode 2: Generate notebooks
        if not all([stix_objects, notebook_name]):
            results['errors'].append("Notebook mode requires: stix_objects, notebook_name")
            return results
        
        try:
            # First, convert objects to data forms and store alongside templates
            from .convert_object_list_to_data_forms import create_data_forms_from_stix_objects
            
            # Generate data forms in template directories with reference tracking
            # Using test_directory enables Mode 2 which provides reference tracking data
            test_dir = Path("Block_Families/StixORM")
            data_form_results = create_data_forms_from_stix_objects(
                stix_objects=stix_objects,
                test_directory=str(test_dir)
            )
            
            if data_form_results['report']['successful'] == 0:
                results['errors'].append("No data forms were successfully created")
                return results
            
            # Load creation sequence and references from the generated files
            reconstitution_file = test_dir / "reconstitution_data.json"
            with open(reconstitution_file, 'r', encoding='utf-8') as f:
                reconstitution_data = json.load(f)
            
            creation_sequence = reconstitution_data['creation_sequence']
            detailed_references = reconstitution_data['detailed_reference_extraction']
            
            # Generate notebook
            orchestration_dir = Path("Orchestration")
            generator = NotebookGenerator(orchestration_dir)
            
            notebook_path = generator.generate_notebook(
                notebook_name=notebook_name,
                creation_sequence=creation_sequence,
                detailed_references=detailed_references,
                context_type=context_type,
                title=notebook_title,
                description=notebook_description
            )
            
            results['success'] = True
            results['generated_files'].append(notebook_path)
            results['data_forms_created'] = data_form_results['report']['successful']
            results['notebook_path'] = str(notebook_path)
            
        except Exception as e:
            results['errors'].append(f"Notebook generation failed: {str(e)}")
            import traceback
            results['errors'].append(traceback.format_exc())
    
    else:
        results['errors'].append(f"Invalid mode: {mode}. Must be 'test' or 'notebook'")
    
    return results


if __name__ == '__main__':
    # Example usage
    print("STIX Object Reconstitution and Notebook Generation Module")
    print("=" * 60)
    print("\nUsage modes:")
    print("  1. Test mode: Reconstitute objects for validation")
    print("  2. Notebook mode: Generate executable notebooks")
    print("\nSee module documentation for detailed usage examples.")
