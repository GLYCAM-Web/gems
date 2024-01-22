#!/usr/bin/env bash

test_conformer_id='6009ea31-3ded-57b9-aee3-2b65fe1071be'

Build5Tests=(
	ListRSeqsSeqID
	ListRRequestedBuilds
	BuildDefaultSymlink
	MinGasPdb
)
declare -A Build5Commands=(
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	[ListRRequestedBuilds]="/bin/ls -R ${sequenceBuildsPath}/${build_5_pUUID}/Requested_Builds"
	[BuildDefaultSymlink]="file ${sequenceBuildsPath}/${build_5_pUUID}/default"
	[MinGasPdb]="md5sum ${sequenceBuildsPath}/${build_5_pUUID}/New_Builds/${test_conformer_id}/min-gas.pdb | cut -d ' ' -f1"
)
declare -A Build5CorrectOutputs=(
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
84bb4d4a-5323-51ed-8728-b89aaada1605
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[ListRRequestedBuilds]="""${sequenceBuildsPath}/${build_5_pUUID}/Requested_Builds:
6009ea31-3ded-57b9-aee3-2b65fe1071be
84bb4d4a-5323-51ed-8728-b89aaada1605"""
	[BuildDefaultSymlink]="${sequenceBuildsPath}/${build_5_pUUID}/default: symbolic link to New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be"
	[MinGasPdb]="98835307ae85e32f82311672fab2bea2"
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

