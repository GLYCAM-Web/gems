#!/usr/bin/env bash

# If a repo has a versions.txt file that it generates, like gmml2 does, you get that extra info.
generateRepoInfo () {
    repoPath=$1
    repoName=$2
    echo "...$repoName"
    echo """

${repoName}_GIT_BRANCH=\"$(git -C $repoPath rev-parse --abbrev-ref HEAD)\"
${repoName}_GIT_COMMIT_HASH=\"$(git -C $repoPath rev-parse HEAD)\"""" >> $GEMSHOME/versions-info.txt
    if [ -f $repoPath/version.txt ]; then
        echo "${repoName}_VERSION=\"$(cat $repoPath/version.txt)\"" >> $GEMSHOME/versions-info.txt
    fi
   
}

echo "Getting and setting Versions info."
> $GEMSHOME/versions-info.txt

##  Check GEMSHOME is set.
if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo "GEMSHOME must be set."
	exit 1
fi

# Set version info for each repo:
generateRepoInfo $GEMSHOME GEMS
generateRepoInfo $GEMSHOME/gmml GMML
generateRepoInfo $GEMSHOME/gmml2 GMML2
generateRepoInfo $GEMSHOME/External/MD_Utils MD_Utils
generateRepoInfo $GEMSHOME/External/GM_Utils GM_Utils
generateRepoInfo $GEMSHOME/External/AAD2 AAD2 
generateRepoInfo $GEMSHOME/External/GW_Stack_for_AAD2 GW_Stack_for_AAD2

echo "$0 is finished. See $GEMSHOME/versions-info.txt for output."
