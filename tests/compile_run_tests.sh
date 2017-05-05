#!/bin/bash

#Manually change this number as you add tests:
number_of_tests=4
tests_passed=0

##################### Test 1 ########################
echo "Testing detect_sugar..."
#Runs the script that is being tested
detect_sugars inputs/1NXC.pdb > output_test
if [ -f output_test ]; then
   if [ `diff output_test correct_outputs/outfile_detect_sugars` ]; then
	printf "Test failed.\n"
   else
	echo "Test passed."
	((tests_passed++))
   fi
else
   printf "Test failed.\n"
fi
rm output_test


##################### Test 2 ########################
echo "Testing PDBSugarID..."
#runs the script with a functional argument
PDBSugarID inputs/1NXC.pdb test_output keep
if [ -f test_output ]; then
  if [ `diff test_output correct_outputs/Outfile` ]; then
   printf "Test failed.\n"
  else
   echo "Test passed."
    ((tests_passed++))
  fi
else
  printf "Test failed.\n"
fi
rm test_output
rm test_output_sugar-details


##################### Test 3 ########################
echo "Testing test_installation.bash..."
TEST="$(../test_installation.bash)"
#The script's built-in test
if [ "$TEST" != "$OUTPUT" ]; then
   if [ "$OUTPUT" != "" ]; then
        printf "Test failed.\n"
   else
        echo "Test passed."
          ((tests_passed++))
fi
else
   printf "Test failed.\n"
fi


##################### Test 4 ########################
echo "Testing test_installation.py..."
#Tests one of the commands that this script has
OUTPUT="$(python3.4 ../test_installation.py "--help")"
if [ "$OUTPUT" == "" ]; then
	printf "Test failed.\n"
else
	echo "Test passed."
 	  ((tests_passed++))
fi


############# Allow git commits ###################
if [[ $tests_passed == $number_of_tests ]]; then
   > All_Tests_Passed 
fi
