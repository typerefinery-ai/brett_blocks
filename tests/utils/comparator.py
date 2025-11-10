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
        
        - Sort all reference lists (_ref, _refs fields)
        - Sort sequence-specific reference fields
        - Preserve structure for proper comparison
        
        Args:
            obj: STIX object to normalize
            
        Returns:
            Normalized copy of object
        """
        normalized = copy.deepcopy(obj)
        
        # Normalize standard reference fields
        for key, value in normalized.items():
            if key.endswith('_ref') or key.endswith('_refs'):
                if isinstance(value, list):
                    normalized[key] = sorted(value)
        
        # Normalize sequence-specific fields
        for field in self.sequence_ref_fields:
            if field in normalized and isinstance(normalized[field], list):
                normalized[field] = sorted(normalized[field])
        
        return normalized
    
    def compare_objects(
        self, 
        original: Dict, 
        reconstituted: Dict
    ) -> Tuple[bool, Dict]:
        """
        Compare two objects
        
        Args:
            original: Original STIX object
            reconstituted: Reconstituted STIX object
            
        Returns:
            (is_identical, differences_dict)
        """
        try:
            from deepdiff import DeepDiff
        except ImportError:
            raise ImportError("deepdiff is required. Install with: pip install deepdiff")
        
        norm_orig = self.normalize_object(original)
        norm_recon = self.normalize_object(reconstituted)
        
        # Exclude fields that will differ (UUIDs, timestamps)
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
