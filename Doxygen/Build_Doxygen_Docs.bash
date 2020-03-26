#!/bin/bash
##
##  A file to make the Doxygen docs a little better by automatically
##  setting some variables.
##

export GIT_BRANCH=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
export GIT_COMMIT_HASH=$(git rev-parse HEAD)
export DOXYGEN_STRIP_PATH=$(cd ../ && pwd)
export DOXY_LOG_FILE="Doxygen/docs_build.log"
export DOXY_INPUTS=" README.md ./bin/ ./dat/ ./gemsModules/ ./gRPC/ ./testbin/ ./tests/ "

#echo "branch is >>${GIT_BRANCH}<<"
#echo "hash is >>${GIT_COMMIT_HASH}<<"
#echo "path is >>${DOXYGEN_STRIP_PATH}<<"

doxygen Doxygen/Doxyfile
