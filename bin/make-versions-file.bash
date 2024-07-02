#!/usr/bin/env bash
#
# This can be called from anywhere, but the following
#    must be accessible and writable.
#
#    ${GEMSHOME}
#    ${GEMSHOME}/gmml
# 
echo "Getting and setting Versions info."

##  Set the GEMS info
echo "...GEMS"
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
echo "...GMML"
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
echo "...MD_Utils"
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

## Set and get the GM_Utils info
echo "...GM_Utils"
if ! cd "${GEMSHOME}/External/GM_Utils" ; then
	echo "Could not cd to GEMSHOME/GM_Utils directory"
	echo "Cannot complete acquisition of versions info."
	exit 1
fi
if ! ./scripts/make-versions-file.bash ; then
	echo "Could not generate GM_Utils versions file"
	echo "Cannot complete acquisition of versions info."
	exit 1
fi
if ! cd ${GEMSHOME} ; then
        echo "Could not cd to GMSHOME directory the fourth time"
        echo "How did this even happen?"
	exit 1
fi
cat External/GM_Utils/VERSIONS.sh >> VERSIONS.sh

echo "VERSIONS.sh is finished."


