# Create a "Find Embedded" function that reads a Stix Object and returns all Embedded References

## Background

All stix identifier's,  MUST follow the form object-type--UUID, where object-type is the exact value (all type names are lowercase strings, by definition) from the type property of the object being identified or referenced and where the UUID MUST be an RFC 4122-compliant UUID

Every Stix Object has an `id` property that is a valid stix identifier for that object.

Some Stix Objects have properties that contain embedded references to other Stix Objects.  These embedded references are either in the form of a stix identifier string, or a list of stix identifier strings.

## Aim - Create a function that can parse a Stix Object and return all embedded references found in that object, grouped by the property name they were found under.

The major task of this prompt is to build a robust function that can parse any Stix Object and return all embedded references found in that object, grouped by the property name they were found under, by using the EmbeddedReferences Pydantic model below.

Before you create the code, you should first examine some examples in this list of stix objects Block_Families\General\_library\example_foreign_keys.json. You can see here different examples of embedded references in different properties of different stix objects. 

Note that what is not shown is that some objects have references with strange  proeprty names. So the finding of embedded references can only be done by examing the value of each property, where it is a string or a list of strings to see if they are valid identifiers, not by looking for specific property names.

Every time you see an:

- embedded reference property, then report it by adding the value to an empty list, and add the property name and reference list to the EmbeddedReferences model.
- list of embedded references property, then report it by adding the property name and reference list to the EmbeddedReferences model.

Once the function is complete it returns the EmbeddedReferences model instance containing all the found embedded references, in lists and grouped by property name.

You cazn build a small test routine to read in the example_foreign_keys.json file (Block_Families\General\_library\example_foreign_keys.json) and call the function to see the results.

## Pydantic Embedded References Interface

Us the following Pydantic model to represent the collection of embedded references found in a Stix Object:

```python
from pydantic import BaseModel, field_validator, Field
from typing import List, Dict
import re
import uuid


class EmbeddedReferences(BaseModel):
    """Collection of embedded STIX references grouped by property name."""
    
    references: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Property names mapped to lists of STIX IDs"
    )
    
    # STIX ID pattern: object-type--UUID (lowercase type, RFC 4122 UUID)
    _STIX_ID_PATTERN = re.compile(
        r'^[a-z][a-z0-9-]*--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    )
    
    @field_validator('references')
    @classmethod
    def validate_stix_ids(cls, v: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Validate all STIX IDs in the references dictionary."""
        for prop_name, id_list in v.items():
            if not isinstance(id_list, list):
                raise ValueError(f'Property "{prop_name}" must map to a list of STIX IDs')
            
            for stix_id in id_list:
                if not isinstance(stix_id, str):
                    raise ValueError(f'STIX ID must be string, got {type(stix_id).__name__}: {stix_id}')
                
                if not cls._STIX_ID_PATTERN.match(stix_id):
                    raise ValueError(
                        f'Invalid STIX ID in "{prop_name}": {stix_id}. '
                        'Must be object-type--UUID (lowercase, RFC 4122)'
                    )
                
                # Validate UUID portion
                try:
                    uuid_part = stix_id.split('--')[1]
                    uuid.UUID(uuid_part, version=4)
                except (IndexError, ValueError):
                    raise ValueError(f'Invalid UUID in STIX ID: {stix_id}')
        
        return v


# Example usage:
refs = EmbeddedReferences(references={
    "created_by_ref": ["identity--12345678-1234-1234-1234-123456789abc"],
    "object_refs": [
        "indicator--87654321-4321-4321-4321-cba987654321",
        "malware--11111111-2222-3333-4444-555555555555"
    ],
    "target_ref": ["identity--aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"]
})

print(refs.references)
# {'created_by_ref': ['identity--12345678-1234-1234-1234-123456789abc'], ...}
```