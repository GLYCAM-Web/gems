#!/bin/bash
##################### Test 8 ########################
echo "Testing delegator with sequence, which takes around 30 seconds..."
#Runs the script that is being tested.
run_newBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > out.json
	sleep 20s # Wait for it to be generated.
	ls $currentOutput
	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test FAILED!"
    	return 1;
	else
    	echo "Test passed."
    	rm out.json
    	return 0;
    fi
}

run_existingBuild_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > out.json
	if ! grep -q $correctOutput $currentOutput; then
		echo "Test for Existing_Builds FAILED!"
    	return 1;
	else
    	echo "Test passed."
    	rm out.json
    	return 0;
    fi
}
################### MAIN #########################
#First remove all outputs in Builds and Sequences to test New_Builds functionality
rm -r $GEMSHOME/../../website/userdata/tools/cb/git-ignore-me_userdata/Sequences/*
rm -r $GEMSHOME/../../website/userdata/tools/cb/git-ignore-me_userdata/Builds/*
#Inputs for new Build
inputJson=$GEMSHOME/gemsModules/delegator/test_in/sequence/build_sequence_with_selected_rotamersAlt.json 
sequenceID=57f51b27-9325-5c41-85d0-ef1bb0aecc6f
currentOutput=$GEMSHOME/../../website/userdata/tools/cb/git-ignore-me_userdata/Sequences/$sequenceID/current/All_Builds/default/structure.pdb
correctOutput=correct_outputs/test008_output_subTest1.pdb
if ! run_newBuild_test; then
	return 1;
fi
correctOutput="6ht_otg_9ht_ogt_10ogt_13ht_otg_14ogt_16ht_ogt"
currentOutput=out.json
if ! run_existingBuild_test; then
	return 1;
else
	return 0;
fi