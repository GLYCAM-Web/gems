#!/bin/bash
# GpBuilder v1 test workflow script.
#
# This script first delegates an evaluation request to the GpBuilder service,
# then it crafts the build request using the project UUID from the evaluation response,
# and finally it delegates the build request to the GpBuilder service.
#
# It waits for the build to complete, checking the status file for completion,
# and verifies that the resulting zip file is non-empty.
# 
# Usage: cd $GEMSHOME/tests && ./run_tests.sh 022.test.GpBuilder.sh
#
# Returns:
#   - 0 on success
#   - 1 if the evaluation response does not contain a project directory
#   - 2 if the build response is not valid JSON
#   - 3 if no zip file is found in the project directory
#   - 4 if the zip file is empty
#   - 5 if the build execution failed
#   - 6 if the build completed with errors

set -euo pipefail

# --- Input Files ---
EVALUATE_REQUEST="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate.json"
BUILD_REQUEST_TEMPLATE="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_build_parameterized.json"


# --- Workflow Execution ---
# Delegate the evaluation request.
EVALUATE_RESPONSE=$($GEMSHOME/bin/delegate "$EVALUATE_REQUEST")

# Extract the project directory path from the evaluation response.
PROJECT_DIR_PATH=$(echo "$EVALUATE_RESPONSE" | grep -o '"project_dir": *"[^"]*' | cut -d'"' -f4)
if [ -z "$PROJECT_DIR_PATH" ]; then
  echo -e "Error: Could not find 'project_dir' in the evaluation response.\nCheck the bad_outputs dir for more info." >&2
  echo $EVALUATE_RESPONSE >bad_outputs/$(date +%Y%m%d_%H%M)-test-022-evaluate-response-git-ignore-me.json
  exit 1
fi

# Substitute the pUUID from the evaluation response into the build request template.
PUUID=$(basename "$PROJECT_DIR_PATH")
BUILD_REQUEST=$(sed "s/<pUUID>/$PUUID/" "$BUILD_REQUEST_TEMPLATE")

# Delegate the prepared build request to start the GpBuilder Build service.
BUILD_RESPONSE=$(echo "$BUILD_REQUEST" | $GEMSHOME/bin/delegate)


# Check results.
echo "$BUILD_RESPONSE" | python -m json.tool >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "Output is not a valid JSON response.\nCheck the bad_outputs dir for more info." >&2
  echo "$BUILD_RESPONSE" > bad_outputs/$(date +%Y%m%d_%H%M)-test-022-build-response-git-ignore-me.json
  exit 2
elif echo "$BUILD_RESPONSE" | grep started -q; then
  STATUS_FILE="$PROJECT_DIR_PATH/status.log"
  echo "Build starting, active project directory: $PROJECT_DIR_PATH"
  tries=0
  max_tries=30
  wait_duration=2
  while [ $tries -lt $max_tries ]; do
    if [ ! -f "$STATUS_FILE" ]; then
      echo "Status file not found yet, waiting..."
    elif grep -q "All complete" "$STATUS_FILE"; then
      ZIP_FILE=$(find "$PROJECT_DIR_PATH" -maxdepth 1 -name "GP_project_*.zip" -print -quit)
      if [ ! -n "$ZIP_FILE" ]; then
        echo "No zip file found in the project directory." >&2
        exit 3
      else
        # check archive is non-empty
        if [ ! -s "$ZIP_FILE" ]; then
          echo "Zip file is empty." >&2
          exit 4
        else
          echo "Build completed successfully, status file: $STATUS_FILE"
          # rm -r "$PROJECT_DIR_PATH"
          exit 0
        fi
      fi
    elif grep -q "GpBuilder execution started" "$STATUS_FILE"; then
      echo "GpBuilder/Build started."
    elif grep -q "GpBuilder execution failed" "$STATUS_FILE"; then
      echo "GpBuilder execution failed, check the status file: $STATUS_FILE" >&2
      exit 5
    elif grep -q "Completed with errors" "$STATUS_FILE"; then
      echo "Build completed with errors." >&2
      echo "See status file: $STATUS_FILE for more details." >&2
      exit 6
    fi
    remaining_time=$(( (max_tries - tries) * wait_duration ))
    echo "Waiting for build to complete... (wait time remaining: ${remaining_time} seconds)"

    tries=$((tries + 1))
    sleep $wait_duration
  done
else
  echo "Build failed. No submission notice found in the response." >&2
  exit 5
fi
