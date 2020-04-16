#!/bin/bash
THISPYTHON='python3'
##################### Test 7 ########################
echo "Testing DrawGlycan.py..."
#Runs the script that is being tested.
${THISPYTHON} $GEMSHOME/bin/DrawGlycan.py LFucp[2S]b1-6[DGlcpNAc[3A]a1-2]DManp[3A]a1-3[DGalpNAc[6Me]a1-4]DGalpNAc[6S]b1-OME
DIFF=$(diff drawglycan.dot correct_outputs/test7_output 2>&1)
if [ "$D0IFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm drawglycan.dot
    return 0;
fi
