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
