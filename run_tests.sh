#!/bin/bash
# run_tests.sh
# Activates the project venv, runs the pytest suite,
# and exits 0 on success or 1 on any failure.

set -u  # treat undefined variables as errors

# ---------- 1. Activate virtual environment ----------
# Try Windows-style venv layout first (.venv/Scripts/activate),
# fall back to Linux/Mac layout (.venv/bin/activate) for CI portability.
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "ERROR: Could not find virtual environment at .venv/"
    exit 1
fi

# ---------- 2. Run the test suite ----------
pytest
pytest_exit_code=$?

# ---------- 3. Normalize exit code (task requires 0 or 1) ----------
if [ $pytest_exit_code -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Test suite failed (pytest exit code: $pytest_exit_code)."
    exit 1
fi