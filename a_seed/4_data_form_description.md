# Data Forms all have a "Fixed" Structure for every Object

There are rules that must be followed for any valid STIX object data forms.:

1. **Data Form File Name**: Can be any name, suitable for the specific data context, so it can be referred to within a notebook.
2. **Form Data is a Dict**: The Form data file must be a valid JSON object (dictionary) with specific layout.
3. **First Property**: The first property in the dictionary must always be `<typeql name>_form` with a fixed value matching the STIX object type.
   ```json
   {
		"<typeql name>_form": {
			...
		}
   }
   ```
4. **First Value - Actual Form**: The value of the first property is itself a dictionary containing the full form structure, using the same set of keys and properties as in the class template, but the values are actual data values instead of property definitions.:
- `base_required`: Required base properties across each STIX object groups: SDO, SCO, SRO, META.
- `base_optional`: Optional base properties across each STIX object groups.
- `object`: The main STIX object properties specific to this object type.
- `extensions`: Any STIX extensions applicable to this object type.
- `sub`: Any nested sub-objects, based on the EmbeddedObjectProperty in the class template

## Conversion between Stix JSON Data and Data Forms Using the Class Template as a Reference

Consider the task of converting between a STIX JSON object and a Data Form, where the Class Template serves as the reference for this conversion. Lets use the example of an identity, as it includes both extensions and sub objects.

First, examine the identity class template either here Block_Families\StixORM\SDO\Identity\Identity_template.json, or at the bottom of the previous page a_seed\3_class_template_description.md

Assume the data example you are going to convert is the following Stix Identity object:

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
````

### Conversion Rules

When converting between the STIX JSON object and the Data Form, follow these rules:
1. **Dont Copy Across Embedded References**: For any properties that are references to other STIX objects (e.g., `email_address_ref`, `user_account_ref`), do not copy the reference value into the data form. Instead, leave these properties empty or null in the data form. Assume these are going to be additional inputs on the Python block code and added as inputs to this form in a notebook
2. **Leave Out Base Required Properties**: If the use case is for demo data, where it the data forms will be made with make_object functions, then you can leave the "base_required" properties as empty strings, except for the type, as these will be auto generated when the object is created.


### Resulting Data Form

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