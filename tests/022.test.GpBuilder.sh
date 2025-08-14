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
#   - 1 if input files are missing or the evaluation response does not contain a project directory
#   - 2 if the build response is not valid JSON
#   - 3 if no zip file is found in the project directory
#   - 4 if the zip file is empty
#   - 5 if the build execution failed
#   - 6 if the build completed with errors

# --- Environment Setup ---
set -euo pipefail
DEBUG=${DEBUG:-false}
debug_log() {
  if [ "$DEBUG" = true ]; then
    echo "DEBUG: $*"
  fi
}

exit_handler() {
  exit_code=$?

  echo $EVALUATE_REQUEST >bad_outputs/$(date +%Y%m%d_%H%M)-test-022-evaluate-request-git-ignore-me.json
  if [ -n "${EVALUATE_RESPONSE:-}" ]; then
    echo "$EVALUATE_RESPONSE" >bad_outputs/$(date +%Y%m%d_%H%M)-test-022-evaluate-response-git-ignore-me.json
  fi
  if [ -n "${BUILD_REQUEST:-}" ]; then
    echo "$BUILD_REQUEST" >bad_outputs/$(date +%Y%m%d_%H%M)-test-022-build-request-git-ignore-me.json
  fi
  if [ -n "${BUILD_RESPONSE:-}" ]; then
    echo "$BUILD_RESPONSE" >bad_outputs/$(date +%Y%m%d_%H%M)-test-022-build-response-git-ignore-me.json
  fi

  if [ $exit_code -ne 0 ]; then
    echo "❌ An error occurred, saving bad outputs to bad_outputs directory. ($exit_code)"
    echo -e "\tCheck $GEMSHOME/tests/bad_outputs directory for details." >&2
  else
    echo "✅ Test 022 Build completed successfully, status file: $STATUS_FILE"

    if [[ "${GEMS_KEEP_BAD_OUTPUTS:-}" == "True" ]]; then
      echo -e "\tGEMS_KEEP_BAD_OUTPUTS is truthy, keeping bad outputs."
    else
      echo -e "\tGEMS_KEEP_BAD_OUTPUTS is not truthy, removing bad outputs."
      rm -rf bad_outputs/*-test-022-*
    fi

    if [[ "${GEMS_REMOVE_TEST_PROJECT:-}" == "true" || "${GEMS_REMOVE_TEST_PROJECT:-}" == "1" ]]; then
      rm -rf "$PROJECT_DIR_PATH"
      echo -e "\tRemoved test project directory, to prevent this set GEMS_REMOVE_TEST_PROJECT to false."
    else
      echo -e "\tGEMS_REMOVE_TEST_PROJECT is not set to true, the project directory will be kept."
    fi
  fi
}
trap exit_handler EXIT


# --- Input Files ---
PDB_FILE="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/pdbs/1eer_eop_Asn.pdb"
EVALUATE_REQUEST_TEMPLATE_FILE="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate_parameterized.json"
EVALUATE_RCSB_REQUEST_FILE="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate_rcsb.json"

BUILD_REQUEST_TEMPLATE_FILE="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_build_parameterized.json"
BUILD_RCSB_REQUEST_FILE="$GEMSHOME/gemsModules/complex/GpBuilder/tests/inputs/explicit_build_rcsb_param.json"

if [ ! -f "$PDB_FILE" ]; then
  echo "PDB file not found: $PDB_FILE" >&2
  exit 1
fi

if [ ! -f "$EVALUATE_REQUEST_TEMPLATE_FILE" ]; then
  echo "Evaluate request template not found: $EVALUATE_REQUEST_TEMPLATE_FILE" >&2
  exit 1
fi

if [ ! -f "$BUILD_REQUEST_TEMPLATE_FILE" ]; then
  echo "Build request template not found: $BUILD_REQUEST_TEMPLATE_FILE" >&2
  exit 1
fi


# --- Workflow Execution ---
# Delegate the evaluation request.
if [[ "${RCSB_EVALUATION:-}" == "true" ]] || [[ "${RCSB_EVALUATION:-}" == "1" ]]; then
  echo "Using RCSB evaluation request instead of default protein_file."
  EVALUATE_REQUEST=$(cat "$EVALUATE_RCSB_REQUEST_FILE")
else
  EVALUATE_REQUEST=$(sed "s|<protein_file>|${PDB_FILE}|" "$EVALUATE_REQUEST_TEMPLATE_FILE")
fi
debug_log "Evaluation Request: ${EVALUATE_REQUEST}"

EVALUATE_RESPONSE=$(echo "$EVALUATE_REQUEST" | $GEMSHOME/bin/delegate)
debug_log "Evaluation Response: ${EVALUATE_RESPONSE}"
# TODO: Extract glycosites and update build request with them for RCSB evaluation.

# Extract the project directory and pUUID path from the evaluation response.
PROJECT_DIR_PATH=$(echo "$EVALUATE_RESPONSE" | grep -o '"project_dir": *"[^"]*' | cut -d'"' -f4)
PUUID=$(echo "$EVALUATE_RESPONSE" | grep -o '"pUUID": *"[^"]*' | cut -d'"' -f4 | head -n 1)
debug_log "pUUID: $PUUID"
debug_log "Project Directory Path: ${PROJECT_DIR_PATH}"
if [ -z "$PROJECT_DIR_PATH" ]; then
  echo -e "Error: Could not find 'project_dir' in the evaluation response.\nCheck the bad_outputs dir for more info." >&2
  exit 1
elif [ -z "$PUUID" ]; then
  echo -e "Error: Could not find 'pUUID' in the evaluation response.\nCheck the bad_outputs dir for more info." >&2
  exit 1
fi

# Substitute the pUUID from the evaluation response into the build request template.
if [[ "${RCSB_EVALUATION:-}" == "true" ]] || [[ "${RCSB_EVALUATION:-}" == "1" ]]; then
  echo "Using RCSB build request."
  BUILD_TEMPLATE="$BUILD_RCSB_REQUEST_FILE"
else
  BUILD_TEMPLATE="$BUILD_REQUEST_TEMPLATE_FILE"
fi
BUILD_REQUEST=$(sed "s/<pUUID>/$PUUID/" "$BUILD_TEMPLATE")

debug_log "Build Request: ${BUILD_REQUEST}"

# Delegate the prepared build request to start the GpBuilder Build service.
BUILD_RESPONSE=$(echo "$BUILD_REQUEST" | $GEMSHOME/bin/delegate)
debug_log "Build Response: ${BUILD_RESPONSE}"

# --- Check results ---
echo "$BUILD_RESPONSE" | python -m json.tool >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "Output is not a valid JSON response.\nCheck the bad_outputs dir for more info." >&2
  exit 2
elif echo "$BUILD_RESPONSE" | grep started -q; then
  STATUS_FILE="${PROJECT_DIR_PATH}/status.log"
  debug_log "Status File: ${STATUS_FILE}"
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
          exit 0
        fi
      fi
    elif grep -q "GpBuilder execution failed" "$STATUS_FILE"; then
      echo "GpBuilder execution failed, check the status file: $STATUS_FILE" >&2
      exit 5
    elif grep -q "Completed with errors" "${STATUS_FILE}"; then
      echo "Build completed with errors." >&2
      echo "See status file: $STATUS_FILE for more details." >&2
      exit 6
    elif grep -q "GpBuilder execution started" "$STATUS_FILE"; then
      echo "GpBuilder/Build started."
    fi

    remaining_time=$(( (max_tries - tries) * wait_duration ))
    tries=$((tries + 1))
    echo "Waiting for build to complete... (wait time remaining: ${remaining_time} seconds)"
    sleep $wait_duration
  done

  if [ $tries -ge $max_tries ]; then
    echo "Build did not complete within the expected time." >&2
    exit 6
  fi
else
  echo "Build failed. No submission notice found in the response." >&2
  exit 5
fi
