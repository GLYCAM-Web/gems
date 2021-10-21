#!/bin/bash

# Tests should pertain to PDB 

# python script to compare test output
evaluate_PDB_py=$GEMSHOME/testbin/evaluatePDB.py

# JSON INPUTS
evaluate_PDB_Json=$GEMSHOME/gemsModules/delegator/test_in/pdb/evaluatePdb.json

# path to test10_output
correct_PDB_Output=$GEMSHOME/tests/correct_outputs/test10_output 

run_evalute_sideload_PDB_test()
{
	echo "TODO"
}

# invoke delegator with an uploaded pdb file
# compare test output to known good output
run_evaluate_upload_PDB_test()
{
	# pipe .json input to delegator; redirect to f
	cat $evaluate_PDB_Json | $GEMSHOME/bin/delegate > f
	# pass f and test10_output to the compare script
	$evaluate_PDB_py f $correct_PDB_Output
	# exit code from evaluate_PDB_py
	isValid=$?
	# clean up
	rm f

	if [ $isValid  != '0' ] ; then
		return 1
	fi

	return 0
}

if run_evaluate_upload_PDB_test; then
	echo "010a -- run_evaluate_upload_PDB_test passed"
else
	echo "010a -- run_evaluate_upload_PDB_test failed"
	echo "010a -- exiting"
	exit 1
fi

echo "All 010 tests passed"
exit 0

