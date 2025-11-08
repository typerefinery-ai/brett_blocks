#!/usr/bin/env python3
"""
Example usage of the STIX Object Reconstitution and Notebook Generation system

Demonstrates both operational modes:
1. Test mode: Reconstitute and validate objects
2. Notebook mode: Generate executable notebooks for creating objects in context
"""

import json
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Orchestration.Utilities.reconstitute_and_generate_notebooks import reconstitute_and_generate


def example_test_mode():
    """
    Example 1: Test Mode
    
    Reconstitute STIX objects from data forms for validation testing.
    This is useful for verifying round-trip conversion works correctly.
    """
    print("=" * 70)
    print("EXAMPLE 1: TEST MODE - Reconstitute objects for validation")
    print("=" * 70)
    
    results = reconstitute_and_generate(
        mode='test',
        data_forms_dir=Path('temporary_reconstitution_testing/generated/data_forms'),
        reconstitution_data_file=Path('temporary_reconstitution_testing/generated/data_forms/reconstitution_data.json'),
        output_dir=Path('temporary_reconstitution_testing/generated/reconstituted')
    )
    
    print(f"\n✅ Test Mode Results:")
    print(f"   Success: {results['success']}")
    print(f"   Files generated: {len(results.get('generated_files', []))}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    return results


def example_notebook_mode_user_context():
    """
    Example 2: Notebook Mode - User Context
    
    Generate a notebook that creates user identity objects and saves to user context.
    Similar to Step_0_User_Setup.ipynb
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: NOTEBOOK MODE - User context setup")
    print("=" * 70)
    
    # Load example user objects
    user_objects = [
        # Example: Load from examples directory or create programmatically
        {
            "type": "identity",
            "spec_version": "2.1",
            "id": "identity--" + "a" * 36,  # Placeholder
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Example User",
            "identity_class": "individual"
        },
        {
            "type": "user-account",
            "spec_version": "2.1",
            "id": "user-account--" + "b" * 36,
            "user_id": "example_user",
            "account_login": "example_user"
        },
        {
            "type": "email-addr",
            "spec_version": "2.1",
            "id": "email-addr--" + "c" * 36,
            "value": "example@company.com"
        }
    ]
    
    results = reconstitute_and_generate(
        mode='notebook',
        stix_objects=user_objects,
        notebook_name='Generated_User_Setup',
        context_type='user',
        notebook_title='User Context Setup',
        notebook_description='Auto-generated notebook to create user identity and save to user context'
    )
    
    print(f"\n✅ Notebook Mode Results:")
    print(f"   Success: {results['success']}")
    print(f"   Notebook path: {results.get('notebook_path', 'N/A')}")
    print(f"   Data forms created: {results.get('data_forms_created', 0)}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    return results


def example_notebook_mode_incident_context():
    """
    Example 3: Notebook Mode - Incident Context
    
    Generate a notebook that creates incident evidence objects and saves to incident context.
    Similar to Step_2_Create_Incident_with_an_Alert.ipynb
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: NOTEBOOK MODE - Incident context with phishing evidence")
    print("=" * 70)
    
    # Load phishing incident objects from examples
    examples_dir = Path('Block_Families/examples')
    
    # Try to load real examples
    incident_objects = []
    
    # Load email addresses
    email_files = list(examples_dir.glob('**/email*.json'))
    for email_file in email_files[:3]:  # Limit to 3 examples
        try:
            with open(email_file) as f:
                obj = json.load(f)
                if isinstance(obj, dict) and 'type' in obj:
                    incident_objects.append(obj)
                elif isinstance(obj, list):
                    incident_objects.extend([o for o in obj if isinstance(o, dict) and 'type' in o])
        except:
            pass
    
    # Load incident object if exists
    incident_files = list(examples_dir.glob('**/incident*.json'))
    for inc_file in incident_files[:1]:
        try:
            with open(inc_file) as f:
                obj = json.load(f)
                if isinstance(obj, dict) and 'type' in obj:
                    incident_objects.append(obj)
        except:
            pass
    
    if not incident_objects:
        print("⚠️  No example objects found, using placeholders")
        incident_objects = [
            {
                "type": "incident",
                "spec_version": "2.1",
                "id": "incident--" + "d" * 36,
                "created": "2023-01-01T00:00:00.000Z",
                "modified": "2023-01-01T00:00:00.000Z",
                "name": "Phishing Investigation"
            }
        ]
    
    results = reconstitute_and_generate(
        mode='notebook',
        stix_objects=incident_objects,
        notebook_name='Generated_Phishing_Incident',
        context_type='incident',
        notebook_title='Phishing Incident Investigation',
        notebook_description='Auto-generated notebook to document phishing evidence and save to incident context'
    )
    
    print(f"\n✅ Notebook Mode Results:")
    print(f"   Success: {results['success']}")
    print(f"   Notebook path: {results.get('notebook_path', 'N/A')}")
    print(f"   Data forms created: {results.get('data_forms_created', 0)}")
    print(f"   Objects processed: {len(incident_objects)}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    return results


def example_notebook_mode_company_context():
    """
    Example 4: Notebook Mode - Company Context
    
    Generate a notebook that creates company infrastructure objects.
    Similar to Step_1_Company_Setup.ipynb
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: NOTEBOOK MODE - Company context with infrastructure")
    print("=" * 70)
    
    # Load company infrastructure examples
    examples_dir = Path('Block_Families/examples')
    
    company_objects = []
    
    # Load identities (company)
    identity_files = list(examples_dir.glob('**/identity*.json'))
    for id_file in identity_files[:2]:
        try:
            with open(id_file) as f:
                data = json.load(f)
                if isinstance(data, dict) and 'type' in data:
                    company_objects.append(data)
                elif isinstance(data, list):
                    company_objects.extend([o for o in data if isinstance(o, dict) and 'type' in o])
        except:
            pass
    
    if not company_objects:
        print("⚠️  No example objects found, using placeholders")
        company_objects = [
            {
                "type": "identity",
                "spec_version": "2.1",
                "id": "identity--" + "e" * 36,
                "created": "2023-01-01T00:00:00.000Z",
                "modified": "2023-01-01T00:00:00.000Z",
                "name": "Example Company",
                "identity_class": "organization"
            }
        ]
    
    results = reconstitute_and_generate(
        mode='notebook',
        stix_objects=company_objects,
        notebook_name='Generated_Company_Setup',
        context_type='company',
        notebook_title='Company Infrastructure Setup',
        notebook_description='Auto-generated notebook to create company infrastructure and save to company context'
    )
    
    print(f"\n✅ Notebook Mode Results:")
    print(f"   Success: {results['success']}")
    print(f"   Notebook path: {results.get('notebook_path', 'N/A')}")
    print(f"   Data forms created: {results.get('data_forms_created', 0)}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    return results


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("STIX RECONSTITUTION & NOTEBOOK GENERATION - EXAMPLES")
    print("=" * 70)
    print("\nThis script demonstrates both operational modes:")
    print("  1. Test mode: Validate round-trip object conversion")
    print("  2. Notebook mode: Generate executable notebooks for context creation")
    print()
    
    # Run examples based on command line args
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'test':
            example_test_mode()
        elif mode == 'user':
            example_notebook_mode_user_context()
        elif mode == 'incident':
            example_notebook_mode_incident_context()
        elif mode == 'company':
            example_notebook_mode_company_context()
        elif mode == 'all':
            example_test_mode()
            example_notebook_mode_user_context()
            example_notebook_mode_incident_context()
            example_notebook_mode_company_context()
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python example_usage.py [test|user|incident|company|all]")
    else:
        print("Usage: python example_usage.py [test|user|incident|company|all]")
        print("\nRun 'python example_usage.py all' to see all examples")
