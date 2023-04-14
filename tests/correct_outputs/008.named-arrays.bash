#!/usr/bin/env bash


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
