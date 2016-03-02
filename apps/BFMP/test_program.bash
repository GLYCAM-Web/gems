#!/bin/bash
if [ ! -e detect_shape ] ; then
	echo "The executable detect_shape does not exist.  Have you
run make yet?  Exiting"
	exit
fi

if [ ! -d test_directory ] ; then
	echo "The test directory appears not to exist.  This is unexpected,
and I cannot run a test unless it exists."
	exit
fi

cd test_directory

echo "Testing the PDB function.  Output from the run follows.
================================================================
" > test_results_PDB
../detect_shape 1AXM.pdb input_PDB >> test_results_PDB 2>&1
output=$(diff ring_conformations.txt_save_PDB ring_conformations.txt)
if [ "${output}" != "" ] ; then
	echo "A file made by the program appears to be incorrect.  Please
check the files diffs_PDB and test_results_PDB in the test_directory folder
for more information" 
	echo ${output} > diffs_PDB
	mv ring_conformations.txt ring_conformations.txt_failed_PDB
else
	echo "The program has passed for the PDB file."
	rm ring_conformations.txt
fi

echo "Testing the traj function.  Output from the run follows.
================================================================
" > test_results_traj
../detect_shape IdoA.prmtop IdoA.crd input_traj >> test_results_traj 2>&1
output=$(diff ring_conformations.txt_save_traj ring_conformations.txt)
if [ "${output}" != "" ] ; then
	echo "A file made by the program appears to be incorrect.  Please
check the files diffs_traj and test_results_traj in the test_directory folder
for more information" 
	echo ${output} > diffs_traj
	mv ring_conformations.txt ring_conformations.txt_failed_traj
else
	echo "The program has passed for the traj file."
	rm ring_conformations.txt
fi
