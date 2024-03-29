#!/usr/bin/env bash

test_conformer_id='ce32017d-6663-5ecc-b282-9e9812986d1c'

Build2Tests=(
	ListRSeqsSeqID
	ListRRequestedBuilds
	BuildDefaultSymlink
	MinGasPdb
)
declare -A Build2Commands=(
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	[ListRRequestedBuilds]="/bin/ls -R ${sequenceBuildsPath}/${build_2_pUUID}/Requested_Builds"
	[BuildDefaultSymlink]="file ${sequenceBuildsPath}/${build_2_pUUID}/default"
	[MinGasPdb]="md5sum ${sequenceBuildsPath}/${build_2_pUUID}/New_Builds/${test_conformer_id}/min-gas.pdb | cut -d ' ' -f1"
)
declare -A Build2CorrectOutputs=(
	[ListRSeqsSeqID]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586:
buildStrategyID1
current
default
evaluation.json

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1:
All_Builds
default

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds:
6009ea31-3ded-57b9-aee3-2b65fe1071be
8ddcc916-47db-5426-828c-fc24aae19d39
ce32017d-6663-5ecc-b282-9e9812986d1c
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[ListRRequestedBuilds]="""${sequenceBuildsPath}/${build_2_pUUID}/Requested_Builds:
8ddcc916-47db-5426-828c-fc24aae19d39
ce32017d-6663-5ecc-b282-9e9812986d1c"""
	[BuildDefaultSymlink]="${sequenceBuildsPath}/${build_2_pUUID}/default: symbolic link to New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c"
	[MinGasPdb]="05f7d07545a4aef2447dc3b6f60aa91c"
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

