#!/bin/bash
# This script runs the GpBuilder workflow by first evaluating a request and then building a project based on the evaluation.

# Exit immediately if a command exits with a non-zero status.
# Treat unset variables as an error.
# Pipelines fail if any command fails, not just the last one.
set -euo pipefail

# Keep the output directory for debugging if the test fails.
# TODO: use temporary bad outputs directory for this test
export GEMS_KEEP_BAD_OUTPUTS=True

# --- Input Files ---
# 1. Evaluate request
EVALUATE_REQUEST="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate.json"
# 2. Build Request
BUILD_REQUEST="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_build_paramaterized.json"


# --- Workflow Execution ---

# Run the evaluation delegate
EVALUATE_RESPONSE=$($GEMSHOME/bin/delegate "$EVALUATE_REQUEST")

# Step 1: Extract the project directory path from the JSON response.
# We grep for the 'project_dir' line and use cut to get the value.
# If grep doesn't find a match, it will exit with an error, and `set -e` will stop the script here.
PROJECT_DIR_PATH=$(echo "$EVALUATE_RESPONSE" | grep -o '"project_dir": *"[^"]*' | cut -d'"' -f4)

# Add an explicit check for an empty path to provide a better error message.
if [ -z "$PROJECT_DIR_PATH" ]; then
  echo "Error: Could not find 'project_dir' in the evaluation response." >&2
  echo "Response was: $EVALUATE_RESPONSE" >&2
  exit 1
fi

# Step 2: Get the basename of the path.
# This is now a standalone command. If it fails, `set -e` will stop the script.
PUUID=$(basename "$PROJECT_DIR_PATH")

# Step 3: Substitute the pUUID into the build request template.
# This uses sed to replace the placeholder.
# Note the improved syntax: `sed ... file` is preferred over `cat file | sed ...`
BUILD_REQUEST_JSON=$(sed "s/<pUUID>/$PUUID/" "$BUILD_REQUEST")

# Run the build delegate with the now-complete request JSON.
BUILD_RESPONSE=$(echo "$BUILD_REQUEST_JSON" | $GEMSHOME/bin/delegate)

# check that the response is a valid JSON
echo "$BUILD_RESPONSE" | python -m json.tool > test-22-output-git-ignore-me.json
if [ $? -ne 0 ]; then
  echo "Output is not a valid JSON"
  echo "$BUILD_RESPONSE" > test-22-invalid-output-git-ignore-me.json
  exit 1
else
  echo "Output is a valid JSON"
fi
