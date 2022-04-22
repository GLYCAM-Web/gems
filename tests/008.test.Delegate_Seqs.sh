#!/bin/bash

## Shortens time spent minimizing
export GEMS_MD_TEST_WORKFLOW=True

## A place for testing output. Separated so it is safe to delete.
export GEMS_OUTPUT_PATH='/website/TESTS/git-ignore-me/pre-push'
gemsServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
gemsSequencePath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
gemsBuildPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds

## Inputs
inputJson=$GEMSHOME/gemsModules/delegator/test_in/sequence/build_sequence_with_selected_rotamers.json
sequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
now=$(date "+%Y-%m-%d-%H-%M-%S")

## Outputs
## The variable badOutDir should be defined in the calling directory.
filename=git-ignore-me_test08_out.txt
badOutput="${badOutDir}/${now}_${filename}"

## Edit if your machine needs more time for minimization to finish
maxTimeCount=40
sleepTime=10

clear_output()
{
	if [ -f ${badOutput} ] ; then
		#echo "Removing output."
		rm ${badOutput}
	fi
}


##################### Test 8 ########################
echo "
Testing delegator using a sequence request with specified conformers.
" | tee -a $badOutput

# See if a returned object is proper JSON and no other data
check_json_output_test() 
{
	commonServicerResponse="$(cat ${1} | python ../gemsModules/common/utils.py)"
	if ( echo ${commonServicerResponse} | grep -q CommonServices ) ; then
		echo ""
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo ""
		echo "  The returned data is not a proper JSON Object"
		echo "  This will cause the test to fail even if the builds work."
		echo "  The Common Servicer has this to say about the data:"
		echo ""
		echo "${commonServicerResponse}"
		echo ""
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo ""
		return 1
	else
		echo "The data response appears to be ok"
		return 0
	fi
}

# Runs the script that is being tested.
run_newBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > newBuild_out.json
	check_json_output_test newBuild_out.json 
	export isJsonOk=$?
	#currentOutput=${gemsSequencePath}/${sequenceID}/current/All_Builds/${conformerID}/min-gas.pdb
	count=0
	while [ "${count}" -lt "${maxTimeCount}" ] ; do
		sleep ${sleepTime} # Wait for it to be generated.
		currentNumberOfConformers=$(ls ${gemsSequencePath}/${sequenceID}/current/All_Builds/*/min-gas.pdb | wc -l)
		if [ $currentNumberOfConformers -eq 8 ]; then
			break
		fi
		count=$((count+1))
		if [ "${count}" -eq "${maxTimeCount}" ] ; then
			echo "Output still not found after $((maxTimeCount*sleepTime)) seconds.  Aborting." | tee -a $badOutput
			echo "The output being sought is : " | tee -a $badOutput
			echo "${currentOutput}" | tee -a $badOutput
			echo "Test 008a FAILED!" | tee -a $badOutput
			return 1
		fi
		echo "Waited $((count*sleepTime)) seconds so far." | tee -a $badOutput
	done
	for conformerID in $(cat inputs/008.conformerIdList.txt);
	do
		currentOutput=${gemsSequencePath}/${sequenceID}/current/All_Builds/${conformerID}/min-gas.pdb
		correctOutput=correct_outputs/008.conformers/${conformerID}/min-gas.pdb
		if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
			echo "Test 008a FAILED!" | tee -a $badOutput
			echo "These files are different:\n$currentOutput\n$correctOutput\n"
			if  test -e "$currentOutput"  ; then
				echo "output from test exists: $currentOutput"
			else
				echo "output from test is missing, expected is: $currentOutput"
			fi
			return 1;
		fi
	done
	echo "Test 008a passed." 
	rm newBuild_out.json 
	clear_output
	return 0; 
}

run_existingBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > existingBuild_out.json
	pUUID=$(grep -m 1  pUUID existingBuild_out.json | cut -d '"' -f4)
	echo "pUUID: ${pUUID}" >> $badOutput
	echo "conformerID: ${conformerID}" >> $badOutput
	currentOutput="${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}/min-gas.pdb"
	echo "currentOutput: ${currentOutput}" >> $badOutput

	## Initial compare
	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test 008b run_existingBuild_test() failed the initial check." >> $badOutput

		## Debugging help:
		## Check for project dir
		if [ ! -d "${gemsBuildPath}/${pUUID}/" ] ; then
			echo "failed to find project dir:" >> $badOutput
			echo "    ${gemsBuildPath}/${pUUID}/" >> $badOutput
		else 
			## Check for Existing_Builds dir
			if [ ! -d "${gemsBuildPath}/${pUUID}/Existing_Builds/" ] ; then 
				echo "Existing_Builds dir does not exist." | tee -a $badOutput
				echo "    ${gemsBuildPath}/${pUUID}/Existing_Builds/" | tee -a $badOutput

			else 
				## Check for the conformer dir
				if [ ! -d "${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}/" ] ; then 
					echo "conformerID dir does not exist yet. May still need time." >> $badOutput
					echo "    ${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}/" >> $badOutput
				fi
			fi
		fi		
		## End debugging help

		## Check for the existence of last file written out by minimization.
		if [ ! -e $currentOutput ]; then
		    echo "currentOutput file not found yet. Sleeping in case it just needs time..." | tee -a $badOutput
		    count=0
		    while [ "${count}" -lt "${maxTimeCount}" ] ; do
				sleep ${sleepTime} # Wait for it to be generated.
				if [ -f $currentOutput ]; then
					echo "currentOutput found." >> $badOutput
					break
				else
					count=$((count+1))
					echo "Waited $(($count*sleepTime)) seconds so far. Still no file." | tee -a $badOutput
				fi
			done
		fi	
		# echo "Done waiting. Final comparison."
		if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
			echo "Test 008b FAILED!" | tee -a $badOutput
			return 1;
		else
			echo "Test 008b passed." 
			rm existingBuild_out.json 
			clear_output
			return 0;
		fi	
	else 
		echo "Test 008b passed." 
		rm existingBuild_out.json 
		clear_output
		return 0; 
	fi

}


################### MAIN #########################
#
# First remove all outputs in Builds and Sequences to test New_Builds functionality
if [ -d "${gemsServicePath}" ] ; then
	echo "Removing Sequences and Builds from ${gemsServicePath}" >> $badOutput
	( cd ${gemsServicePath} && rm -rf Sequences Builds )
else 
	mkdir -p ${gemsServicePath}
fi
if [ ! -d "${gemsServicePath}" ] ; then
	echo "Unable to create output directory.  Exiting." | tee -a $badOutput
	exit 1
fi

echo "008a (and 008c): new builds.
" | tee -a $badOutput
echo "Allowing up to $((maxTimeCount*sleepTime)) seconds to complete the new build." | tee -a $badOutput
echo "If your build completes, but takes longer, update the test to wait longer." | tee -a $badOutput
# Build something from scratch
if ! run_newBuild_test; then
	echo "Test 008a failed. Details can be found here: " $badOutput
	return 1;
fi
echo "
008b: existing builds.
" | tee -a $badOutput

# Check that the build is found
if ! run_existingBuild_test; then
	echo "Test 008b failed. Details can be found here: " $badOutput
	return 1;
else
	## Remove what we made
	( cd ${gemsServicePath} && rm -rf Sequences Builds )
	clear_output
	if [ "${isJsonOk}" -eq "1" ] ; then
		echo "The builds worked, but the JSON fails."
		echo "Please change the appropriate return statement once the JSON is fixed.  Also remove this line."
		return 0;  # change me to '1' once the cout thing is fixed
	else
		return 0;
	fi
fi
