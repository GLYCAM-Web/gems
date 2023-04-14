#!/usr/bin/env bash

. utilities/common_environment.bash

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test008'
badOutputPrefix="${badOutDir}/${now}_${outputFilename}"
badOutput="${badOutputPrefix}.txt"

ALL_JSON_ARE_GOOD='true'
ALL_SEQID_ARE_GOOD='true'

theCorrectSequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
defaultStructureConformationID='e6c2e2e8-758b-58b8-b5ff-d138da38dd22'


do_the_common_tasks()
{	
	jsonInFile="${1}"
	outFilePrefix="${2}"

	# Delegate the json input

	theJsonOut="$(cat ${jsonInFile} | $GEMSHOME/bin/delegate | tee ${outFilePrefix}.json)"

	check_output_is_only_json ${outFilePrefix}.json
	
	isJsonOk=$?
	
	if [ "${isJsonok}" != 0 ] ; then
		ALL_JSON_ARE_GOOD='false'
		echo "FAILURE:  ${1} got a non-purely-json response from delegator." | tee -a ${badOutput}
		echo "Check ${outFilePrefix}.json for more information." | tee -a ${badOutput}
	fi

	theseqID="$(get_seqID_from_json ${theJsonout})"
	if [ "${theseqID}" != "${theCorrectSequenceID}" ] ; then
		ALL_SEQID_ARE_GOOD='false'
		echo "FAILURE:  got seqID of ${theseqID} which shouldbe ${theCorrectSequenceID}." | tee -a ${badOutput}
	fi

	thepUUID="$(get_pUUID_from_json ${theJsonout})"
	return thepUUID
}



## run the evaluation
## check:


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
