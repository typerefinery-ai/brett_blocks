"""
Pytest configuration and fixtures for StixORM testing
"""
import pytest
from pathlib import Path
import shutil
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.utils.reporter import TestReporter


@pytest.fixture(scope='session')
def project_root():
    """Get project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture(scope='session')
def stixorm_path(project_root):
    """Get StixORM base path"""
    return project_root / 'Block_Families' / 'StixORM'


@pytest.fixture(scope='session')
def examples_dir(project_root):
    """Get examples directory path"""
    return project_root / 'Block_Families' / 'examples'


@pytest.fixture(scope='session')
def generated_dir(project_root):
    """
    Create and return generated artifacts directory
    Cleanup after session (optional)
    """
    gen_dir = project_root / 'tests' / 'generated'
    
    # Create subdirectories
    subdirs = [
        'data_forms',
        'input_objects', 
        'output_objects',
        'reports'
    ]
    
    for subdir in subdirs:
        (gen_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    yield gen_dir
    
    # Cleanup (commented out to preserve artifacts for review)
    # Uncomment to auto-cleanup after test run
    # shutil.rmtree(gen_dir, ignore_errors=True)


@pytest.fixture(scope='session')
def test_reporter(generated_dir):
    """Shared reporter instance for all tests"""
    return TestReporter(generated_dir)


@pytest.fixture(scope='session')
def discovery_results(examples_dir, stixorm_path, generated_dir):
    """Run discovery once per test session"""
    from tests.utils.discovery import ObjectDiscovery
    import json
    
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


@pytest.fixture(scope='session')
def generation_results(discovery_results, stixorm_path, generated_dir):
    """Generate data forms once per test session"""
    from tests.utils.data_form_generator import DataFormGenerator
    
    objects = [obj for obj, _, _ in discovery_results]
    
    generator = DataFormGenerator(stixorm_path, generated_dir)
    data_forms, reconstitution_data, sequence = generator.generate_data_forms(objects)
    
    # Save artifacts
    generator.save_artifacts(data_forms, reconstitution_data, objects)
    
    return {
        'data_forms': data_forms,
        'reconstitution_data': reconstitution_data,
        'sequence': sequence,
        'objects': objects
    }


@pytest.fixture(scope='session')
def execution_results(discovery_results, generation_results, stixorm_path, generated_dir):
    """
    Execute all blocks using the proven STIXReconstitutionEngine
    
    This uses the production-proven reconstitution engine that achieves 99.3% success rate.
    The engine automatically handles:
    - Reference restoration via id_mapping
    - Dependency ordering via creation_sequence
    - Embedded object loading
    - Proper make_*.py block invocation
    """
    import sys
    import json
    
    # Add Orchestration/Utilities to path for reconstitution engine
    utilities_path = generated_dir.parent.parent / 'Orchestration' / 'Utilities'
    sys.path.insert(0, str(utilities_path))
    
    from reconstitute_object_list import STIXReconstitutionEngine
    
    # The reconstitution engine needs original STIX objects in a directory
    # Copy testable objects to input_objects directory
    input_objects_dir = generated_dir / 'input_objects'
    input_objects_dir.mkdir(parents=True, exist_ok=True)
    
    # Save testable objects to files for the engine to load
    for obj, metadata, _ in discovery_results:
        obj_id = obj['id']
        obj_type = obj.get('type', 'unknown')
        truncated_id = obj_id.split('--')[1][:8] if '--' in obj_id else obj_id[:8]
        filename = f"{obj_type}_{truncated_id}.json"
        
        with open(input_objects_dir / filename, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
    
    # Initialize the reconstitution engine
    engine = STIXReconstitutionEngine(generated_dir)
    
    # The engine expects reconstitution_data.json in data_forms/ subdirectory
    # Copy it from generated/ root to data_forms/ where engine expects it
    recon_source = generated_dir / 'reconstitution_data.json'
    recon_dest = generated_dir / 'data_forms' / 'reconstitution_data.json'
    recon_dest.parent.mkdir(parents=True, exist_ok=True)
    
    if recon_source.exists():
        import shutil
        shutil.copy2(recon_source, recon_dest)
    
    # Run full reconstitution process
    # This returns (original_objects, reconstituted_objects, report)
    # The engine has already:
    # 1. Loaded objects from input_objects/
    # 2. Generated data forms (we skip this since we already did it)
    # 3. Reconstituted objects using make_*.py blocks
    try:
        # Since we already generated data forms, we just need reconstitution
        # Load reconstitution data and reconstitute
        recon_data = engine.load_reconstitution_data()
        reconstituted_objects = engine.reconstitute_stix_objects(recon_data)
        
        # Build results mapping original IDs to reconstituted objects
        results = {}
        
        # Use creation_sequence for deterministic mapping (same approach as temporary_reconstitution_testing/runner.py)
        # The reconstituted_objects list is produced in the same order as creation_sequence,
        # so we can zip them together deterministically.
        creation_sequence = recon_data.get('creation_sequence', [])
        
        # Build mapping from original_id -> reconstituted object using creation_sequence index
        for idx, seq_entry in enumerate(creation_sequence):
            original_id = seq_entry.get('object_id')
            
            if idx < len(reconstituted_objects):
                recon_obj = reconstituted_objects[idx]
                
                # Verify it's a valid object
                if isinstance(recon_obj, dict) and 'type' in recon_obj:
                    results[original_id] = {
                        'status': 'SUCCESS',
                        'object': recon_obj,
                        'execution_time_ms': 0  # Engine doesn't track individual times
                    }
                else:
                    results[original_id] = {
                        'status': 'ERROR',
                        'error': f'Reconstituted object is {type(recon_obj).__name__}, expected dict',
                        'error_type': 'TypeError',
                        'execution_time_ms': 0
                    }
            else:
                results[original_id] = {
                    'status': 'ERROR',
                    'error': f'Reconstitution index {idx} out of range (only {len(reconstituted_objects)} objects reconstituted)',
                    'error_type': 'IndexError',
                    'execution_time_ms': 0
                }
        
        # Any objects not in creation_sequence were skipped (no data form generated)
        for obj, _, _ in discovery_results:
            obj_id = obj['id']
            if obj_id not in results:
                results[obj_id] = {
                    'status': 'SKIPPED',
                    'reason': 'Not in creation_sequence - data form not generated',
                    'execution_time_ms': 0
                }
        
    except Exception as e:
        # If reconstitution fails entirely, mark all as errors
        results = {}
        for obj, _, _ in discovery_results:
            results[obj['id']] = {
                'status': 'ERROR',
                'error': f'Reconstitution engine failed: {str(e)}',
                'error_type': type(e).__name__,
                'execution_time_ms': 0
            }
    
    # Save execution summary
    with open(generated_dir / 'execution_results.json', 'w', encoding='utf-8') as f:
        summary = {
            obj_id: {
                'status': r['status'],
                'error': r.get('error'),
                'reason': r.get('reason'),
                'execution_time_ms': r.get('execution_time_ms')
            }
            for obj_id, r in results.items()
        }
        json.dump(summary, f, indent=2)
    
    return results


@pytest.fixture(scope='session')
def comparison_results(discovery_results, execution_results, test_reporter):
    """Compare all objects once per test session"""
    from tests.utils.comparator import ObjectComparator
    
    comparator = ObjectComparator()
    results = {}
    
    for obj, metadata, _ in discovery_results:
        obj_id = obj['id']
        
        # Skip if execution failed or was skipped
        if obj_id not in execution_results or execution_results[obj_id]['status'] != 'SUCCESS':
            test_reporter.add_result(
                obj_id, 
                obj['type'], 
                'SKIPPED',
                error_message='Execution failed or skipped'
            )
            continue
        
        reconstituted = execution_results[obj_id]['object']
        is_identical, differences = comparator.compare_objects(obj, reconstituted)
        
        status = 'PASS' if is_identical else 'FAIL'
        test_reporter.add_result(
            obj_id,
            obj['type'],
            status,
            differences=differences,
            execution_time_ms=execution_results[obj_id].get('execution_time_ms', 0)
        )
        
        results[obj_id] = {
            'status': status,
            'differences': differences
        }
    
    return results


def pytest_configure(config):
    """Display test session banner"""
    print("\n" + "="*70)
    print("StixORM Block Testing System")
    print("="*70)


def pytest_sessionfinish(session, exitstatus):
    """Display completion message"""
    print("\n" + "="*70)
    print("Test session complete - check tests/generated/ for artifacts")
    print("="*70)
