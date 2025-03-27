#!/usr/bin/env bash
# OG: thought about a function to pass info into, but GMML2 is unique with a version number. This is quite clear so fine.
echo "Getting and setting Versions info."

##  Check GEMSHOME is set.
if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo "GEMSHOME must be set."
	exit 1
fi

# Set version info for each repo:
echo "...GEMS"
echo """
GEMS_GIT_BRANCH=\"$(git -C $GEMSHOME rev-parse --abbrev-ref HEAD)\"
GEMS_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME rev-parse HEAD)\"
""" > $GEMSHOME/versions-info.txt

echo "...GMML"
echo """
GMML_GIT_BRANCH=\"$(git -C $GEMSHOME/gmml rev-parse --abbrev-ref HEAD)\"
GMML_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME/gmml rev-parse HEAD)\"
""" >> $GEMSHOME/versions-info.txt

echo "...GMML2"
echo """
GMML2_GIT_BRANCH=\"$(git -C $GEMSHOME/gmml2 rev-parse --abbrev-ref HEAD)\"
GMML2_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME/gmml2 rev-parse HEAD)\"
GMML2_VERSION=\"$(cat $GEMSHOME/gmml2/version.txt)\"
""" >> $GEMSHOME/versions-info.txt

echo "...MD_Utils"
echo """
MD_UTILS_GIT_BRANCH=\"$(git -C $GEMSHOME/External/MD_Utils rev-parse --abbrev-ref HEAD)\"
MD_UTILS_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME/External/MD_Utils rev-parse HEAD)\"
""" >> $GEMSHOME/versions-info.txt

echo "...GM_Utils"
echo """
GM_UTILS_GIT_BRANCH=\"$(git -C $GEMSHOME/External/GM_Utils rev-parse --abbrev-ref HEAD)\"
GM_UTILS_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME/External/GM_Utils rev-parse HEAD)\"
""" >> $GEMSHOME/versions-info.txt

echo "...AAD2"
echo """
AAD2_GIT_BRANCH=\"$(git -C $GEMSHOME/External/AAD2 rev-parse --abbrev-ref HEAD)\"
AAD2_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME/External/AAD2 rev-parse HEAD)\"
""" >> $GEMSHOME/versions-info.txt

echo "...GW_Stack_for_AAD2"
echo """
GW_Stack_for_AAD2_GIT_BRANCH=\"$(git -C $GEMSHOME/External/GW_Stack_for_AAD2 rev-parse --abbrev-ref HEAD)\"
GW_Stack_for_AAD2_GIT_COMMIT_HASH=\"$(git -C $GEMSHOME/External/GW_Stack_for_AAD2 rev-parse HEAD)\"
""" >> $GEMSHOME/versions-info.txt


echo "$0 is finished. See $GEMSHOME/versions-info.txt for output."
