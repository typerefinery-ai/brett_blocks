# Class Templates all have a "Fixed" Structure

There are rules that must be followed for any valid STIX object class template (`*_template.json`):

1. **Template File Name**: Must start with the Python class name, end with `_template.json` to be recognized as a class template.
2. **Template is a Dict**: The template file must be a valid JSON object (dictionary) with specific layout.
3. **First Property**: The first property in the `properties` dictionary must always be `class_name` with a fixed value matching the STIX object type.
4. **Second Property**: The second property must be Python class name plus underscore, plus `template`, which is itself a dictionary containing the full template structure:
   ```json
   {
		"class_name": "Artifact",
		"Artifact_template": {
			...
		}
   }
   ```

5. **Template Structure**: The template structure must include the following top-level keys:
   - `_type`: The STIX object type (e.g., "artifact").
   - `base_required`: Required base properties across each STIX object groups: SDO, SCO, SRO, META.
   - `base_optional`: Optional base properties across each STIX object groups.
   - `object`: The main STIX object properties specific to this object type.
   - `extensions`: Any STIX extensions applicable to this object type.
   - `sub`: Any nested sub-objects or properties.
6. **Extension Naming**: If the object has any extensions, the `extensions` key is in the STIX type format of the property (e.g., "ntfs-ext").
7. **Sub Objects**: If the object has nested sub-objects, they are defined under the `sub` key, but their name is in the Python class format (e.g. `ContactNumber`).

Recall that there are 3 types of names for any object in this repo:

8. **Three Types of Names, each with a specific Format**: There are 3 types of names for any object in this repo:

- **Class Name**: The name of the Python class, unique for every object, capitalised, no spaces
- **TypeQL Name**: The name of the TypeQL object, converted from the Class Name, unique for each object, lowercase with dashes between words
- **Stix Type**: The name of the object type, not unique for all object, lowercase with dashes

### 8.1 Examples of names

| Class Name     | TypeQL Name                        | Stix Type          |
|:--------------|:------------|:-------------------|
| "EmailAddress" | "email-address" | "email-addr" |
| "Finding"      | "finding"       | "x-ibm-finding"        |
| "Technique"     | "technique"      | "attack-pattern"       |
| "AttackPattern" | "attack-pattern" | "attack-pattern" |
| "HTTPRequestExt" | "http-request-ext" | "http-request-ext" |
| "WindowsPEBinaryExt" | "windows-pe-binary-ext" | "windows-pebinary-ext" |

9. **Converting between the three name types**: To convert between the three name types, Copilot must reference the object conversion list files for all Stix dialects. These files provide mappings between Class Names, TypeQL Names, and Stix Types.

To convert between them, copilot must join each of the object conversion list files in the StixORM dialects, and search for the correct class based on any of the extension object's key

### 9.1 Object conversion lists for all Stix dialects

| Dialect        | File URL                                               |
|:--------------|:--------------------------------------------------------|	
| "STIX 2.1"      | `https://raw.githubusercontent.com/os-threat/Stix-ORM/refs/heads/main/stixorm/module/definitions/stix21/mappings/object_conversion.json` |
| "OS-Threat" | `https://raw.githubusercontent.com/os-threat/Stix-ORM/refs/heads/main/stixorm/module/definitions/os_threat/mappings/object_conversion.json` |
| "MITRE ATT&CK" | `https://raw.githubusercontent.com/os-threat/Stix-ORM/refs/heads/main/stixorm/module/definitions/attack/mappings/object_conversion.json` |
|
| "OCA" | `https://raw.githubusercontent.com/os-threat/Stix-ORM/refs/heads/main/stixorm/module/definitions/oca/mappings/object_conversion.json` |
| "MBC" | `https://raw.githubusercontent.com/os-threat/Stix-ORM/refs/heads/main/stixorm/module/definitions/mbc/mappings/object_conversion.json` |
| "Attack-Flow" | `https://raw.githubusercontent.com/os-threat/Stix-ORM/refs/heads/main/stixorm/module/definitions/attack_flow/mappings/object_conversion.json` |

## 10. The Python Block Needs to Import the Correct Classes

When creating a Python block that uses subobjects or extensions, copilot must ensure that the correct classes for these two are imported at the top of the block, in addition to the main class for the Stix object.

By using the above object conversion lists, copilot can convert the name from the class template to the correct Class Names for each extension to be used in the block, and add the appropriate import statements.

The Python Classes for the sub objects is given in both the EmbeddedObjectProperty `property` field in the class template, and the `sub` key in the class template definition, and the copilot can use those names directly in the import statements.