# StixORM Testing System

This directory contains the comprehensive testing system for validating all StixORM blocks.

## Quick Start

### Using the Test Runner Scripts (Recommended)

**Windows (PowerShell):**
```powershell
# Run all tests
.\tests\run_tests.ps1

# Run specific phase
.\tests\run_tests.ps1 -Phase 1

# Run with marker
.\tests\run_tests.ps1 -Marker discovery -Verbose
```

**Linux/Mac:**
```bash
# Run all tests
./tests/run_tests.sh

# Run specific phase
./tests/run_tests.sh --phase 1

# Run with marker
./tests/run_tests.sh --marker discovery
```

### Using Poetry Directly

```bash
# Ensure Poetry environment is set up
poetry install

# Run all tests using Poetry
poetry run pytest tests/

# Run specific phase
poetry run pytest tests/test_1_discovery.py
poetry run pytest tests/test_2_data_form_generation.py
poetry run pytest tests/test_3_block_execution.py
poetry run pytest tests/test_4_verification.py
poetry run pytest tests/test_5_reporting.py

# Run with specific markers
poetry run pytest -m discovery
poetry run pytest -m generation
poetry run pytest -m execution
poetry run pytest -m verification
poetry run pytest -m reporting
```

## Directory Structure

```
tests/
├── pytest.ini              # Pytest configuration
├── conftest.py            # Shared fixtures
├── test_1_discovery.py    # Phase 1: Object discovery
├── test_2_data_form_generation.py  # Phase 2: Data form generation
├── test_3_block_execution.py       # Phase 3: Block execution
├── test_4_verification.py          # Phase 4: Comparison
├── test_5_reporting.py             # Phase 5: Report generation
├── utils/                 # Utility modules
│   ├── discovery.py      # Object discovery
│   ├── data_form_generator.py  # Data form generation
│   ├── block_executor.py       # Block execution
│   ├── comparator.py           # Object comparison
│   └── reporter.py             # Report generation
└── generated/            # Test artifacts (gitignored)
    ├── data_forms/       # Generated data forms
    ├── input_objects/    # Original STIX objects
    ├── output_objects/   # Reconstituted objects
    └── reports/          # Test reports
```

## Test Phases

### Phase 1: Discovery
Scans `Block_Families/StixORM/examples/` for STIX objects and identifies which have corresponding `make_*.py` blocks.

### Phase 2: Data Form Generation
Converts STIX objects to data forms using the existing `convert_object_list_to_data_forms.py` utility.

### Phase 3: Block Execution
Executes each `make_*.py` block with the generated data forms to reconstitute STIX objects.

### Phase 4: Verification
Compares original and reconstituted objects using DeepDiff with normalization for UUIDs, timestamps, and reference order.

### Phase 5: Reporting
Generates JSON and Markdown reports with detailed results and summary statistics.

## Output Files

After running tests, check `tests/generated/reports/`:
- `test_results.json` - Detailed results for each object
- `test_summary.json` - Summary statistics
- `test_summary.md` - Human-readable report

## Success Criteria

- **Discovery**: Find >50 testable objects
- **Generation**: >85% success rate
- **Execution**: >70% success rate
- **Verification**: >60% pass rate

## Troubleshooting

### Import Errors
If you see import errors, ensure Poetry environment is activated and you're running from the project root:

```bash
cd c:\projects\brett_blocks
poetry install
poetry run pytest tests/
```

### Missing Dependencies
All dependencies are managed by Poetry. If you see missing packages:

```bash
poetry install
```

### No Objects Found
Verify examples directory exists:

```bash
dir Block_Families\StixORM\examples\
```

### Poetry Environment Issues
Verify Poetry environment is working:

```bash
poetry env info
poetry show pytest deepdiff
```

## Architecture

See `architecture/stixorm-testing-system-design.md` for complete design documentation.
