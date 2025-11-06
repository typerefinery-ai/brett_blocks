# Create Data Forms from STIX JSON Using Class Templates

## Context

This prompt instructs AI assistants to convert STIX JSON objects into Brett Blocks data forms using class templates as reference. This approach is part of the Brett Blocks template-driven architecture for cybersecurity intelligence processing.

## When to Use This Prompt

- Converting STIX JSON objects to Brett Blocks data forms
- Creating data templates for the template-driven architecture
- Ensuring proper structure preservation from class templates
- Extracting embedded references for separate Python block parameters

## Required Input

1. **STIX JSON Object**: The source cybersecurity object to convert
2. **Class Template**: The corresponding `{ClassName}_template.json` file that defines the structure
3. **Target Directory**: Location in `Block_Families/StixORM/{SDO|SCO|SRO}/{ClassName}/` structure

## Expected Output

A properly structured data form file following the template-driven pattern:
- File name: `{descriptive_name}.json` 
- Root key: `{typeql_name}_form`
- Structure: Preserves class template sections with actual data values
- References: Extracted as separate parameters (not embedded)

## Prompt Template

```
I need you to convert a STIX JSON object to a Brett Blocks data form using the class template as reference.

**STIX JSON Object:**
[paste STIX JSON here]

**Class Template Path:** 
Block_Families/StixORM/{SDO|SCO|SRO}/{ClassName}/{ClassName}_template.json

**Conversion Requirements:**

**⚠️ CRITICAL RULES FOR EXTENSIONS AND SUB-OBJECTS:**

1. **Extension Reference Rule**: Any field ending in `_ref` or `_refs` inside extensions must be empty string "" or empty array []
2. **Extension Embedded Objects Rule**: Arrays of embedded objects (like contact_numbers, email_addresses) must be empty arrays [] in extensions
3. **Sub Section Rule**: All embedded object data goes to the `sub` section with references removed

1. **Structure Preservation**: Follow the exact template structure:
   - `base_required`: Required base STIX properties
   - `base_optional`: Optional base STIX properties  
   - `object`: Main object-specific properties
   - `extensions`: STIX extensions with simple values only (no embedded objects, no references)
   - `sub`: Sub-objects extracted from embedded references

2. **Property Conversion Rules**:
   - Template property definitions → actual data values
   - StringProperty → string value or empty string ""
   - ListProperty → array with actual values or []
   - ReferenceProperty → empty string "" (handled as separate parameters)
   - IntegerProperty → number value
   - BooleanProperty → true/false/null
   - TimestampProperty → ISO timestamp or "" for auto-generation

3. **Reference Extraction**:
   - Properties ending in `_ref`: Extract as separate parameter, leave empty string "" in data form
   - Properties ending in `_refs`: Extract as separate parameter, leave empty array [] in data form
   - All other values that are single stix-id (<object-type>--<uuid>) or arrays of stix-ids: Extract as separate parameters
   - **CRITICAL**: This applies EVERYWHERE including inside extensions and sub-objects
   - **CRITICAL**: When extracting references from extensions, the extension field becomes empty string or empty array, and the actual reference data goes to sub section

4. **Type Accuracy**:
   - Ensure `base_required.type` matches the correct STIX object type
   - Use `{typeql_name}_form` as root key (convert ClassName to lowercase-with-dashes)

5. **Auto-Generated Fields**:
   - Leave `id`, `created`, `modified` as empty strings for auto-generation
   - Keep `type` and `spec_version` with actual values

6. **Sub-Objects Handling**:
   - When the class template uses an `EmbeddedObjectProperty`, ensure that the `sub` section contains the actual embedded object data and use the field name as the key.
   - The `sub` section may contain either a single sub-object or an array of sub-objects, depending on the template definition.
   - **CRITICAL**: For extensions with embedded objects (like contact_numbers, email_addresses, social_media_accounts):
     - Leave the extension field as empty array []
     - Move the actual embedded object data to the sub section
     - Remove any reference values (_ref fields) from the sub section data and leave as empty strings

7. **Extension Processing Rules**:
   - Extensions contain property definitions and simple values only
   - **NO embedded objects** in extensions - move to sub section
   - **NO reference values** in extensions - extract as separate parameters
   - Arrays of embedded objects become empty arrays [] in extensions
   - Reference fields become empty strings "" in extensions
   - All extensions and sub-objects should also be searched for `EmbeddedObjectProperty` usages and handled similarly.

Please create the data form and identify any extracted references that should be separate Python block parameters.
```

## ⚠️ COMMON MISTAKES TO AVOID

### **❌ WRONG - References and Embedded Objects in Extensions:**
```json
"extensions": {
    "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
        "extension_type": "property-extension",
        "contact_numbers": [
            {
                "contact_number_type": "work-phone",
                "contact_number": "123-456-7890"
            }
        ],
        "email_addresses": [
            {
                "digital_contact_type": "work",
                "email_address_ref": "email-addr--4722424c-7012-56b0-84d5-01d076fc547b"
            }
        ]
    }
}
```

### **✅ CORRECT - Empty Arrays in Extensions, Data in Sub:**
```json
"extensions": {
    "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
        "extension_type": "property-extension",
        "contact_numbers": [],
        "email_addresses": [],
        "first_name": "Paolo",
        "team": "responders"
    }
},
"sub": {
    "contact_numbers": [
        {
            "contact_number_type": "work-phone",
            "contact_number": "123-456-7890"
        }
    ],
    "email_addresses": [
        {
            "digital_contact_type": "work",
            "email_address_ref": ""
        }
    ]
}
```

## Example Usage

Compare the two examples below with the class template here Block_Families\StixORM\SDO\Identity\Identity_template.json

### Input:
```json
{
    "type": "identity",
    "id": "identity--4e0dd272-7d68-4c8d-b6bc-0cb9d4b8e924",
    "created": "2022-05-06T01:01:01.000Z",
    "modified": "2022-12-16T01:01:01.000Z",
    "spec_version": "2.1",
    "name": "Paolo",
    "description": "The main point of contact for the incident.",
    "identity_class": "individual",
    "roles": [
        "security-point-of-contact"
    ],
    "contact_information": "Ring him as he is unreliable on Slack",
    "extensions": {
        "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
            "extension_type": "property-extension",
            "team": "responders",
            "first_name": "Paolo",
            "middle_name": "",
            "last_name": "Di Prodi",
            "contact_numbers": [
                {
                    "contact_number": "123-456-7890",
                    "contact_number_type": "work-phone"
                }
            ],
            "email_addresses": [
                {
                    "email_address_ref": "email-addr--06029cc1-105d-5495-9fc5-3d252dd7af76",
                    "digital_contact_type": "work"
                },
                {
                    "email_address_ref": "email-addr--78b946aa-91ab-5ce8-829b-4d078a8ecc00",
                    "digital_contact_type": "organizational"
                }
            ],
            "social_media_accounts": [
                {
                    "user_account_ref": "user-account--7aa68be3-1d4d-5b0f-8c26-8410085e5741",
                    "digital_contact_type": "career",
                    "description": "Paolo's LinkeIn contact details"
                }
            ]
        }
    }
}
```

### Expected Output:
```json
{
    "identity_form": {
        "base_required": {
            "type": "identity",
            "spec_version": "2.1",
            "id": "",
            "created": "",
            "modified": ""
        },
        "base_optional": {
            "created_by_ref": "",
            "revoked": null,
            "labels": [],
            "lang": "",
            "external_references": [],
            "object_marking_refs": [],
            "granular_markings": [],
            "defanged": null
        },
        "object": {
            "name": "Paolo",
            "description": "The main point of contact for the incident.",
            "roles": [
                "security-point-of-contact"
            ],
            "identity_class": "individual",
            "sectors": [
                "technology"
            ],
    		"contact_information": "Ring him as he is unreliable on Slack",
        },
        "extensions": {
            "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
                "extension_type": "property-extension",
                "contact_numbers": [],
                "email_addresses": [],
                "social_media_accounts": [],
            "team": "responders",
            "first_name": "Paolo",
            "middle_name": "",
            "last_name": "Di Prodi",
            }
        },
        "sub": {
            "contact_numbers": [
                {
                    "contact_number_type": "work-phone",
                    "contact_number": "123-456-7890"
                }
            ],
            "email_addresses": [
                {
                    "digital_contact_type": "organizational"
                }
            ],
            "social_media_accounts": [
                {
                    "digital_contact_type": "career",
                    "description": "Paolo's LinkeIn contact details"
                }
            ]
        }
    }
}
```

## Quality Checklist

- [ ] Root key uses correct `{typeql_name}_form` pattern
- [ ] All five template sections present: base_required, base_optional, object, extensions, sub
- [ ] Type field matches correct STIX object type
- [ ] Auto-generated fields (id, created, modified) are empty strings
- [ ] Reference fields are empty strings/arrays (extracted separately)
- [ ] **CRITICAL**: Extensions contain NO reference values (_ref fields are empty strings)
- [ ] **CRITICAL**: Extensions contain NO embedded objects (arrays are empty [])
- [ ] **CRITICAL**: Sub section contains all embedded object data
- [ ] **CRITICAL**: Reference fields in sub objects are empty strings (extracted separately)
- [ ] Embedded objects moved to sub section
- [ ] Property types converted according to mapping rules
- [ ] Extensions contain simple values only, not property definitions
- [ ] Sub section contains actual embedded object data, when the EmbeddedObjectProperty is used in a template

## Reference Documentation

- Architecture analysis: `architecture/stix-data-form-conversion-complete-analysis.md`
- Template structure: `a_seed/3_class_template_description.md`  
- Data form rules: `a_seed/4_data_form_description.md`
- Implementation guide: `.github/instructions/stix-guidelines.md`