#!/bin/bash

export GEMS_MD_TEST_WORKFLOW=True
export GEMS_OUTPUT_PATH='/website/TESTS/git-ignore-me/pre-push'
gemsServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
gemsSequencePath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
gemsBuildPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds
inputJson=$GEMSHOME/gemsModules/delegator/test_in/sequence/build_sequence_with_selected_rotamers.json
sequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
conformerID='caec5dc2-05f8-582a-b76a-f2be379ece8d'
correctOutput=correct_outputs/test008_output_subTest1.pdb
maxCount=30
sleepTime=10

##################### Test 8 ########################
echo "
Testing delegator using a sequence request with specified conformers.
"
# Runs the script that is being tested.
run_newBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > out1.json
	currentOutput=${gemsSequencePath}/${sequenceID}/current/All_Builds/${conformerID}/min-t5p.pdb
	count=0
	while [ "${count}" -lt "${maxCount}" ] ; do
		sleep ${sleepTime} # Wait for it to be generated.
		if [ -e  "${currentOutput}" ] ; then
			break
		fi
		count=$((count+1))
		if [ "${count}" -eq "${maxCount}" ] ; then
			echo "Output still not found after 300 seconds.  Aborting."
			echo "The output being sought is : "
			echo "${currentOutput}"
			echo "Test 008.a FAILED!" 
			return 1
		fi
		echo "Waited $((count*sleepTime)) seconds so far."
	done
	if ! cmp $currentOutput $correctOutput > newBuildCompare.txt; then
		echo "Test 008.a FAILED!" 
		return 1;
	else 
		echo "Test 008.a passed." 
		rm out.json 
		return 0; 
	fi
}

run_existingBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > out2.json
	pUUID=$(grep -m 1  pUUID out.json | cut -d '"' -f4)
	currentOutput="${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}/min-t5p.pdb"


	if ! cmp $currentOutput $correctOutput > existingBuildCompare.txt; then
		echo "Test 008.b FAILED!" 
		return 1;
	else 
		echo "Test 008.b passed." 
		rm out.json 
		return 0; 
	fi
}
################### MAIN #########################
#
# First remove all outputs in Builds and Sequences to test New_Builds functionality
if [ -d "${gemsServicePath}" ] ; then
	echo "Removing Sequences and Builds from ${gemsServicePath}"
	( cd ${gemsServicePath} && rm -rf Sequences Builds )
else 
	mkdir -p ${gemsServicePath}
fi
if [ ! -d "${gemsServicePath}" ] ; then
	echo "Unable to create output directory.  Exiting."
	exit 1
fi

echo "
008.a Checking that new builds work properly.
"
echo "Allowing up to $((maxCount*sleepTime)) seconds to complete the new build."
echo "If your build completes, but takes longer, update the test to wait longer."
# Build something from scratch
if ! run_newBuild_test; then
	return 1;
fi
echo "
008.b Checking now that existing builds are found.
"

# Check that the build is found
if ! run_existingBuild_test; then
	return 1;
else
	## Remove what we made
	( cd ${gemsServicePath} && rm -rf Sequences Builds )
	return 0;
fi
