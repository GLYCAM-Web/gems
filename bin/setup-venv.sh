#!/bin/bash
# ==============================================================================
# GEMS Virtual Environment Setup Script
# ==============================================================================
# Creates and configures a Python virtual environment (.venv) inside GEMSHOME
# with all required dependencies for GEMS execution and gRPC services.
# ==============================================================================

set -e

# Resolve GEMSHOME if not set
if [ -z "${GEMSHOME}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    GEMSHOME="$(cd "${SCRIPT_DIR}/.." && pwd)"
    export GEMSHOME
fi

echo "=========================================="
echo " Setting up GEMS Virtual Environment"
echo " GEMSHOME: ${GEMSHOME}"
echo "=========================================="

VENV_DIR="${GEMSHOME}/.venv"

# Locate suitable python3 binary (respect PYTHON_BIN or --python, else prefer newer Python 3.x)
if [ "${1:-}" = "--python" ] && [ -n "${2:-}" ]; then
    PYTHON_BIN="${2}"
fi

if [ -z "${PYTHON_BIN:-}" ]; then
    for cand in python3.12 python3.11 python3.10 python3.9 python3.8 python3; do
        if command -v "${cand}" >/dev/null 2>&1; then
            PYTHON_BIN="$(command -v "${cand}")"
            break
        fi
    done
fi

if [ -z "${PYTHON_BIN:-}" ] || ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "Error: No suitable python3 binary found in PATH." >&2
    exit 1
fi

echo "Using Python binary: ${PYTHON_BIN} ($("${PYTHON_BIN}" --version))"

# Create virtual environment if it does not exist (check bin/activate in case a previous run left a broken dir)
if [ ! -f "${VENV_DIR}/bin/activate" ]; then
    if [ -d "${VENV_DIR}" ]; then
        echo "Removing incomplete virtual environment at ${VENV_DIR}..."
        rm -rf "${VENV_DIR}"
    fi
    echo "Creating virtual environment at ${VENV_DIR}..."
    if ! "${PYTHON_BIN}" -m venv "${VENV_DIR}"; then
        echo "Error: Failed to create virtual environment. Removing partial ${VENV_DIR}." >&2
        rm -rf "${VENV_DIR}"
        exit 1
    fi
else
    echo "Existing virtual environment found at ${VENV_DIR}."
fi

# Activate virtual environment
source "${VENV_DIR}/bin/activate"

echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Install base requirements if requirements.txt exists
if [ -f "${GEMSHOME}/requirements.txt" ]; then
    echo "Installing dependencies from ${GEMSHOME}/requirements.txt..."
    pip install -r "${GEMSHOME}/requirements.txt"
fi

# Ensure gRPC dependencies are present
echo "Ensuring gRPC dependencies (grpcio, protobuf)..."
pip install grpcio protobuf

echo "=========================================="
echo " Virtual environment setup complete!"
echo " Location: ${VENV_DIR}"
echo ""
echo " To activate this environment in your shell run:"
echo "   source ${VENV_DIR}/bin/activate"
echo "=========================================="
