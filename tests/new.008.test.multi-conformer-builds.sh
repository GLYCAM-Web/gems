#!/usr/bin/env bash

## Shortens time spent minimizing
export GEMS_MD_TEST_WORKFLOW=True

## A place for testing output. Separated so it is safe to delete.
export GEMS_OUTPUT_PATH='/website/TESTS/git-ignore-me/pre-push'
gemsServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
gemsSequencePath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
gemsBuildPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds

## Inputs
inputJson=$GEMSHOME/gemsModules/deprecated/delegator/test_in/sequence/build_sequence_with_selected_rotamers.json
sequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
now=$(date "+%Y-%m-%d-%H-%M-%S")

## Outputs
## The variable badOutDir should be defined in the calling directory.
filename=git-ignore-me_test08_out.txt
badOutput="${badOutDir}/${now}_${filename}"

## Edit if your machine needs more time for minimization to finish
maxTimeCount=40
sleepTime=10

## run the evaluation
## check:

##        -  the output is only proper json

##        -  tree Sequences/00e7d454-06dd-5067-b6c9-441dd52db586/
"""
Sequences/00e7d454-06dd-5067-b6c9-441dd52db586/
├── buildStrategyID1
│   ├── All_Builds
│   │   └── e6c2e2e8-758b-58b8-b5ff-d138da38dd22 -> ../../../../Builds/${pUUID}/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
│   └── default -> All_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
├── current -> buildStrategyID1
├── default -> buildStrategyID1/All_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
└── evaluation.json -> ../../Builds/${pUUID}/logs/response.json
"""

##        -   tree Builds/${pUUID}/Requested_Builds/
"""
Builds/${pUUID}/Requested_Builds/
└── e6c2e2e8-758b-58b8-b5ff-d138da38dd22 -> ../New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22

1 directory, 0 files
"""

##        -  the contents of Sequences/00e7d454-06dd-5067-b6c9-441dd52db586/evaluation.json

##        -  the contents of min-gas.pdb


##  Do pretty much the same for each of the three build requests as well.   Maybe simplify the All_Builds in Sequences
##          the Requested_Builds in the pUUID might also cause issues due to directory sorting of the hashes.
