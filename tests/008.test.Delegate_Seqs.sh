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
conformerID='caec5dc2-05f8-582a-b76a-f2be379ece8d'
correctOutput=correct_outputs/test008_output_subTest1.pdb
now=$(date "+%Y-%m-%d-%H-%M-%S")

## Outputs
filename=git-ignore-me_test08_out.txt
badOutput="bad_outputs/"$now"_"$filename

## Edit if your machine needs more time for minimization to finish
maxCount=40
sleepTime=10

clear_output()
{
	if [ -f $badOutput ] ; then
		#echo "Removing output."
		rm $badOutput
	fi
}


##################### Test 8 ########################
echo "
Testing delegator using a sequence request with specified conformers.
" | tee -a $badOutput


# Runs the script that is being tested.
run_newBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > newBuild_out.json
	currentOutput=${gemsSequencePath}/${sequenceID}/current/All_Builds/${conformerID}/min-t5p.pdb
	count=0
	while [ "${count}" -lt "${maxCount}" ] ; do
		sleep ${sleepTime} # Wait for it to be generated.
		if [ -e  "${currentOutput}" ] ; then
			break
		fi
		count=$((count+1))
		if [ "${count}" -eq "${maxCount}" ] ; then
			echo "Output still not found after $((maxCount*sleepTime)) seconds.  Aborting." | tee -a $badOutput
			echo "The output being sought is : " | tee -a $badOutput
			echo "${currentOutput}" | tee -a $badOutput
			echo "Test 008a FAILED!" | tee -a $badOutput
			return 1
		fi
		echo "Waited $((count*sleepTime)) seconds so far." | tee -a $badOutput
	done
	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test 008a FAILED!" | tee -a $badOutput
		return 1;
	else 
		echo "Test 008a passed." 
		rm newBuild_out.json 
		clear_output
		return 0; 
	fi
}

run_existingBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > existingBuild_out.json
	pUUID=$(grep -m 1  pUUID existingBuild_out.json | cut -d '"' -f4)
	echo "pUUID: ${pUUID}" >> $badOutput
	echo "conformerID: ${conformerID}" >> $badOutput
	currentOutput="${gemsBuildPath}/${pUUID}/Existing_Builds/${conformerID}/min-t5p.pdb"
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
		    while [ "${count}" -lt "${maxCount}" ] ; do
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

echo "008a: new builds.
" | tee -a $badOutput
echo "Allowing up to $((maxCount*sleepTime)) seconds to complete the new build." | tee -a $badOutput
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
	return 0;
fi
