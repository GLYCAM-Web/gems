#!/usr/bin/env bash

# If GEMS_KEEP_BAD_OUTPUTS is set to "True", badOutputs will not be removed after testing

. './utilities/common_environment.bash'
. './utilities/functions.bash'

echo "The output path is: ${GEMS_OUTPUT_PATH}"

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test023'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutput="${badOutputPrefix}.txt"
badOutputDir="${badOutDir}/${now}_${outputFilePrefix}_Files"

mkdir -p "${badOutputDir}"

ALL_JSON_ARE_GOOD='true'
ALL_TESTS_PASSED='true'

echo "Testing Instance Config Generation"

# Source the inputs for the test
source "inputs/023.instance_config_input_swarm.bash"



# Generate the preconfig files for the GRPC/Delegator instance and remote hosts.
MD_PRECONFIG_NAME="MDaaS-RunMD_preconfig-git-ignore-me.json"
MD_LOCAL_PRECONFIG_PATH="${badOutputDir}/local.${MD_PRECONFIG_NAME}"
MD_REMOTE_PRECONFIG_PATH="${badOutputDir}/remote.${MD_PRECONFIG_NAME}"

GM_PRECONFIG_NAME="Glycomimetics_preconfig-git-ignore-me.json"
GM_LOCAL_PRECONFIG_PATH="${badOutputDir}/local.${GM_PRECONFIG_NAME}"
GM_REMOTE_PRECONFIG_PATH="${badOutputDir}/remote.${GM_PRECONFIG_NAME}"

AD_PRECONFIG_NAME="AntibodyDocking_preconfig-git-ignore-me.json"
AD_LOCAL_PRECONFIG_PATH="${badOutputDir}/local.${AD_PRECONFIG_NAME}"
AD_REMOTE_PRECONFIG_PATH="${badOutputDir}/remote.${AD_PRECONFIG_NAME}"

GP_PRECONFIG_NAME="GlycoProtein_preconfig-git-ignore-me.json"
GP_LOCAL_PRECONFIG_PATH="${badOutputDir}/local.${GP_PRECONFIG_NAME}"
GP_REMOTE_PRECONFIG_PATH="${badOutputDir}/remote.${GP_PRECONFIG_NAME}"


# TODO: skip this complicated cli and just write preconfig jsons instead.
python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_LOCAL_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_LOCAL_CLUSTER_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --config "${MD_LOCAL_PRECONFIG_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_REMOTE_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_REMOTE_CLUSTER_PATH}"

python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig Glycomimetics "${GM_LOCAL_PRECONFIG_PATH}" "${GM_GRPC_HOSTNAME}" "${GM_GRPC_HOST}" "${GM_GRPC_PORT}" "${GM_SBATCH_ARGS}" "${GM_LOCAL_PARAMETERS}" "${GM_LOCAL_CLUSTER_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --config "${GM_LOCAL_PRECONFIG_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig Glycomimetics "${GM_REMOTE_PRECONFIG_PATH}" "${GM_GRPC_HOSTNAME}" "${GM_GRPC_HOST}" "${GM_GRPC_PORT}" "${GM_SBATCH_ARGS}" "${GM_LOCAL_PARAMETERS}" "${GM_REMOTE_CLUSTER_PATH}"

python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig AntibodyDocking "${AD_LOCAL_PRECONFIG_PATH}" "${AD_GRPC_HOSTNAME}" "${AD_GRPC_HOST}" "${AD_GRPC_PORT}" "${AD_SBATCH_ARGS}" "${AD_LOCAL_PARAMETERS}" "${AD_LOCAL_CLUSTER_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --config "${AD_LOCAL_PRECONFIG_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig AntibodyDocking "${AD_REMOTE_PRECONFIG_PATH}" "${AD_GRPC_HOSTNAME}" "${AD_GRPC_HOST}" "${AD_GRPC_PORT}" "${AD_SBATCH_ARGS}" "${AD_LOCAL_PARAMETERS}" "${AD_REMOTE_CLUSTER_PATH}"

python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig GlycoProtein "${GP_LOCAL_PRECONFIG_PATH}" "${GP_GRPC_HOSTNAME}" "${GP_GRPC_HOST}" "${GP_GRPC_PORT}" "${GP_SBATCH_ARGS}" "${GP_LOCAL_PARAMETERS}" "${GP_LOCAL_CLUSTER_PATH}"
python3 "${GEMSHOME}/bin/setup-instance.py" --config "${GP_LOCAL_PRECONFIG_PATH}"
python3 "$GEMSHOMEGEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig GlycoProtein "${GP_REMOTE_PRECONFIG_PATH}" "${GP_GRPC_HOSTNAME}" "${GP_GRPC_HOST}" "${GP_GRPC_PORT}" "${GP_SBATCH_ARGS}" "${GP_LOCAL_PARAMETERS}" "${GP_REMOTE_CLUSTER_PATH}"

