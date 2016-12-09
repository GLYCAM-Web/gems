#!/bin/bash

#Probably the most common error for this script
if [ "$PYTHON_HOME" = "" ] ; then
echo  "

	 Set PYTHON_HOME to the location of the Python.h file for your
         version of python.

	(For Ubuntu users, you could literally copy paste this and that 
	should usually fix it)

                export PYTHON_HOME=/usr/include/python3.4  
"

exit 1
fi

#source "/home/hussain/gems/gems/make.sh"
