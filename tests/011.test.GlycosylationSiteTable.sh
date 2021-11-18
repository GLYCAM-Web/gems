#!/bin/bash
THISPYTHON='python3'
echo "Testing GlycosylationSiteTable.py..."
#Runs the script that is being tested.
${THISPYTHON} $GEMSHOME/bin/GlycosylationSiteTable.py $GEMSHOME/gmml/tests/tests/inputs/4mbz_NoWat_NoConect_NoAnisou.pdb > test011_output.txt
DIFF=$(diff test011_output.txt correct_outputs/test011_output.txt 2>&1)
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm test011_output.txt
    return 0;
fi
