#!/usr/bin/env bash

USAGE="""
\n
Usage :\n
\n
\t ${0} [-h] [PORT] \n
\n
where PORT is an optional port nubmer and entering '-h' will show\n
this message.  These two options are mutually exclusive.  You will\n
get whichever one comes first and not the other.\n
\n
The output from the script will tell you how to view the docs.\n
\n
\n
# Prerequisites\n
\n
You must first install mkdocs.  You can typically do this\n
using your OS's installer, e.g., 'apt install mkdocs'.\n
\n
Then, from the GEMSHOME directory, run this script again:\n
\n
\n
# Updating the Docs\n
\n
These docs use the MkDocs system.  The configuration file\n
is mkdocs.yml and the source files are in the docs\n
directory.  Adter running this script,  site will be \n
created.  This directory is git-ignored.  Changes made to \n
the configuration file or to files in the docs directory\n
are generally updated immediately in the site you will\n
will find at the URL shown when you run the script.\n
\n
## More Info\n
\n
See the MkDocs documentation at https://www.mkdocs.org/\n
"""

if ! command -v mkdocs &> /dev/null
then
    echo ""
    echo "The mkdocs executable could not be found.  Exiting."
    echo -e  ${USAGE}
    exit
fi

if [ "${1}" == "-h" ] ; then
	echo -e  ${USAGE}
	exit
fi

thePort='58051'

if [ "${1}zzz" != "zzz" ] ; then
	thePort=${1}
fi

echo """
About to run mkdocs serve

To view the docs, in the URL bar of your browser type:

     127.0.0.1:${thePort}

"""
mkdocs serve -a 127.0.0.1:${thePort}
