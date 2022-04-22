#!/bin/bash

printf "\n!!!NOTICE!!!\n
Please note that this will only clean the GEMS layer
If one wants to clean the GMML layer, please go into that
directory and, if the cmakeBuild directory exists (and the
Makefile exists), cd into cmakeBuild and run make clean.\n
We do not want to have different layers cleaning files that
are not their own.\n\n"

if [ -f ./gmml.py ];then
	echo "Removing gmml.py in GEMS directory"
	rm ./gmml.py
fi
if [ -f ./_gmml.so ]; then
	echo "Removing _gmml.so in GEMS directory"
	rm ./_gmml.so
fi

printf "Note that GMML has not been touched from this script.
To remove or clean gmml refer to the notice above.\n"
