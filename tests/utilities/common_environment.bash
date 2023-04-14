#!/usr/bin/env bash
##
##  This file contains variables that are likely to be useful for multiple tests.
##
##  It should be sourced from the tests directory.
##
##  In your test file, add the line:
##
##  . utilities/common_environment.bash
##
##  If any of these definitions doesn't work for you, just reassign them in your test script, after sourcing this file.
##  If the definition is exported here, you probably want to export it in your test file as well.
##
##  If you make these changes between sourcing this file and any other file, then the other files will pick up the
##  changes that you made.
##

## A place for testing output to go. Separated from the usual space so that it is safe to delete.

export GEMS_OUTPUT_PATH='/website/TESTS/git-ignore-me/pre-push'

## Shortens time spent minimizing or testing MD

export GEMS_MD_TEST_WORKFLOW=True

## If there must be a wait for a process to complete, set how long that wait should be.
## In the definitions below, the maximum wait time is 400 seconds, done in 10-second increments.

maxSleepTimeCount=40      ## How many sleep/wait periods to allow

oneSleepTimeDuration=10   ## How long each sleep/wait period should be

## A common definition for a datetime form.

now=$(date "+%Y-%m-%d-%H-%M-%S")

######## Sequence-specific defines

sequenceServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
sequenceSequencesPath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
sequenceBuildsPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds

