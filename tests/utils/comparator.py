"""
Comparator Module - Compare STIX objects using DeepDiff with normalization
"""
from typing import Dict, Any, Tuple
import copy


class ObjectComparator:
    """Compare STIX objects using DeepDiff with normalization"""
    
    def __init__(self):
        """Initialize comparator with field configurations"""
        self.sequence_ref_fields = [
            'on_completion', 'sequenced_object', 'next_steps',
            'on_success', 'on_failure'
        ]
    
    def normalize_object(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize object for comparison
        
        This matches the approach in temporary_reconstitution_testing/runner.py:
        - Replace all UUID-based IDs with normalized placeholders
        - Normalize timestamps to standard format
        - Recursively normalize all reference fields
        
        This allows structural comparison while ignoring UUID differences.
        
        Args:
            obj: STIX object to normalize
            
        Returns:
            Normalized copy of object
        """
        normalized = copy.deepcopy(obj)
        
        # Replace UUID-based ID with normalized placeholder
        if 'id' in normalized:
            obj_type = normalized.get('type', 'unknown')
            normalized['id'] = f"{obj_type}--normalized-uuid"
        
        # Normalize timestamps to standard format
        for time_field in ['created', 'modified']:
            if time_field in normalized:
                normalized[time_field] = "2023-01-01T00:00:00.000Z"
        
        # Recursively normalize all references
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
                        data[key] = sorted(normalized_refs)  # Sort for consistent comparison
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
                        data[key] = sorted(normalized_refs)  # Sort for consistent comparison
                    elif isinstance(value, (dict, list)):
                        normalize_references(value)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, (dict, list)):
                        normalize_references(item)
        
        normalize_references(normalized)
        return normalized
    
    def compare_objects(
        self, 
        original: Dict, 
        reconstituted: Any
    ) -> Tuple[bool, Dict]:
        """
        Compare two objects
        
        Args:
            original: Original STIX object
            reconstituted: Reconstituted object (could be dict, string, or other type)
            
        Returns:
            (is_identical, differences_dict)
        """
        try:
            from deepdiff import DeepDiff
        except ImportError:
            raise ImportError("deepdiff is required. Install with: pip install deepdiff")
        
        # Check if reconstituted is the expected type
        if not isinstance(reconstituted, dict):
            return False, {
                'error': f'Reconstituted object is {type(reconstituted).__name__}, expected dict',
                'value': str(reconstituted)[:200]
            }
        
        norm_orig = self.normalize_object(original)
        norm_recon = self.normalize_object(reconstituted)
        
        # Use DeepDiff with ignore_order
        # UUID normalization is handled in normalize_object()
        diff = DeepDiff(
            norm_orig,
            norm_recon,
            exclude_paths=[
                "root['id']",
                "root['created']", 
                "root['modified']"
            ],
            ignore_order=True
        )
        
        return (not bool(diff), dict(diff) if diff else {})
