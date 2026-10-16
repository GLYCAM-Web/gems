#!/bin/bash
THISPYTHON='python3'
echo "Testing $0 (AntibodyDocking Interface-Only)..."

if [ -z "$GEMSHOME" ]; then
    echo "GEMSHOME not set, defaulting to /programs/gems"
    GEMSHOME="/programs/gems"
fi

${THISPYTHON} ${GEMSHOME}/gemsModules/complex/antibody/tests/test_ad_data_flow.py
TEST_RESULT=$?

if [ ${TEST_RESULT} -ne 0 ]; then
    echo "AntibodyDocking Interface-Only Tests FAILED!"
    return 1 2>/dev/null || exit 1
else
    echo "AntibodyDocking Interface-Only Tests passed."
    return 0 2>/dev/null || exit 0
fi
