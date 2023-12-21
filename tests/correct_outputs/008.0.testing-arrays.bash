#!/usr/bin/env bash

EvaluationTests=(
	ListRSeqsSeqID
	DefaultSymlink
	EvalJsonOutput
	MinGasPdb
)
declare -A EvaluationCommands=(
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	[DefaultSymlink]="file ${sequenceSequencesPath}/${theCorrectSequenceID}/buildStrategyID1/All_Builds/${defaultStructureConformationID}"
	[EvalJsonOutput]="grep suuid ${sequenceSequencesPath}/${theCorrectSequenceID}/evaluation.json | cut -d '\"' -f4"
	[MinGasPdb]="md5sum ${sequenceBuildsPath}/${evaluation_pUUID}/New_Builds/${defaultStructureConformationID}/min-gas.pdb | cut -d ' ' -f1"
)
declare -A EvaluationCorrectOutputs=(
	[ListRSeqsSeqID]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586:
buildStrategyID1
current
default
evaluation.json

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1:
All_Builds
default

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds:
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[DefaultSymlink]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22: symbolic link to ../../../../Builds/${evaluation_pUUID}/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[EvalJsonOutput]="00e7d454-06dd-5067-b6c9-441dd52db586"
	[MinGasPdb]="556f6248cd99679ef99261582cfb3519"
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

