#!/usr/bin/env bash
echo "Getting and setting Versions info."

##  Check GEMSHOME is set and is an accessible directory.
echo "...GEMS"
if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo "GEMSHOME must be set."
	exit 1
fi
if ! cd ${GEMSHOME} ; then
        echo "Could not cd to \$GEMSHOME directory: $GEMSHOME"
	exit 1
fi
## Set the GEMS version info
echo """
GEMS_GIT_BRANCH=\"$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')\"
GEMS_GIT_COMMIT_HASH=\"$(git rev-parse HEAD)\"
""" > $GEMSHOME/VERSIONS.sh

## Set the GMML version info
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
cat $GEMSHOME/gmml/VERSIONS.sh >> $GEMSHOME/VERSIONS.sh
## Set and get the GMML2 info
echo "...GMML2"
if ! cd "${GEMSHOME}/gmml2" ; then
    echo "Could not cd to GEMSHOME/gmml2 directory"
    echo "Cannot complete acquisition of versions info."
    exit 1
fi
if ! ./make-versions-file.bash ; then
    echo "Could not generate gmml2 versions file"
    echo "Cannot complete acquisition of versions info."
    exit 1
fi
cat $GEMSHOME/gmml2/VERSIONS.sh >> $GEMSHOME/VERSIONS.sh
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
cat $GEMSHOME/External/MD_Utils/VERSIONS.sh >> $GEMSHOME/VERSIONS.sh

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
cat $GEMSHOME/External/GM_Utils/VERSIONS.sh >> $GEMSHOME/VERSIONS.sh

echo "VERSIONS.sh is finished."
