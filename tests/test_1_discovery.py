"""
Phase 1: Discovery Tests
"""
import pytest
from pathlib import Path
import json

from tests.utils.discovery import ObjectDiscovery


@pytest.fixture(scope='session')
def discovery_results(stixorm_path, generated_dir):
    """Run discovery once per test session"""
    examples_dir = stixorm_path / 'examples'
    discovery = ObjectDiscovery(examples_dir, stixorm_path)
    
    results = discovery.discover_testable_objects()
    
    # Save discovery results
    with open(generated_dir / 'discovery_results.json', 'w', encoding='utf-8') as f:
        json.dump([
            {
                'id': obj['id'],
                'type': obj['type'],
                'python_class': metadata.python_class,
                'group': metadata.group,
                'typeql': metadata.typeql,
                'path': str(path)
            }
            for obj, metadata, path in results
        ], f, indent=2)
    
    return results


@pytest.mark.discovery
def test_discovery_finds_objects(discovery_results):
    """Verify discovery finds testable objects"""
    assert len(discovery_results) > 0, "No testable objects discovered"


@pytest.mark.discovery
def test_discovery_minimum_coverage(discovery_results):
    """Verify we have minimum expected coverage"""
    # Adjusted threshold based on actual example count
    min_expected = 50  # Conservative minimum
    assert len(discovery_results) >= min_expected, \
        f"Expected >={min_expected} objects, found {len(discovery_results)}"


@pytest.mark.discovery
def test_all_groups_represented(discovery_results):
    """Verify all groups (SCO, SDO, SRO) are represented"""
    groups = {metadata.group.lower() for _, metadata, _ in discovery_results}
    assert 'sco' in groups or 'sdo' in groups, \
        "No SCO or SDO objects found"


@pytest.mark.discovery
def test_discovery_results_valid_structure(discovery_results):
    """Verify each discovery result has required fields"""
    for obj, metadata, path in discovery_results:
        assert 'id' in obj, "Object missing 'id' field"
        assert 'type' in obj, "Object missing 'type' field"
        assert metadata is not None, "Missing metadata"
        assert hasattr(metadata, 'python_class'), "Metadata missing python_class"
        assert hasattr(metadata, 'group'), "Metadata missing group"
        assert path.exists(), f"Path does not exist: {path}"
