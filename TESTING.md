# StixORM Testing - Quick Reference

## Setup (One Time)

```bash
# Install all dependencies via Poetry
poetry install
```

## Running Tests

### Quick Start (Recommended)

**Windows:**
```powershell
.\tests\run_tests.ps1
```

**Linux/Mac:**
```bash
./tests/run_tests.sh
```

### Using Poetry Directly

```bash
# All tests
poetry run pytest tests/

# Specific phase (1-5)
poetry run pytest tests/test_1_discovery.py
poetry run pytest tests/test_2_data_form_generation.py
poetry run pytest tests/test_3_block_execution.py
poetry run pytest tests/test_4_verification.py
poetry run pytest tests/test_5_reporting.py

# By marker
poetry run pytest -m discovery
poetry run pytest -m generation
poetry run pytest -m execution
poetry run pytest -m verification
poetry run pytest -m reporting

# Verbose output
poetry run pytest tests/ -v
```

### PowerShell Runner Options

```powershell
# Run specific phase
.\tests\run_tests.ps1 -Phase 1

# Run with marker
.\tests\run_tests.ps1 -Marker discovery

# Verbose output
.\tests\run_tests.ps1 -Verbose

# Combine options
.\tests\run_tests.ps1 -Phase 3 -Verbose
```

### Bash Runner Options

```bash
# Run specific phase
./tests/run_tests.sh --phase 1

# Run with marker  
./tests/run_tests.sh --marker discovery

# Verbose output
./tests/run_tests.sh --verbose
```

## Results

After running tests, check:
- `tests/generated/reports/test_summary.md` - Human-readable summary
- `tests/generated/reports/test_summary.json` - Summary statistics
- `tests/generated/reports/test_results.json` - Detailed per-object results

## Test Phases

1. **Discovery** - Find testable STIX objects with make_*.py blocks
2. **Generation** - Convert STIX objects to data forms
3. **Execution** - Execute make_*.py blocks to reconstitute objects
4. **Verification** - Compare original vs reconstituted objects
5. **Reporting** - Generate comprehensive reports

## Dependencies

All managed by Poetry (defined in `pyproject.toml`):
- pytest - Testing framework
- deepdiff - Object comparison
- typedb-client, stixorm, requests - StixORM dependencies

## Troubleshooting

```bash
# Verify Poetry environment
poetry env info

# Check dependencies
poetry show pytest deepdiff

# Reinstall if needed
poetry install --no-cache

# Update dependencies
poetry update
```

## Documentation

- `tests/README.md` - Detailed testing documentation
- `architecture/stixorm-testing-system-design.md` - Complete system design

## Environment

- Uses Poetry-managed Python environment (3.9+)
- No separate pip installations required
- Consistent across development and testing
