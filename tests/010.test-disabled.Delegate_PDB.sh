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
echo "1"
$evaluate_PDB_py f $correct_PDB_Output
echo "1"

echo "2"
$evaluate_PDB_py f f
echo "2"

echo "3"
$evaluate_PDB_py $correct_PDB_Output $correct_PDB_Output
echo "3"

# clean up
rm f

exit 1

