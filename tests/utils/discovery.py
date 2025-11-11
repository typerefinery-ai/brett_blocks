"""
Discovery Module - Load and filter STIX objects to identify testable ones
"""
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from Block_Families.General._library.parse import determine_content_object_from_list_by_tests


class ObjectDiscovery:
    """Discover testable STIX objects from examples directory"""
    
    def __init__(self, examples_dir: Path, stixorm_base: Path):
        """
        Initialize discovery module
        
        Args:
            examples_dir: Path to Block_Families/StixORM/examples/
            stixorm_base: Path to Block_Families/StixORM/
        """
        self.examples_dir = Path(examples_dir)
        self.stixorm_base = Path(stixorm_base)
    
    def load_all_stix_objects(self) -> List[Dict[str, Any]]:
        """
        Load all STIX objects from examples/*.json files
        
        Returns:
            List of STIX objects
        """
        all_objects = []
        
        if not self.examples_dir.exists():
            print(f"Warning: Examples directory not found: {self.examples_dir}")
            return all_objects
        
        for json_file in self.examples_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    
                    # Handle both single objects and lists
                    if isinstance(content, list):
                        all_objects.extend(content)
                    else:
                        all_objects.append(content)
                        
            except Exception as e:
                print(f"Warning: Failed to load {json_file}: {e}")
                continue
        
        print(f"Loaded {len(all_objects)} STIX objects from {self.examples_dir}")
        return all_objects
    
    def is_testable(self, stix_obj: Dict[str, Any]) -> Tuple[bool, Any, Path]:
        """
        Check if object has corresponding make_*.py block
        
        Process:
        1. Get ParseContent metadata using get_parse_content_for_object()
        2. Construct object path from metadata.group and metadata.python_class
        3. Check for make_*.py file in object directory
        
        Args:
            stix_obj: STIX object dictionary
            
        Returns:
            (is_testable, metadata, object_path)
        """
        try:
            # Get metadata using determine_content_object_from_list_by_tests
            metadata = determine_content_object_from_list_by_tests(stix_obj, "class")
            if metadata is None:
                return False, None, None
            
            # Construct object path
            group_dir = metadata.group.upper()  # SCO, SDO, SRO
            object_path = self.stixorm_base / group_dir / metadata.python_class
            
            # Check if directory exists
            if not object_path.exists():
                return False, None, None
            
            # Check for make_*.py files
            py_files = list(object_path.glob("make_*.py"))
            if py_files:
                return True, metadata, object_path
                
            return False, None, None
            
        except Exception as e:
            # Object doesn't have valid metadata
            return False, None, None
    
    def discover_testable_objects(self) -> List[Tuple[Dict, Any, Path]]:
        """
        Main discovery function - returns list of (object, metadata, path)
        
        Returns:
            List of tuples: (stix_object, metadata, block_path)
        """
        all_objects = self.load_all_stix_objects()
        testable = []
        
        for obj in all_objects:
            is_test, metadata, path = self.is_testable(obj)
            if is_test:
                testable.append((obj, metadata, path))
        
        print(f"Found {len(testable)} testable objects out of {len(all_objects)}")
        return testable
