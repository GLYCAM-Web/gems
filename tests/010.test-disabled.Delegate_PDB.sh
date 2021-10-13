#!/bin/bash

# Tests should pertain to PDB 

# python script to compare test output
evaluate_PDB_py=$GEMSHOME/testbin/evaluatePDB.py

# JSON INPUTS
evaluate_PDB_Json=$GEMSHOME/gemsModules/delegator/test_in/pdb/evaluatePdb.json

# path to test10_output
correct_PDB_Output=$GEMSHOME/tests/correct_outputs/test10_output 

# pipe .json input to delegator; redirect to f
cat $evaluate_PDB_Json | $GEMSHOME/bin/delegate > f

# pass f and test10_output to the compare script
echo "here"
$evaluate_PDB_py f $correct_PDB_Output
echo "there"
# clean up
rm f

exit 1

