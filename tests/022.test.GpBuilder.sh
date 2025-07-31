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
PROJECT_DIR_PATH=$(echo "$EVALUATE_RESPONSE" | grep -o '"project_dir": *"[^"]*' | cut -d'"' -f4)
STATUS_FILE="$PROJECT_DIR_PATH/status.log"

# Add an explicit check for an empty path to provide a better error message.
if [ -z "$PROJECT_DIR_PATH" ]; then
  echo "Error: Could not find 'project_dir' in the evaluation response." >&2
  echo "Response was: $EVALUATE_RESPONSE" >&2
  exit 1
fi

# Step 2: Get the basename of the path.
PUUID=$(basename "$PROJECT_DIR_PATH")

# Step 3: Substitute the pUUID into the build request template.
BUILD_REQUEST_JSON=$(sed "s/<pUUID>/$PUUID/" "$BUILD_REQUEST")

# Run the build delegate with the now-complete request JSON.
BUILD_RESPONSE=$(echo "$BUILD_REQUEST_JSON" | $GEMSHOME/bin/delegate)

# check that the response is a valid JSON
echo "$BUILD_RESPONSE" | python -m json.tool > test-22-output-git-ignore-me.json
if [ $? -ne 0 ]; then
  echo "Output is not a valid JSON"
  echo "$BUILD_RESPONSE" > test-22-invalid-output-git-ignore-me.json
  exit 2
elif echo "$BUILD_RESPONSE" | grep started -q; then
      echo "Build was started, project directory: $PROJECT_DIR_PATH"
      tries=0
      max_tries=30
      wait_duration=2
      success=false
      while [ $tries -lt $max_tries ]; do
          if [ ! -f "$STATUS_FILE" ]; then
              echo "Status file not found yet, waiting..."
          elif grep -q "All complete" "$STATUS_FILE"; then
              ZIP_FILE=$(find "$PROJECT_DIR_PATH" -maxdepth 1 -name "GP_project_*.zip" -print -quit)
              if [ ! -n "$ZIP_FILE" ]; then
                  echo "No zip file found in the project directory." >&2
                  echo "$BUILD_RESPONSE" > test-22-invalid-output-git-ignore-me.json
                  exit 3
              else
                  # check archive is non-empty
                  if [ ! -s "$ZIP_FILE" ]; then
                      echo "Zip file is empty." >&2
                      echo "$BUILD_RESPONSE" > test-22-invalid-output-git-ignore-me.json
                      exit 4
                  else
                      echo "Build completed successfully, status:"
                      cat "$STATUS_FILE"
                      # rm -r "$PROJECT_DIR_PATH"
                      exit 0
                  fi
              fi
          elif grep -q "Completed with errors" "$STATUS_FILE"; then
              echo "Build completed with errors."
              echo "$BUILD_RESPONSE" > test-22-invalid-output-git-ignore-me.json
              echo "See status file: $STATUS_FILE for more details." >&2
              exit 5
          fi
          remaining_time=$(( (max_tries - tries) * wait_duration ))
          echo "Waiting for build to complete... (wait time remaining: ${remaining_time} seconds)"

          tries=$((tries + 1))
          sleep $wait_duration
      done
  else
      echo "Build failed. No success notice found in the response." >&2
      echo "$BUILD_RESPONSE" > test-22-invalid-output-git-ignore-me.json
      exit 6
  fi
fi
