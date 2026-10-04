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

# Locate suitable python3 binary (prefer python3.9 if available)
PYTHON_BIN=""
if command -v python3.9 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3.9)"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
else
    echo "Error: Neither python3.9 nor python3 was found in PATH." >&2
    exit 1
fi

echo "Using Python binary: ${PYTHON_BIN} ($("${PYTHON_BIN}" --version))"

# Create virtual environment if it does not exist
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating virtual environment at ${VENV_DIR}..."
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
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
