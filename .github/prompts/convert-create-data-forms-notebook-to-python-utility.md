# Refactor the create data forms from stix data objects using class templates from a notebook to extract a python utility

Read [the notebook](../../Orchestration/Convert_Examples_to_DataForms.ipynb) to understand how class templates define the structure of STIX objects and how data forms are created from Stix json data objects based on those templates.

We want to refactor out the logic that creates data forms from a Stix object list into a reusable python utility function that can be called from anywhere in the codebase. There are two modes of operation:

1. Mode 1: Fill StixORM directory: Create data forms from a list of stix data objects, and save them to the appropriate StixORM directory based on object type. In this mode it will return a report of the created data forms.
2. Mode 2: Fill a nominated "test" directory: Create data forms from a list of stix data objects, and save them to the appropriate "test" directory based on a second input parameter. In this mode it will collect comprehensive documentation on every reference deleted for each object to enable you to reconstitute the full object later for testing purposes. It will return a dict containing the report and a list containing the dicts describing all deleted references, and their field names for each object. Ideally you order the input list by dependencies so that objects that are referenced by others come first. It is important to retain this order and the specific names of each data form made, so that you can later reconstitute the full objects with references intact, with embedded refences pointing to objects with the same information in them.

The signature of the function should be:

```python
def create_data_forms_from_stix_objects(
	stix_objects: List[Dict],
	test_directory: Optional[str] = None
) -> Dict:
```

The file should be called "convert_object_list_to_data_forms.py" and be placed in the Orchestration\Utilities directory. Please place the documentation here too.

Make sure you provide full documentation for the function, and that it handles all the requirements for creating data forms as described in the notebook, check this against the prompt specification here (.github/prompts/create-data-forms.md).

Then change the notebook to call this utility function instead of having the logic inline in the notebook.

Finally, delete then generated files from the temp_method_comparison and run the expanded tests to compare the new utility capability to the prompt-driven notebook approach, and ensure they produce identical results.

For the moment, use a static function that takes an object and returns the object's directory based on its type. This can initially use the fixed inventory below, but later on we can enhance it to use a dynamic decision making process

```python
def get_stix_type_mapping():
    """Map STIX types to their expected directory structure"""
    
    # Load the inventory from the documentation
    inventory = {
        # SDO types (currently implemented)
        'identity': 'SDO/Identity',
        'indicator': 'SDO/Indicator', 
        'impact': 'SDO/Impact',
        'incident': 'SDO/Incident',
        'event': 'SDO/Event',
        'observed-data': 'SDO/Observed_Data',
        'sequence': 'SDO/Sequence',
        'task': 'SDO/Task',
        
        # SCO types (currently implemented)
        'anecdote': 'SCO/Anecdote',
        'email-addr': 'SCO/Email_Addr',
        'user-account': 'SCO/User_Account',
        'url': 'SCO/URL',
        'email-message': 'SCO/Email_Message',
        
        # SRO types (currently implemented)
        'relationship': 'SRO/Relationship',
        'sighting': 'SRO/Sighting',
        
        # Standard STIX 2.1 SDO types (templates exist)
        'attack-pattern': 'SDO/Attack_Pattern',
        'campaign': 'SDO/Campaign',
        'course-of-action': 'SDO/Course_of_Action',
        'grouping': 'SDO/Grouping',
        'infrastructure': 'SDO/Infrastructure',
        'intrusion-set': 'SDO/Instrusion_Set',
        'location': 'SDO/Location',
        'malware-analysis': 'SDO/Malware_Analysis',
        'note': 'SDO/Note',
        'opinion': 'SDO/Opinion',
        'report': 'SDO/Report',
        'threat-actor': 'SDO/Threat_Actor',
        'vulnerability': 'SDO/Vulnerability',
        
        # Standard STIX 2.1 SCO types (templates exist)
        'artifact': 'SCO/Artifact',
        'autonomous-system': 'SCO/Autonomous_System',
        'directory': 'SCO/Directory',
        'domain-name': 'SCO/Domain_Name',
        'file': 'SCO/File',
        'ipv4-addr': 'SCO/IPv4_Addr',
        'ipv6-addr': 'SCO/IPv6_Addr',
        'mac-addr': 'SCO/MAC_Address',
        'mutex': 'SCO/Mutex',
        'software': 'SCO/Software',
        'x509-certificate': 'SCO/X509_Cert'
    }
    
    return inventory
	```