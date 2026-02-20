#!/usr/bin/env bash
. './utilities/common_environment.bash'
. './utilities/functions.bash'

echo "The output path is: ${GEMS_OUTPUT_PATH}"

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test020'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutputDir="${badOutDir}/${now}_${outputFilePrefix}_Files"
mkdir -p "${badOutputDir}"

ALL_TESTS_PASSED='true'

echo "Testing Glycomimetics"

#rm -f test-20-output-git-ignore-me.json
#rm -f test-20-invalid-output-git-ignore-me.json

# Run the test
#TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/entity_evaluate.json"
#TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/explicit_evaluate.json"
TEST_INPUT="/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/explicit_build.test.json"

#OUTPUT=$(/programs/gems/bin/delegate $TEST_INPUT)
# same as above, but capture stderr seprately
### THERE SHOULD BE NO STDERR
StdErrOut="${badOutputDir}/delegate_out.stderr"
echo "StdErrOut is ${StdErrOut}"
COMMAND="/programs/gems/bin/delegate $TEST_INPUT 2> \"${StdErrOut}\""
echo "COMMAND is ${COMMAND}"
#OUTPUT="$(/programs/gems/bin/delegate $TEST_INPUT 2> "${StdErrOut}")"
OUTPUT="$(eval ${COMMAND})"
echo $OUTPUT >  ${badOutputDir}/test-20-delegation_output.json

# TODO - Make this not silently exit on failure. Add hints about what failed and why.
# Check the output is a valid JSON
echo $OUTPUT | python -m json.tool > ${badOutputDir}/test-20-check-json-format.json
if [ $? -ne 0 ]; then
  echo "Output is not a valid JSON"
  return 1
else
  # Check that Evaluation worked.
  echo $OUTPUT | grep "Evaluation Successful" > ${badOutputDir}/test-20-check-evaluation-response.txt
  if [ $? -ne 0 ]; then
  	echo "Evaluation Failed"
  	return 1
  fi

  # Check that Build is running.
  echo $OUTPUT | grep "Glycomimetics is running" > ${badOutputDir}/test-20-check-gm-is-running.txt
  if [ $? -ne 0 ]; then
  	echo "Glycomimetics is not running"
  	return 1
  fi


  # grab "projectect_dir": "<dir>" with grep
  PROJECT_DIR=$(echo $OUTPUT | grep -Po '"project_dir":\s*"\K[^"]*')
  echo "GM/Build project_dir: $PROJECT_DIR"
fi

return 0

# Inspect as needed
# tests/utilities/json_ripper.py --json_file ct-output-git-ignore-me.json entity
# cat ct-output-git-ignore-me.json

