#!/usr/bin/env bash

if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo "GEMSHOME must be defined to use this test.  Exiting."
	exit 1
fi

( cd $GEMSHOME && bash logs/clearLogs.sh )

unset GEMS_LOGGING_LEVEL
python3 ensure_logging_works.py

export GEMS_LOGGING_LEVEL='error'
python3 ensure_logging_works.py

export GEMS_LOGGING_LEVEL='info'
python3 ensure_logging_works.py

export GEMS_LOGGING_LEVEL='debug'
python3 ensure_logging_works.py

dirhere=$(pwd -P)

#echo "dirhere is ${dirhere}"

expected_errors_counts="logs/git-ignore-me_gemsDebug.log:4
logs/git-ignore-me_gemsError.log:4
logs/git-ignore-me_gemsInfo.log:3"

cd $GEMSHOME 
errors_counts="$(grep -c ERROR logs/git-ignore-me_gems*)"

if [ "${errors_counts}" != "${expected_errors_counts}" ] ; then
	echo "Test Failed!"
	echo "Please see the contents of GEMSHOME/logs/ for more info.  See also below."
        echo "errors_counts is >>>${errors_counts}<<<"
        echo "expected_errors_counts is >>>${expected_errors_counts}<<<"
else 
	echo "Test Passed!"
        bash logs/clearLogs.sh
fi


