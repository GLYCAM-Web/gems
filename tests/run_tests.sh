#!/bin/bash

THISPYTHON='python3'

#Manually change this number as you add tests:
number_of_tests=4
tests_passed=0

##################### Test 1 ########################
echo "Testing detect_sugar..."
#Runs the script that is being tested
cd $GEMSHOME #detect sugars has hardcoded path to apps/BFMP/detect_shape in GMML::Assembly.ExtractSugars.
${THISPYTHON} ./bin/detect_sugars $GEMSHOME/tests/inputs/1NXC.pdb > $GEMSHOME/tests/test1_output
cd - >> /dev/null 2>&1 #return now to reduce chance of forgetting later
DIFF=$(diff test1_output correct_outputs/test1_output) 
if [ "$DIFF" != "" ]; then
    echo "Test failed"
else
    echo "Test passed."
    ((tests_passed++))
fi
rm test1_output


##################### Test 2 ########################
echo "Testing PDBSugarID..."
#runs the script with a functional argument
cd $GEMSHOME
${THISPYTHON} ./bin/PDBSugarID $GEMSHOME/tests/inputs/1NXC.pdb $GEMSHOME/tests/test2_output keep
cd - >> /dev/null 2>&1
tail -n +18 test2_output >> tmp2
DIFF=$(diff tmp2 correct_outputs/test2_output)
if [ "$DIFF" != "" ]; then
    echo "Test failed"
else
    echo "Test passed."
    ((tests_passed++))
fi
rm tmp2
rm test2_output
rm test2_output_sugar-details


##################### Test 3 ########################
echo "Testing test_installation.bash..."
cd $GEMSHOME
./test_installation.bash > $GEMSHOME/tests/test3_output
cd - >> /dev/null 2>&1
DIFF=$(diff test3_output correct_outputs/test3_output)
if [ "$DIFF" != "" ]; then
    echo "Test failed"
else
    echo "Test passed."
    ((tests_passed++))
fi
rm test3_output

##################### Test 4 ########################
echo "Testing test_installation.py..."
#Tests one of the commands that this script has
${THISPYTHON} ../test_installation.py "--help" > test4_output
DIFF=$(diff test4_output correct_outputs/test4_output)
if [ "$DIFF" != "" ]; then
    echo "Test failed"
else
    echo "Test passed."
    ((tests_passed++))
fi
rm test4_output
 
##################### Test 5 ########################
#echo "Testing GMMO query 1..."
##Tests one of the commands that this script has
#python3 ../testbin/query1_ExtractOntologyInfoByNameOfGlycan.py > test5_output
#DIFF=$(diff test5_output correct_outputs/test5_output)
#if [ "$DIFF" != "" ]; then
#    echo "Test failed"
#else
#    echo "Test passed."
#    ((tests_passed++))
#fi
##rm test5_output

##################### Test 6 ########################
#echo "Testing GMMO query 2..."
##Tests one of the commands that this script has
#python3 ../testbin/query3_ExtractOntologyInfoByPDBID.py > test6_output
#DIFF=$(diff test6_output correct_outputs/test6_output)
#if [ "$DIFF" != "" ]; then
#    echo "Test failed"
#else
#    echo "Test passed."
#    ((tests_passed++))
#fi
##rm test6_output


############# Allow git Pushes ###################
if [[ $tests_passed == $number_of_tests ]]; then
    exit 0
    echo "All tests passed"
else
    exit 1
fi

