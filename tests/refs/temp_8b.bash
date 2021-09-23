#!/bin/bash

export GEMS_MD_TEST_WORKFLOW=True
export GEMS_OUTPUT_PATH='/website/TESTS/git-ignore-me/pre-push'
gemsServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
gemsSequencePath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
gemsBuildPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds
inputJson=$GEMSHOME/gemsModules/delegator/test_in/sequence/build_sequence_with_selected_rotamers.json
sequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
conformerID='caec5dc2-05f8-582a-b76a-f2be379ece8d'
correctOutput=${GEMSHOME}/tests/correct_outputs/test008_output_subTest1.pdb
maxCount=12
sleepTime=5

##################### Test 8 ########################
echo "
Testing delegator using a sequence request with specified conformers.
"
run_existingBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > git-ignore-me_temp_out_8b.json
	pUUID=$(grep -m 1  pUUID git-ignore-me_temp_out_8b.json | cut -d '"' -f4)

	echo "Trying to get the symlnked file the original way"
	currentOutput="${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}/min-t5p.pdb"
	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test FAILED!" 
	else 
		echo "Test passed." 
	fi

	echo "Trying to get the symlnked file from the Existing Builds cirectory"
	echo "changing dir to :"
	echo "${gemsBuildPath}/${pUUID}/Existing_Builds/"
	cd "${gemsBuildPath}/${pUUID}/Existing_Builds/"
	echo "Listing long:"
	ls -la 
	currentOutput="${conformerID}/min-t5p.pdb"


	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test FAILED!" 
	else 
		echo "Test passed." 
	fi

	echo "Trying to get the symlnked file from the conformerID cirectory"
	echo "changing dir to :"
	echo "${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}"
	cd "${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}"
	echo "Listing long:"
	ls -la 
	currentOutput="min-t5p.pdb"
	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test FAILED!" 
		echo "currentOutput:"
		echo $currentOutput
	else 
		echo "Test passed." 
	fi
}
################### MAIN #########################
#
echo "
Checking now that existing builds are found.
"
# Check that the build is found
run_existingBuild_test


##TODO: Maintain function, but add wait.
##		- check for error file, remove it.
##		- add to the real test (watch sleep times.)
##		- on fail, send output to file - use timestamp $(date)
##		- delete output if pass