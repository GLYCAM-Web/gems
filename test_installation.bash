#!/bin/bash

if [ "$(which python3)" == "" ] ; then
	echo "

TEST FAILURE:

	You need python3 to use this version of GEMS.

"
	exit
fi

if [ ! -d "gmml" ] ; then
	echo "

TEST FAILURE:

	You need gmml to use GEMS.  
	It must be in a sub-directory of GEMS to run this test.

"
	exit
fi


for i in test_installation.py gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep gmml/example/pdb/Small_to_test.pdb test_pdb.txt.save ; do 
	if [ ! -e "${i}" ] ; then
		echo "

TEST FAILURE:
	
	Cannot find the file ${i}

"
		exit
	fi
done

echo "

This test should take less than 10 seconds to run on most modern computers.

This test will compare these files:

	updated_pdb.txt      --   this is the file the test should generate
	test_pdb.txt.save    --   this is the file to which it should be identical


Beginning test.
"

python3 test_installation.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -prep "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -pdb "gmml/example/pdb/Small_to_test.pdb" > testing.log 2> testing.error

echo "

Checking for diffeences between test output and the standard output.
"

if [ ! -e "updated_pdb.txt" ] ; then
	echo "
TEST FAILURE:

	The file called updated_pdb.txt was not generated.  This probably means there
	is something terribly wrong with your installation.
	
	Please check the contents of the following files to determine the problem:
	
	testing.log
	testing.error

TEST FAILURE
"
	exit

fi

OUTPUT="$(diff test_pdb.txt.save updated_pdb.txt | tee Difference_Test.log)"

if [ "$OUTPUT" != "" ] ; then 
	echo "

TEST FAILURE:

	There are differences between the saved file and the one the test just generated.
	
	Please check the contents of the following files to determine the problem:
	
	Difference_Test.log 
	testing.log
	testing.error

TEST FAILURE
"
else
	echo "

The test passed.

"
	rm testing.log testing.error updated_pdb.txt Difference_Test.log
fi
