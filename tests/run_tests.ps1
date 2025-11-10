#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run StixORM testing suite using Poetry environment

.DESCRIPTION
    This script runs the StixORM block testing system using the Poetry-managed
    Python environment. It ensures dependencies are installed and runs pytest
    with appropriate options.

.PARAMETER Phase
    Specific test phase to run (1-5). If not specified, runs all phases.

.PARAMETER Marker
    Run tests with specific marker (discovery, generation, execution, verification, reporting)

.PARAMETER Verbose
    Enable verbose output

.EXAMPLE
    .\run_tests.ps1
    Run all tests

.EXAMPLE
    .\run_tests.ps1 -Phase 1
    Run only Phase 1 (discovery)

.EXAMPLE
    .\run_tests.ps1 -Marker discovery -Verbose
    Run discovery tests with verbose output
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateRange(1,5)]
    [int]$Phase,

    [Parameter(Mandatory=$false)]
    [ValidateSet('discovery', 'generation', 'execution', 'verification', 'reporting')]
    [string]$Marker,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# Ensure we're in the project root
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "StixORM Block Testing System" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check if Poetry is installed
try {
    $poetryVersion = poetry --version
    Write-Host "✓ Poetry found: $poetryVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Poetry not found. Please install Poetry first:" -ForegroundColor Red
    Write-Host "  https://python-poetry.org/docs/#installation" -ForegroundColor Yellow
    exit 1
}

# Ensure dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
poetry install --no-interaction
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Build pytest command
$pytestArgs = @("pytest", "tests/")

if ($Phase) {
    $pytestArgs = @("pytest", "tests/test_${Phase}_*.py")
    Write-Host "Running Phase $Phase tests..." -ForegroundColor Cyan
} elseif ($Marker) {
    $pytestArgs += @("-m", $Marker)
    Write-Host "Running tests with marker: $Marker..." -ForegroundColor Cyan
} else {
    Write-Host "Running all tests..." -ForegroundColor Cyan
}

if ($Verbose) {
    $pytestArgs += "-v"
}

Write-Host ""

# Run tests
poetry run @pytestArgs

# Capture exit code
$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan

if ($exitCode -eq 0) {
    Write-Host "✓ Tests completed successfully" -ForegroundColor Green
    Write-Host "Check tests/generated/reports/ for detailed results" -ForegroundColor Cyan
} else {
    Write-Host "✗ Tests completed with failures" -ForegroundColor Red
    Write-Host "Check tests/generated/reports/ for details" -ForegroundColor Cyan
}

Write-Host "=" * 70 -ForegroundColor Cyan

exit $exitCode
