#!/usr/bin/env bash
#
# This can be called from anywhere, but the following
#    must be accessible and writable.
#
#    ${GEMSHOME}
#    ${GEMSHOME}/gmml
# 

##  Set the GEMS info
if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo "GEMSHOME must be set."
	exit 1
fi
if ! cd ${GEMSHOME} ; then
        echo "Could not cd to GMSHOME directory"
	exit 1
fi
echo """
GEMS_GIT_BRANCH=\"$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')\"
GEMS_GIT_COMMIT_HASH=\"$(git rev-parse HEAD)\"
""" > VERSIONS.sh

## Set and get the GMML info
if ! cd "${GEMSHOME}/gmml" ; then
	echo "Could not cd to GEMSHOME/gmml directory"
	echo "Cannot complete acquisition of versions info."
	exit 1
fi
if ! ./make-versions-file.bash ; then
	echo "Could not generate gmml versions file"
	echo "Cannot complete acquisition of versions info."
	exit 1
fi
if ! cd ${GEMSHOME} ; then
        echo "Could not cd to GMSHOME directory the second time"
        echo "How did this even happen?"
	exit 1
fi
cat gmml/VERSIONS.sh >> VERSIONS.sh

## Set and get the MD_Utils info
if ! cd "${GEMSHOME}/External/MD_Utils" ; then
	echo "Could not cd to GEMSHOME/MD_Utils directory"
	echo "Cannot complete acquisition of versions info."
	exit 1
fi
if ! ./scripts/make-versions-file.bash ; then
	echo "Could not generate MD_Utils versions file"
	echo "Cannot complete acquisition of versions info."
	exit 1
fi
if ! cd ${GEMSHOME} ; then
        echo "Could not cd to GMSHOME directory the third time"
        echo "How did this even happen?"
	exit 1
fi
cat External/MD_Utils/VERSIONS.sh >> VERSIONS.sh


