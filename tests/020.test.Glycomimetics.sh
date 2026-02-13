#!/usr/bin/env bash
rm -f test-20-output-git-ignore-me.json
rm -f test-20-invalid-output-git-ignore-me.json

# Run the test
#TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/entity_evaluate.json"
#TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/explicit_evaluate.json"
TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/explicit_build.test.json"

#OUTPUT=$(/programs/gems/bin/delegate $TEST_INPUT)
# same as above, but capture stderr seprately
### THERE SHOULD BE NO STDERR
OUTPUT=$(/programs/gems/bin/delegate $TEST_INPUT 2>/dev/null)

# Check the output is a valid JSON
echo $OUTPUT | python -m json.tool >test-20-output-git-ignore-me.json
if [ $? -ne 0 ]; then
  echo "Output is not a valid JSON"
  echo $OUTPUT > test-20-invalid-output-git-ignore-me.json
  exit 1
else
  # Check that Evaluation worked.
  echo $OUTPUT | grep "Evaluation Successful">/dev/null || exit 1

  # Check that Build is running.
  echo $OUTPUT | grep "Glycomimetics is running">/dev/null || exit 1


  # grab "projectect_dir": "<dir>" with grep
  PROJECT_DIR=$(echo $OUTPUT | grep -Po '"project_dir":\s*"\K[^"]*')
  echo "GM/Build project_dir: $PROJECT_DIR"
fi

# Inspect as needed
# tests/utilities/json_ripper.py --json_file ct-output-git-ignore-me.json entity
# cat ct-output-git-ignore-me.json

