#!/bin/bash
# Run StixORM testing suite using Poetry environment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Ensure we're in the project root
cd "$(dirname "$0")/.."

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}StixORM Block Testing System${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}✗ Poetry not found. Please install Poetry first:${NC}"
    echo -e "${YELLOW}  https://python-poetry.org/docs/#installation${NC}"
    exit 1
fi

POETRY_VERSION=$(poetry --version)
echo -e "${GREEN}✓ Poetry found: ${POETRY_VERSION}${NC}"

# Ensure dependencies are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
poetry install --no-interaction
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Parse arguments
PYTEST_ARGS="tests/"
if [ "$1" == "--phase" ] && [ -n "$2" ]; then
    PYTEST_ARGS="tests/test_${2}_*.py"
    echo -e "${CYAN}Running Phase $2 tests...${NC}"
elif [ "$1" == "--marker" ] && [ -n "$2" ]; then
    PYTEST_ARGS="tests/ -m $2"
    echo -e "${CYAN}Running tests with marker: $2...${NC}"
elif [ "$1" == "--verbose" ]; then
    PYTEST_ARGS="tests/ -v"
    echo -e "${CYAN}Running all tests (verbose)...${NC}"
else
    echo -e "${CYAN}Running all tests...${NC}"
fi

echo ""

# Run tests
poetry run pytest $PYTEST_ARGS

# Capture exit code
EXIT_CODE=$?

echo ""
echo -e "${CYAN}======================================================================${NC}"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Tests completed successfully${NC}"
    echo -e "${CYAN}Check tests/generated/reports/ for detailed results${NC}"
else
    echo -e "${RED}✗ Tests completed with failures${NC}"
    echo -e "${CYAN}Check tests/generated/reports/ for details${NC}"
fi

echo -e "${CYAN}======================================================================${NC}"

exit $EXIT_CODE
