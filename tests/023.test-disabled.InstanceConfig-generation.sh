#!/usr/bin/env bash

#### READ ME
##
## This test cannot be a standard part of the testing suite until:
##
##     - The location and name of the output file 'instance_config.json' can be controlled.
##         Currently it only overwrites the one in GEMSHOME.
##     - Actually, worse, it might choose to fail rather than overwrite the one in GEMSHOME.
##     - The JSON files output by the IC module are always the same.
##         The IC module does not use Pydantic, so order in the json output is not predictable.
##         An alternative is to use the 'jq' utility. I am doing that for now, but that's a kluge.
##         The IC module will soon use Pydantic, that change being the reason for writing this test.
##
####

# If GEMS_KEEP_BAD_OUTPUTS is set to "True", badOutputs will not be removed after testing

. './utilities/common_environment.bash'
. './utilities/functions.bash'

echo "The output path is: ${GEMS_OUTPUT_PATH}"

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test023'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutputDir="${badOutDir}/${now}_${outputFilePrefix}_Files"
correctFilesPath="correct_outputs/023.InstanceConfig-generation_Files"

mkdir -p "${badOutputDir}"

ALL_TESTS_PASSED='true'

echo "Testing Instance Config Generation"

# Source the inputs for the test
source "inputs/023.instance_config_input_swarm.bash"

filesAreSame()
{
	#echo "working on files:"
	#echo "        ${1}"
	#echo "        ${2}"
	jq -S 'walk(if type == "array" then sort else . end)' ${1} > ${badOutputDir}/sort1.json
	jq -S 'walk(if type == "array" then sort else . end)' ${2} > ${badOutputDir}/sort2.json
	COMMAND="diff -U 0 ${badOutputDir}/sort1.json ${badOutputDir}/sort2.json | grep -v ^@ | wc -l"
	DiffCount="$(eval $COMMAND)"
	result="$?"
	#echo "DiffCount is ${DiffCount}"
	#echo "result is ${result}"
	if [ "${result}" != "0" ] ; then
		rclr "Saving results diff that exited with code ${result}." "${DiffCount}" "Failed diff logging"
		rm -f ${badOutputDir}/sort1.json ${badOutputDir}/sort2.json
		return "${result}"
	fi
	if [ "${DiffCount}" != "0" ] ; then
		COMMAND="diff ${badOutputDir}/sort1.json ${badOutputDir}/sort2.json "
		rclr "Saving diffs from failed comparision." "${COMMAND}" "Failed comparison logging"
		result="$?"
		rm -f ${badOutputDir}/sort1.json ${badOutputDir}/sort2.json
		return "$((result+1))"
	else
		rm -f ${badOutputDir}/sort1.json ${badOutputDir}/sort2.json
		return 0
	fi
}

declare -A lFailed  # generation of the local preconfig passed
declare -A oFailed  # updating the main instance config from the local preconfig
declare -A rFailed  # generation of the remote preconfig passed
oFailedOverall="0"

export STATUSFILE="${badOutputPrefix}.txt"
export LOGFILE="${badOutputPrefix}_details.txt"
#export TEST="True"
#export GEMS_KEEP_BAD_OUTPUTS="True"
passedSum="0"
for service in ${Services[@]} ; do 
	PreconfName="${PreconfigName[${service}]}"
	CorrectPreconfName="${PreconfName/-git-ignore-me/}"
	locICPath="${badOutputDir}/local.${PreconfName}"
	remICPath="${badOutputDir}/remote.${PreconfName}"
	IChName="${SubmissionHostNames[${service}]}"
	IChost="${SubmissionHosts[${service}]}"
	ICport="${SubmissionHostPorts[${service}]}"
	ICargs="${BatchSubmissionArgs[${service}]}"
	locParm="${LocalParameters[${service}]}"
	locExePath="${LocalWorkingPathHead[${service}]}"
	remExePath="${RemoteWorkingPathHead[${service}]}"

	## Generate the local preconfig
        COMMAND="python3 ${GEMSHOME}/bin/setup-instance.py --generate-preconfig '${service}' '${locICPath}' '${IChName}' '${IChost}' '${ICport}' '${ICargs}' '${locParm}' '${locExePath}'"
	rclr "Generating the local preconfig for service ${service}." "${COMMAND}" "Local IC setup"
	lFailed[${service}]="$?"
	if ! filesAreSame "${locICPath}"  "${correctFilesPath}/local.${CorrectPreconfName}" ; then
		lFailed[${service}]="$((lFailed[${service}]+1))"
	fi
	passedSum=$((passedSum+lFailed[${service}]))

	## Update the main instance config with the local information
        COMMAND="python3 ${GEMSHOME}/bin/setup-instance.py --config '${locICPath}'"
	rclr "Adding local info to the main instance config." "${COMMAND}" "Add local IC to main IC"
	oFailed[${service}]="$?"
	passedSum=$((passedSum+oFailed[${service}]))

	## Generate the remote preconfig
        COMMAND="python3 ${GEMSHOME}/bin/setup-instance.py --generate-preconfig '${service}' '${remICPath}' '${IChName}' '${IChost}' '${ICport}' '${ICargs}' '${locParm}' '${remEXePath}'"
	rclr "Generating the remote preconfig for service ${service}." "${COMMAND}" "Remote IC setup"
	rFailed[${service}]="$?"
	if ! filesAreSame "${remICPath}"  "${correctFilesPath}/remote.${CorrectPreconfName}" ; then
		rFailed[${service}]="$((rFailed[${service}]+1))"
	fi
	passedSum=$((passedSum+rFailed[${service}]))
done

## This has to wait for the end because I didn't save the interim versions
if ! filesAreSame "${GEMSHOME}/instance_config.json"  "${correctFilesPath}/not-ignored_instance_config.json" ; then
	echo "the instance config files are not the same"
	oFailedOverall="1"
	passedSum="$((passedSum+oFailedOverall))"
fi

if [ "${passedSum}" != "0" ] ; then
	ALL_TESTS_PASSED='false'
	for service in ${Services[@]} ; do 
		echo "For the service ${service}:"
		echo "        ${lFailed[${service}]} local preconfig actions failed."
		echo "        ${oFailed[${service}]} update of main instance config actions failed."
		echo "        ${rFailed[${service}]} remote preconfig actions failed."
	done
	if [ "${oFailedOverall}" != "0" ] ; then
		echo "The final form of the instance config file failed."
	fi
	return 1
fi

return 0

###
## The following are records of sample commands that were run in the file I based these tests on. 
##
### Generate the preconfig files for the GRPC/Delegator instance and remote hosts.
##MD_PRECONFIG_NAME="MDaaS-RunMD_preconfig-git-ignore-me.json"
##MD_LOCAL_PRECONFIG_PATH="${badOutputDir}/local.${MD_PRECONFIG_NAME}"
##MD_REMOTE_PRECONFIG_PATH="${badOutputDir}/remote.${MD_PRECONFIG_NAME}"
##
### TODO: skip this complicated cli and just write preconfig jsons instead.
##python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_LOCAL_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_LOCAL_CLUSTER_PATH}"
##python3 "${GEMSHOME}/bin/setup-instance.py" --config "${MD_LOCAL_PRECONFIG_PATH}"
##python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_REMOTE_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_REMOTE_CLUSTER_PATH}"

