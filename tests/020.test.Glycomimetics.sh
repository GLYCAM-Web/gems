#!/usr/bin/env bash
bash logs/clearLogs.sh

# Run the test
# TEST_INPUT=${1:-"/programs/gems/ct-input-git-ignore-me.json"}
# TEST_INPUT=${1:-"/programs/gems/tests/inputs/008.0.evaluation-request.json"}
# TEST_INPUT=${1:-"/programs/gems/gemsModules/mmservice/mdaas/tests/inputs/run_md.json"}
#
TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/entity_evaluate.json"
#TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/explicit_evaluate.json"

OUTPUT=$(/programs/gems/bin/delegate $TEST_INPUT)

# Check the output is a valid JSON
echo $OUTPUT | python -m json.tool > ct-output-git-ignore-me.json
if [ $? -ne 0 ]; then
  echo "Output is not a valid JSON"
  echo $OUTPUT > ct-invalid-output-git-ignore-me.json
  exit 1
fi

# Inspect as needed
# tests/utilities/json_ripper.py --json_file ct-output-git-ignore-me.json entity
cat ct-output-git-ignore-me.json

