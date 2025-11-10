# StixORM Testing System Design

**Document Version:** 1.0  
**Created:** 2025-11-10  
**Status:** 🎯 Ready for Implementation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Directory Structure](#directory-structure)
4. [Core Modules](#core-modules)
5. [Test Pipeline](#test-pipeline)
6. [Pytest Configuration](#pytest-configuration)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Success Criteria](#success-criteria)
9. [Known Limitations and Edge Cases](#known-limitations-and-edge-cases)
10. [Future Enhancements](#future-enhancements)
11. [Appendix: Integration with Existing Utilities](#appendix-integration-with-existing-utilities)

---

## Overview

### Purpose

This testing system validates all StixORM blocks by executing a complete round-trip conversion:
1. STIX Objects → Data Forms (conversion)
2. Data Forms → STIX Objects (reconstitution via make_*.py blocks)
3. Original vs Reconstituted (verification)

### Goals

- **Comprehensive Coverage**: Test all STIX objects with corresponding make_*.py blocks (target: >95%)
- **High Pass Rate**: Achieve >90% pass rate on first run
- **Robust Error Handling**: Gracefully handle failures without stopping test suite
- **Clear Reporting**: Provide actionable JSON and Markdown reports
- **Maintainability**: Modular, extensible architecture

### Integration with Existing System

Leverages proven utilities:
- `Orchestration/Utilities/convert_object_list_to_data_forms.py` - Data form generation (99.3% success rate)
- `Orchestration/Utilities/reconstitute_object_list.py` - Reference restoration
- `Block_Families/General/_library/parse.py` - ParseContent metadata

### Environment Management

The testing system uses the existing **Poetry** environment defined in `pyproject.toml`:
- All dependencies (`pytest`, `deepdiff`) are managed by Poetry
- Tests run via `poetry run pytest` or provided runner scripts
- No separate pip installations required
- Consistent Python environment across development and testing

---

## Architecture

### 5-Phase Test Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                         StixORM Testing Pipeline                     │
└─────────────────────────────────────────────────────────────────────┘

Phase 1: Discovery
┌──────────────────────────────────────────────────────────────────┐
│ Input: Block_Families/StixORM/examples/*.json                    │
│ Process: Load all STIX objects, filter for testable objects     │
│ Output: tests/stixorm/fixtures/testable_objects.json            │
└──────────────────────────────────────────────────────────────────┘
                                ↓
Phase 2: Data Form Generation
┌──────────────────────────────────────────────────────────────────┐
│ Input: testable_objects.json                                     │
│ Process: Convert to data forms using existing utilities          │
│ Output: generated/{data_forms/, input_objects/,                  │
│         reconstitution_data.json}                                │
└──────────────────────────────────────────────────────────────────┘
                                ↓
Phase 3: Block Execution
┌──────────────────────────────────────────────────────────────────┐
│ Input: data_forms/, reconstitution_data.json                     │
│ Process: Restore references, invoke make_*.py blocks             │
│ Output: generated/output_objects/, execution_results.json        │
└──────────────────────────────────────────────────────────────────┘
                                ↓
Phase 4: Verification
┌──────────────────────────────────────────────────────────────────┐
│ Input: input_objects/, output_objects/                           │
│ Process: DeepDiff comparison with UUID normalization             │
│ Output: verification_results.json                                │
└──────────────────────────────────────────────────────────────────┘
                                ↓
Phase 5: Reporting
┌──────────────────────────────────────────────────────────────────┐
│ Input: All results JSON files                                    │
│ Process: Generate summary statistics                             │
│ Output: test_summary.json, test_summary.md                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
tests/
├── stixorm/
│   ├── conftest.py              # Pytest fixtures and configuration
│   ├── pytest.ini               # Pytest settings
│   ├── README.md                # Testing documentation
│   │
│   ├── utils/                   # Reusable testing utilities
│   │   ├── __init__.py
│   │   ├── discovery.py         # Object discovery and filtering
│   │   ├── data_form_generator.py  # Data form generation wrapper
│   │   ├── block_executor.py    # Block invocation logic
│   │   ├── comparator.py        # DeepDiff comparison with normalization
│   │   └── reporter.py          # Report generation
│   │
│   ├── fixtures/                # Test fixtures and reference data
│   │   └── testable_objects.json  # Discovered testable objects
│   │
│   ├── generated/               # Generated test artifacts (gitignored)
│   │   ├── data_forms/          # Generated data forms
│   │   ├── input_objects/       # Original STIX objects
│   │   ├── output_objects/      # Reconstituted STIX objects
│   │   ├── reconstitution_data.json  # Reference restoration metadata
│   │   ├── execution_results.json    # Block execution results
│   │   ├── verification_results.json # Comparison results
│   │   ├── test_summary.json    # Summary statistics (JSON)
│   │   └── test_summary.md      # Summary report (Markdown)
│   │
│   └── test_1_discovery.py           # Object discovery tests
│       test_2_data_form_generation.py # Data form generation tests
│       test_3_block_execution.py      # Block execution tests
│       test_4_verification.py         # Object verification tests
│       test_5_reporting.py            # Report generation tests
│
└── os_triage/                   # OS_Triage testing (future)
    ├── conftest.py              # Placeholder
    ├── fixtures/                # Placeholder
    └── README.md                # TODO documentation
```

---


## Core Modules

### 1. Discovery Module (`utils/discovery.py`)

**Purpose:** Load and filter STIX objects to identify testable ones

```python
class ObjectDiscovery:
    """Discover testable STIX objects from examples directory"""
    
    def __init__(self, examples_dir: Path, stixorm_base: Path):
        self.examples_dir = Path(examples_dir)
        self.stixorm_base = Path(stixorm_base)
    
    def load_all_stix_objects(self) -> List[Dict[str, Any]]:
        """Load all STIX objects from examples/*.json files"""
        all_objects = []
        for json_file in self.examples_dir.glob("*.json"):
            with open(json_file, 'r') as f:
                objects = json.load(f)
                if isinstance(objects, list):
                    all_objects.extend(objects)
                else:
                    all_objects.append(objects)
        return all_objects
    
    def is_testable(self, stix_obj: Dict[str, Any]) -> Tuple[bool, Any, Path]:
        """
        Check if object has corresponding make_*.py block
        
        Process:
        1. Get ParseContent metadata using get_parse_content_for_object()
        2. Construct object path from metadata.group and metadata.python_class
        3. Check for make_*.py file in object directory
        
        Returns:
            (is_testable, metadata, object_path)
        """
        metadata = get_parse_content_for_object(stix_obj)
        if metadata is None:
            return False, None, None
        
        group_dir = metadata.group.upper()  # SCO, SDO, SRO
        object_path = self.stixorm_base / group_dir / metadata.python_class
        
        # Check for make_*.py files
        py_files = list(object_path.glob("make_*.py"))
        if py_files:
            return True, metadata, object_path
        return False, None, None
    
    def discover_testable_objects(self) -> List[Tuple[Dict, Any, Path]]:
        """Main discovery function - returns list of (object, metadata, path)"""
        all_objects = self.load_all_stix_objects()
        testable = []
        
        for obj in all_objects:
            is_test, metadata, path = self.is_testable(obj)
            if is_test:
                testable.append((obj, metadata, path))
        
        return testable
```

**Key Features:**
- Scans all example JSON files
- Uses ParseContent for dynamic metadata lookup
- Filters objects without corresponding blocks
- Returns structured data for downstream phases

---

### 2. Data Form Generator (`utils/data_form_generator.py`)

**Purpose:** Thin wrapper around existing data form generation utilities

```python
class DataFormGenerator:
    """Generate data forms from STIX objects"""
    
    def __init__(self, stixorm_path: Path, output_dir: Path):
        self.stixorm_path = Path(stixorm_path)
        self.output_dir = Path(output_dir)
    
    def generate_data_forms(
        self, 
        stix_objects: List[Dict[str, Any]]
    ) -> Tuple[Dict, Dict, List]:
        """
        Generate data forms using existing utility
        
        Calls: create_data_forms_from_stix_objects() from 
               convert_object_list_to_data_forms.py
               
        Returns:
            (data_forms_dict, reconstitution_data, creation_sequence)
        """
        from Orchestration.Utilities.convert_object_list_to_data_forms import (
            create_data_forms_from_stix_objects
        )
        
        return create_data_forms_from_stix_objects(
            stix_objects,
            self.stixorm_path,
            self.output_dir
        )
    
    def save_artifacts(self, data_forms, reconstitution_data, stix_objects):
        """Save generated artifacts to appropriate directories"""
        # Save data forms to generated/data_forms/
        for form_name, form_data in data_forms.items():
            form_file = self.output_dir / 'data_forms' / f"{form_name}.json"
            with open(form_file, 'w') as f:
                json.dump(form_data, f, indent=2)
        
        # Save input objects to generated/input_objects/
        for obj in stix_objects:
            obj_file = self.output_dir / 'input_objects' / f"{obj['id']}.json"
            with open(obj_file, 'w') as f:
                json.dump(obj, f, indent=2)
        
        # Save reconstitution_data.json
        with open(self.output_dir / 'reconstitution_data.json', 'w') as f:
            json.dump(reconstitution_data, f, indent=2)
```

**Key Features:**
- Reuses proven conversion logic (99.3% success rate)
- Organizes outputs into structured directories
- Preserves all metadata for reconstitution

---

### 3. Block Executor (`utils/block_executor.py`)

**Purpose:** Invoke make_*.py blocks with properly prepared inputs

```python
class BlockExecutor:
    """Execute StixORM blocks with reference restoration"""
    
    def __init__(
        self, 
        stixorm_path: Path, 
        data_forms_dir: Path, 
        output_dir: Path
    ):
        self.stixorm_path = Path(stixorm_path)
        self.data_forms_dir = Path(data_forms_dir)
        self.output_dir = Path(output_dir)
        self.reconstituted_objects = {}  # Cache for dependency resolution
    
    def execute_block(
        self, 
        stix_obj: Dict, 
        metadata: Any, 
        reconstitution_data: Dict
    ) -> Dict[str, Any]:
        """
        Execute a single block
        
        Process:
        1. Load data form from data_forms_dir
        2. Get reference info from reconstitution_data
        3. Restore references to data form
        4. Load embedded objects as inputs
        5. Dynamically import and call make_*.py block
        6. Save output
        7. Cache result for dependency resolution
        
        Returns:
            Reconstituted STIX object
        """
        # 1. Find and load data form
        data_form = self._load_data_form(stix_obj['id'])
        
        # 2. Get reference restoration info
        ref_info = self._get_ref_info(stix_obj['id'], reconstitution_data)
        
        # 3. Restore references
        from Orchestration.Utilities.reconstitute_object_list import restore_references_to_data_form
        restored_form = restore_references_to_data_form(
            data_form, 
            ref_info, 
            {}  # id_mapping for new UUIDs
        )
        
        # 4. Load embedded objects as inputs
        embedded_inputs = self._load_embedded_objects(ref_info)
        
        # 5. Dynamically import and call block
        result = self._invoke_make_block(
            metadata, 
            restored_form, 
            embedded_inputs
        )
        
        # 6. Save and cache
        self._save_output(stix_obj['id'], metadata, result)
        self.reconstituted_objects[stix_obj['id']] = result
        
        return result
    
    def _invoke_make_block(
        self, 
        metadata: Any, 
        data_form: Dict, 
        embedded_inputs: Dict
    ) -> Dict:
        """
        Dynamically import and invoke make_*.py block
        
        Uses importlib to load module based on metadata.python_class
        Constructs input JSON structure expected by block's main() function
        """
        import importlib
        
        # Construct module path
        group_dir = metadata.group.upper()
        module_path = f"Block_Families.StixORM.{group_dir}.{metadata.python_class}.make_{metadata.typeql.replace('-', '_')}"
        
        # Import module
        module = importlib.import_module(module_path)
        
        # Prepare input structure
        input_data = {
            f"{metadata.typeql}_form": data_form,
            **embedded_inputs  # Add embedded objects
        }
        
        # Create temp input file
        input_file = self.data_forms_dir / f"temp_input_{metadata.typeql}.json"
        output_file = self.output_dir / f"temp_output_{metadata.typeql}.json"
        
        with open(input_file, 'w') as f:
            json.dump(input_data, f)
        
        # Call block's main() function
        module.main(str(input_file), str(output_file))
        
        # Load result
        with open(output_file, 'r') as f:
            result = json.load(f)
        
        # Cleanup temp files
        input_file.unlink()
        output_file.unlink()
        
        # Extract object from result (blocks return {type: [obj]})
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, list) and value:
                    return value[0]
        
        return result
    
    def _load_embedded_objects(self, ref_info: Dict) -> Dict:
        """Load embedded reference objects from cache or data forms"""
        embedded = {}
        
        for ref_id in ref_info.get('embedded_references', []):
            if ref_id in self.reconstituted_objects:
                embedded[ref_id] = self.reconstituted_objects[ref_id]
        
        return embedded
    
    def _load_data_form(self, object_id: str) -> Dict:
        """Load data form for object ID"""
        # Implementation to find and load data form
        pass
    
    def _get_ref_info(self, object_id: str, reconstitution_data: Dict) -> Dict:
        """Get reference info for object from reconstitution data"""
        # Implementation to extract reference info
        pass
    
    def _save_output(self, object_id: str, metadata: Any, result: Dict):
        """Save reconstituted object to output directory"""
        output_file = self.output_dir / f"{metadata.typeql}_{object_id}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
```

**Key Features:**
- Dynamic module import based on metadata
- Reference restoration using existing utilities
- Dependency resolution through caching
- Proper input structure for blocks

---

### 4. Comparator Module (`utils/comparator.py`)

**Purpose:** Compare original and reconstituted objects with normalization

```python
class ObjectComparator:
    """Compare STIX objects using DeepDiff with normalization"""
    
    def __init__(self):
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
        """
        import copy
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
        
        Returns:
            (is_identical, differences_dict)
        """
        from deepdiff import DeepDiff
        
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
```

**Key Features:**
- Handles UUID differences
- Normalizes reference lists
- Supports sequence-specific fields
- Returns structured diff for reporting

---

### 5. Reporter Module (`utils/reporter.py`)

**Purpose:** Generate comprehensive test reports

```python
class TestReporter:
    """Generate JSON and Markdown test reports"""
    
    def __init__(self, generated_dir: Path):
        self.generated_dir = Path(generated_dir)
        self.results = []
    
    def add_result(
        self, 
        object_id: str, 
        object_type: str,
        status: str,  # PASS, FAIL, ERROR, SKIPPED
        differences: Dict = None,
        execution_time_ms: float = 0,
        error_message: str = None
    ):
        """Add a test result"""
        self.results.append({
            'object_id': object_id,
            'object_type': object_type,
            'status': status,
            'differences': differences or {},
            'execution_time_ms': execution_time_ms,
            'error_message': error_message,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics
        
        Returns:
            {
                'total_objects': int,
                'passed': int,
                'failed': int,
                'errors': int,
                'pass_rate': float,
                'by_type': {type: {total, passed, failed, errors}},
                'failures': [list of failed objects]
            }
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')
        
        # Aggregate by type
        by_type = {}
        for result in self.results:
            obj_type = result['object_type']
            if obj_type not in by_type:
                by_type[obj_type] = {
                    'total': 0, 'passed': 0, 'failed': 0, 'errors': 0
                }
            by_type[obj_type]['total'] += 1
            if result['status'] == 'PASS':
                by_type[obj_type]['passed'] += 1
            elif result['status'] == 'FAIL':
                by_type[obj_type]['failed'] += 1
            elif result['status'] == 'ERROR':
                by_type[obj_type]['errors'] += 1
        
        return {
            'total_objects': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'by_type': by_type,
            'failures': [r for r in self.results if r['status'] in ['FAIL', 'ERROR']]
        }
    
    def save_reports(self):
        """Save JSON and Markdown reports"""
        # Save detailed results
        with open(self.generated_dir / 'test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save summary
        summary = self.generate_summary()
        with open(self.generated_dir / 'test_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Generate markdown
        self._generate_markdown_report(summary)
    
    def _generate_markdown_report(self, summary: Dict):
        """Generate human-readable Markdown report"""
        md_lines = [
            "# StixORM Block Testing Report",
            f"\n**Generated:** {datetime.utcnow().isoformat()}",
            "\n## Summary\n",
            f"- **Total Objects:** {summary['total_objects']}",
            f"- **Passed:** {summary['passed']} ✅",
            f"- **Failed:** {summary['failed']} ❌",
            f"- **Errors:** {summary['errors']} ⚠️",
            f"- **Pass Rate:** {summary['pass_rate']:.1f}%",
            "\n## Results by Type\n"
        ]
        
        for obj_type, stats in sorted(summary['by_type'].items()):
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            md_lines.append(
                f"- **{obj_type}**: {stats['passed']}/{stats['total']} passed ({pass_rate:.1f}%)"
            )
        
        if summary['failures']:
            md_lines.append("\n## Failures\n")
            for failure in summary['failures']:
                md_lines.append(f"### {failure['object_type']} - {failure['object_id']}")
                md_lines.append(f"- **Status:** {failure['status']}")
                if failure.get('error_message'):
                    md_lines.append(f"- **Error:** {failure['error_message']}")
                if failure.get('differences'):
                    md_lines.append(f"- **Differences:** See test_results.json for details")
                md_lines.append("")
        
        with open(self.generated_dir / 'test_summary.md', 'w') as f:
            f.write('\n'.join(md_lines))
```

**Key Features:**
- Per-object result tracking
- Summary statistics by type
- Both JSON and Markdown outputs
- Detailed failure information

---

## Test Pipeline

### Phase 1: Discovery (`test_1_discovery.py`)

```python
import pytest
from pathlib import Path
from utils.discovery import ObjectDiscovery

@pytest.fixture(scope='session')
def discovery_results(stixorm_path, generated_dir):
    """Run discovery once per test session"""
    examples_dir = stixorm_path / 'examples'
    discovery = ObjectDiscovery(examples_dir, stixorm_path / 'Block_Families' / 'StixORM')
    
    results = discovery.discover_testable_objects()
    
    # Save discovery results
    import json
    with open(generated_dir / 'discovery_results.json', 'w') as f:
        json.dump([
            {
                'id': obj['id'],
                'type': obj['type'],
                'python_class': metadata.python_class,
                'group': metadata.group,
                'path': str(path)
            }
            for obj, metadata, path in results
        ], f, indent=2)
    
    return results

def test_discovery_finds_objects(discovery_results):
    """Verify discovery finds testable objects"""
    assert len(discovery_results) > 0, "No testable objects discovered"

def test_discovery_minimum_coverage(discovery_results):
    """Verify we have minimum expected coverage"""
    assert len(discovery_results) >= 130, f"Expected >=130 objects, found {len(discovery_results)}"

def test_all_groups_represented(discovery_results):
    """Verify all groups (SCO, SDO, SRO) are represented"""
    groups = {metadata.group for _, metadata, _ in discovery_results}
    assert 'sco' in groups, "No SCO objects found"
    assert 'sdo' in groups, "No SDO objects found"
```

**Purpose:** Verify discovery process and provide data for downstream tests

---

### Phase 2: Data Form Generation (`test_2_data_form_generation.py`)

```python
import pytest
from pathlib import Path
from utils.data_form_generator import DataFormGenerator

@pytest.fixture(scope='session')
def generation_results(discovery_results, stixorm_path, generated_dir):
    """Generate data forms once per test session"""
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

def test_generation_success_rate(generation_results):
    """Verify minimum 95% success rate"""
    total = len(generation_results['objects'])
    generated = len(generation_results['data_forms'])
    success_rate = (generated / total) * 100
    
    assert success_rate >= 95.0, f"Success rate {success_rate:.1f}% below 95% threshold"

def test_data_forms_valid_structure(generation_results):
    """Verify data forms have required structure"""
    for form_name, form_data in generation_results['data_forms'].items():
        assert 'typeql' in form_data, f"Missing 'typeql' in {form_name}"
        assert 'id' in form_data, f"Missing 'id' in {form_name}"

def test_reconstitution_data_complete(generation_results):
    """Verify reconstitution data includes all generated forms"""
    for form_name in generation_results['data_forms'].keys():
        assert form_name in generation_results['reconstitution_data'], \
            f"Missing reconstitution data for {form_name}"
```

**Purpose:** Validate data form generation and prepare for execution

---

### Phase 3: Block Execution (`test_3_block_execution.py`)

```python
import pytest
from pathlib import Path
from utils.block_executor import BlockExecutor

@pytest.fixture(scope='session')
def execution_results(discovery_results, generation_results, stixorm_path, generated_dir):
    """Execute all blocks once per test session"""
    executor = BlockExecutor(
        stixorm_path,
        generated_dir / 'data_forms',
        generated_dir / 'output_objects'
    )
    
    results = {}
    for obj, metadata, _ in discovery_results:
        try:
            result = executor.execute_block(
                obj,
                metadata,
                generation_results['reconstitution_data']
            )
            results[obj['id']] = {
                'status': 'SUCCESS',
                'object': result
            }
        except Exception as e:
            results[obj['id']] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    # Save execution results
    import json
    with open(generated_dir / 'execution_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    return results

@pytest.mark.parametrize('object_id', [
    pytest.param(obj_id, id=obj_id) 
    for obj_id in execution_results.keys()
])
def test_block_execution_succeeds(execution_results, object_id):
    """Verify each block executes successfully"""
    result = execution_results[object_id]
    assert result['status'] == 'SUCCESS', f"Execution failed: {result.get('error', 'Unknown error')}"

def test_execution_success_rate(execution_results):
    """Verify minimum 90% execution success rate"""
    total = len(execution_results)
    successes = sum(1 for r in execution_results.values() if r['status'] == 'SUCCESS')
    success_rate = (successes / total) * 100
    
    assert success_rate >= 90.0, f"Success rate {success_rate:.1f}% below 90% threshold"
```

**Purpose:** Execute blocks and capture outputs

---

### Phase 4: Verification (`test_4_verification.py`)

```python
import pytest
from utils.comparator import ObjectComparator

@pytest.fixture(scope='session')
def comparison_results(discovery_results, execution_results, test_reporter):
    """Compare all objects once per test session"""
    comparator = ObjectComparator()
    results = {}
    
    for obj, metadata, _ in discovery_results:
        obj_id = obj['id']
        
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
            differences=differences
        )
        
        results[obj_id] = {
            'status': status,
            'identical': is_identical,
            'differences': differences
        }
    
    return results

@pytest.mark.parametrize('object_id', [
    pytest.param(obj_id, id=obj_id)
    for obj_id in comparison_results.keys()
])
def test_object_comparison(comparison_results, object_id):
    """Verify each object matches original"""
    result = comparison_results[object_id]
    assert result['identical'], f"Object differs: {result['differences']}"

def test_overall_pass_rate(comparison_results):
    """Verify minimum 90% pass rate"""
    total = len(comparison_results)
    passed = sum(1 for r in comparison_results.values() if r['status'] == 'PASS')
    pass_rate = (passed / total) * 100
    
    assert pass_rate >= 90.0, f"Pass rate {pass_rate:.1f}% below 90% threshold"
```

**Purpose:** Compare original and reconstituted objects

---

### Phase 5: Reporting (`test_5_reporting.py`)

```python
import pytest
from utils.reporter import TestReporter

def test_generate_final_reports(test_reporter, generated_dir):
    """Generate final JSON and Markdown reports"""
    test_reporter.save_reports()
    
    # Verify reports exist
    assert (generated_dir / 'test_results.json').exists()
    assert (generated_dir / 'test_summary.json').exists()
    assert (generated_dir / 'test_summary.md').exists()

def test_summary_completeness(test_reporter):
    """Verify summary includes all metrics"""
    summary = test_reporter.generate_summary()
    
    assert 'total_objects' in summary
    assert 'passed' in summary
    assert 'failed' in summary
    assert 'pass_rate' in summary
    assert 'by_type' in summary

def test_display_summary(test_reporter, capsys):
    """Display summary to console"""
    summary = test_reporter.generate_summary()
    
    print("\n" + "="*60)
    print("STIXORM BLOCK TESTING SUMMARY")
    print("="*60)
    print(f"Total Objects:  {summary['total_objects']}")
    print(f"Passed:         {summary['passed']} ✅")
    print(f"Failed:         {summary['failed']} ❌")
    print(f"Pass Rate:      {summary['pass_rate']:.1f}%")
    print("="*60)
    
    captured = capsys.readouterr()
    assert "STIXORM BLOCK TESTING SUMMARY" in captured.out
```

**Purpose:** Generate reports and display results

---

## Pytest Configuration

### `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers for selective test execution
markers =
    discovery: Discovery phase tests
    generation: Data form generation tests
    execution: Block execution tests
    verification: Object comparison tests
    reporting: Report generation tests
    integration: Full pipeline integration tests

# Output options
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings

# Session-scoped fixtures
console_output_style = progress
```

### `conftest.py`

```python
import pytest
from pathlib import Path
import shutil
from utils.reporter import TestReporter

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
    Cleanup after session
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
    
    # Cleanup (optional - comment out to preserve artifacts)
    # shutil.rmtree(gen_dir)

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
    print("Test session complete - check generated/ for artifacts")
    print("="*70)
```

**Key Features:**
- Session-scoped fixtures to run expensive operations once
- Automatic directory creation and cleanup
- Shared reporter instance across all tests
- Custom markers for selective execution
- Clean console output

---

## Implementation Roadmap

### Phase 0: Environment Setup (Day 1)
1. **Verify Poetry Environment**
   - Ensure `poetry install` has been run
   - Verify pytest and deepdiff are available: `poetry run pytest --version`
   - Test Poetry environment: `poetry env info`

### Phase 1: Foundation (Week 1)
1. **Verify Directory Structure** ✅
   - All directories created in `tests/`
   - All utility modules implemented
   - Configuration files in place

2. **Test Discovery Module** ✅
   - Run: `poetry run pytest tests/test_1_discovery.py -v`
   - Validate with small subset of examples
   - Verify ParseContent integration

3. **Validate pytest Configuration** ✅
   - Test markers: `poetry run pytest -m discovery`
   - Verify fixture behavior
   - Check report generation

### Phase 2: Generation & Execution (Week 2)
4. **Test Data Form Generator** ✅
   - Run: `poetry run pytest tests/test_2_data_form_generation.py -v`
   - Verify integration with existing utilities
   - Review generated artifacts

5. **Test Block Executor** ✅
   - Run: `poetry run pytest tests/test_3_block_execution.py -v`
   - Start with simple objects
   - Validate dynamic imports
   - Test reference restoration

### Phase 3: Comparison & Reporting (Week 3)
6. **Test Comparator** ✅
   - Run: `poetry run pytest tests/test_4_verification.py -v`
   - Validate normalization logic
   - Review differences for failures

7. **Test Reporter** ✅
   - Run: `poetry run pytest tests/test_5_reporting.py -v`
   - Verify JSON and Markdown generation
   - Review report formats

### Phase 4: Integration & Testing (Week 4)
8. **Run Complete Pipeline**
   - Execute: `poetry run pytest tests/` or `.\tests\run_tests.ps1`
   - Analyze results in `tests/generated/reports/`
   - Tune thresholds based on results
   - Document failures

9. **Performance Analysis**
   - Run with timing: `poetry run pytest tests/ --durations=10`
   - Identify slow operations
   - Consider optimizations

### Phase 5: Optimization & Documentation (Week 5)
10. **Performance Optimization**
    - Profile slow operations
    - Add caching where appropriate
    - Consider parallel execution

11. **Documentation**
    - Update test thresholds based on actual performance
    - Document known issues
    - Add troubleshooting guide
    - Create usage examples

---

## Success Criteria

1. **Coverage:** Test >130 STIX objects (current example count)
2. **Generation Success Rate:** ≥95% of objects successfully generate data forms
3. **Execution Success Rate:** ≥90% of generated forms successfully execute
4. **Pass Rate:** ≥90% of executed blocks produce identical outputs
5. **Performance:** Complete pipeline runs in <10 minutes
6. **Reporting:** Clear identification of all failures with detailed diffs

---

## Known Limitations

1. **UUID Regeneration:** Every block invocation creates new UUIDs - comparison must exclude these fields
2. **Timestamp Differences:** `created` and `modified` fields will differ - must be excluded
3. **Reference Order:** Lists of references may have different orders - normalization required
4. **Embedded Object Dependencies:** Some objects require embedded objects as inputs - dependency resolution needed
5. **Single Failure:** One object in `convert_object_list_to_data_forms.py` fails (99.3% success) - needs investigation
6. **Complex References:** Some objects have circular or deeply nested references - may require special handling

---

## Future Enhancements

1. **CI/CD Integration:** GitHub Actions workflow for automated testing
2. **Parallel Execution:** Use pytest-xdist for faster test runs
3. **Coverage Tracking:** Track which blocks have been tested over time
4. **Regression Detection:** Compare results across code changes
5. **Performance Benchmarking:** Track execution times to detect performance regressions
6. **Interactive Dashboard:** Web-based visualization of test results
7. **Automated Issue Creation:** Create GitHub issues for persistent failures

---

## Appendix

### Integration with Existing Utilities

**convert_object_list_to_data_forms.py:**
- Function: `create_data_forms_from_stix_objects(objects, stixorm_path, output_dir)`
- Returns: `(data_forms_dict, reconstitution_data, creation_sequence)`
- Success Rate: 99.3% (151/152 objects)

**reconstitute_object_list.py:**
- Function: `restore_references_to_data_form(data_form, ref_info, id_mapping)`
- Purpose: Converts reference IDs back to full objects
- Critical for embedded object handling

**parse.py:**
- Function: `get_parse_content_for_object(stix_obj)`
- Returns: `ParseContent` metadata with `typeql`, `python_class`, `group`
- Success Rate: 100% on 133 tested objects

### Example Test Execution

```bash
# Using Poetry (all platforms)
poetry install
poetry run pytest tests/
poetry run pytest tests/test_1_discovery.py
poetry run pytest -m discovery
poetry run pytest -v --tb=short

# Using PowerShell runner script (Windows)
.\tests\run_tests.ps1
.\tests\run_tests.ps1 -Phase 1
.\tests\run_tests.ps1 -Marker discovery -Verbose

# Using Bash runner script (Linux/Mac)
./tests/run_tests.sh
./tests/run_tests.sh --phase 1
./tests/run_tests.sh --marker discovery

# Generate detailed HTML report (requires pytest-html)
poetry add --group dev pytest-html
poetry run pytest --html=tests/generated/reports/report.html --self-contained-html
```
- Phase 2: Integration with existing utilities
- Phase 3: Comprehensive coverage and pass rate improvements
- Phase 4: Robust error handling
- Phase 5: Clear reporting

---

## Success Criteria

- **Comprehensive Coverage**: Test all STIX objects with corresponding make_*.py blocks (target: >95%)
- **High Pass Rate**: Achieve >90% pass rate on first run
- **Robust Error Handling**: Gracefully handle failures without stopping test suite
- **Clear Reporting**: Provide actionable JSON and Markdown reports
- **Maintainability**: Modular, extensible architecture

## Directory Diagram

tests/
├── stixorm/
│ ├── conftest.py # Pytest fixtures and configuration
│ ├── pytest.ini # Pytest settings
│ ├── README.md # Testing documentation
│ │
│ ├── utils/ # Reusable testing utilities
│ │ ├── init.py
│ │ ├── discovery.py # Object discovery and filtering
│ │ ├── data_form_generator.py # Data form generation wrapper
│ │ ├── block_executor.py # Block invocation logic
│ │ ├── comparator.py # DeepDiff comparison with normalization
│ │ └── reporter.py # Report generation
│ │
│ ├── fixtures/ # Test fixtures and reference data
│ │ └── testable_objects.json # Discovered testable objects
│ │
│ ├── generated/ # Generated test artifacts (gitignored)
│ │ ├── data_forms/ # Generated data forms
│ │ ├── input_objects/ # Original STIX objects
│ │ ├── output_objects/ # Reconstituted STIX objects
│ │ ├── reconstitution_data.json # Reference restoration metadata
│ │ ├── execution_results.json # Block execution results
│ │ ├── verification_results.json # Comparison results
│ │ ├── test_summary.json # Summary statistics (JSON)
│ │ └── test_summary.md # Summary report (Markdown)
│ │
│ └── tests/ # Test files
│ ├── test_1_discovery.py # Object discovery tests
│ ├── test_2_data_form_generation.py # Data form generation tests
│ ├── test_3_block_execution.py # Block execution tests
│ ├── test_4_verification.py # Object verification tests
│ └── test_5_reporting.py # Report generation tests
│
└── os_triage/ # OS_Triage testing (future)
├── conftest.py # Placeholder
├── fixtures/ # Placeholder
└── README.md # TODO documentation



