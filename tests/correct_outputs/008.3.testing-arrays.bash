#!/usr/bin/env bash

test_conformer_id='b90a4d30-822c-5aba-ae5a-10a9ddb1a227'

Build3Tests=(
	ListRSeqsSeqID
	ListRRequestedBuilds
	BuildDefaultSymlink
	MinGasPdb
)
declare -A Build3Commands=(
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	[ListRRequestedBuilds]="/bin/ls -R ${sequenceBuildsPath}/${build_3_pUUID}/Requested_Builds"
	[BuildDefaultSymlink]="file ${sequenceBuildsPath}/${build_3_pUUID}/default"
	[MinGasPdb]="md5sum ${sequenceBuildsPath}/${build_3_pUUID}/New_Builds/${test_conformer_id}/min-gas.pdb | cut -d ' ' -f1"
)
declare -A Build3CorrectOutputs=(
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
b90a4d30-822c-5aba-ae5a-10a9ddb1a227
c408f40d-28e0-5e8d-86a3-221b74da42f7
ce32017d-6663-5ecc-b282-9e9812986d1c
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[ListRRequestedBuilds]="""${sequenceBuildsPath}/${build_3_pUUID}/Requested_Builds:
b90a4d30-822c-5aba-ae5a-10a9ddb1a227
c408f40d-28e0-5e8d-86a3-221b74da42f7
ce32017d-6663-5ecc-b282-9e9812986d1c
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[BuildDefaultSymlink]="${sequenceBuildsPath}/${build_3_pUUID}/default: symbolic link to Existing_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22"
	[MinGasPdb]="281f3949dc7224d6e526e4fe09e23e29"
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

