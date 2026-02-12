    MD_GRPC_HOST='gw-slurm-head'
    MD_GRPC_HOSTNAME='swarm'
    MD_GRPC_PORT=50052
    MD_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    MD_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    MD_LOCAL_CLUSTER_PATH="/website/userdata/mmservice/md"
    MD_REMOTE_CLUSTER_PATH="/scratch3/special/userdata/mmservice/md"
    
    GM_GRPC_HOST='gw-slurm-head-two'
    GM_GRPC_HOSTNAME='swarm-two'
    GM_GRPC_PORT=50053
    GM_SBATCH_ARGS='{ "partition": "gmweb", "time": "120", "nodes": "1", "tasks-per-node": "28" }'
    GM_LOCAL_PARAMETERS='{ "numProcs": "28" }'
    GM_LOCAL_CLUSTER_PATH="/website/userdata/complex/gm"
    GM_REMOTE_CLUSTER_PATH="/scratch3/special/userdata/complex/gm"
    
    notGEMSHOME="/path/to/some/gems"
    MD_PRECONFIG_NAME="MDaaS-RunMD_preconfig-git-ignore-me.json"
    GM_PRECONFIG_NAME="Glycomimetics_preconfig-git-ignore-me.json"
    MD_LOCAL_PRECONFIG_PATH="${notGEMSHOME}/local.${MD_PRECONFIG_NAME}"
    GM_LOCAL_PRECONFIG_PATH="${notGEMSHOME}/local.${GM_PRECONFIG_NAME}"
    MD_REMOTE_PRECONFIG_PATH="${notGEMSHOME}/remote.${MD_PRECONFIG_NAME}"
    GM_REMOTE_PRECONFIG_PATH="${notGEMSHOME}/remote.${GM_PRECONFIG_NAME}"

#!/bin/bash
# Environment updated on:  Sun Feb  8 03:57:03 AM EST 2026
#

## Where we find ourselves
export WEBSITE_CONTEXT=DevEnv
##
## The base of it all
export DEV_ENV_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2
##
## Programs and data that get mounted to containers
export PROGRAMS_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Programs
export DATA_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data
export GEMS_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Programs/gems
export GLYCOWEBTOOL_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Programs/glycomimeticsWebtool
export USERDATA_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data/userdata
export UPLOADS_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data/uploads
export WEBDATA_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data
export WEB_STATISTICS_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Statistics/static
export MOLSTAR_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Molstar

## Per-app volume mappings for cluster services
export MD_CLUSTER_USERDATA_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data/userdata/mmservice/md
export GM_CLUSTER_USERDATA_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data/userdata/complex/gm
export AD_CLUSTER_USERDATA_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data/userdata/complex/ad
export GP_CLUSTER_USERDATA_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Web_Data/userdata/conjugate/gp
export MD_CLUSTER_FILESYSTEM_PATH=/website/userdata/mmservice/md
export GM_CLUSTER_FILESYSTEM_PATH=/website/userdata/complex/gm
export AD_CLUSTER_FILESYSTEM_PATH=/website/userdata/complex/ad
export GP_CLUSTER_FILESYSTEM_PATH=/website/userdata/conjugate/gp
##
## Build directories
export SLURM_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Slurm
export GRPC_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/GRPC
export Django_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Django
export Statistics_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Statistics
export Wordpress_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Wordpress
export Proxy_BUILD_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Proxy
export Virtuoso_BASE_PATH=/home/lachele/GLYCAM_Dev_Env/V_2/Virtuoso

#!/usr/bin/env bash
# To manually force reconfiguration run this script from the GRPC folder with GEMS_FORCE_INSTANCE_RECONFIGURATION="True" set.

source "inputs/023.instance_config_input.bash"

echo "Testing Instance Config Generation"

echo "...  for a Standalone Instance"

echo "...  for a DevEnv Instance"
# DEVENV SETTINGS
	MD_GRPC_HOST='gw-slurm-head'
	MD_GRPC_HOSTNAME='swarm'
	MD_GRPC_PORT=50052
    MD_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    MD_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    MD_LOCAL_CLUSTER_PATH="/website/userdata/mmservice/md"
    MD_REMOTE_CLUSTER_PATH=${MD_LOCAL_CLUSTER_PATH}
    GM_GRPC_HOST='gw-slurm-head'
    GM_GRPC_HOSTNAME='swarm'
    GM_GRPC_PORT=50052
    GM_SBATCH_ARGS='{ "partition": "gm", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    GM_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    GM_LOCAL_CLUSTER_PATH="/website/userdata/complex/gm"
    GM_REMOTE_CLUSTER_PATH=${GM_LOCAL_CLUSTER_PATH}
    AD_GRPC_HOST='thortunnel'
    AD_GRPC_HOSTNAME='localhost'
    AD_GRPC_PORT=50052
    AD_JSON_PORT=50053 # UNUSED currently, but needs to be set for AD.
    AD_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    AD_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    AD_LOCAL_CLUSTER_PATH="/website/userdata/complex/ad"
    AD_REMOTE_CLUSTER_PATH=${AD_LOCAL_CLUSTER_PATH}
    GP_GRPC_HOST='gw-slurm-head'
    GP_GRPC_HOSTNAME='swarm'
    GP_GRPC_PORT=50052
    GP_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    GP_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    GP_LOCAL_CLUSTER_PATH="/website/userdata/conjugate/gp"
    GP_REMOTE_CLUSTER_PATH=${GP_LOCAL_CLUSTER_PATH}

echo "...  for a Remote Execution Instance"
# Without modification, these settings are typically used for the swarmtest site.
    MD_GRPC_HOST='172.16.4.2'
    MD_GRPC_HOSTNAME='thoreau' # The instance configuration uses hostname information to simplify logic.
    MD_GRPC_PORT=42029
    MD_SBATCH_ARGS='{ "partition": "mdaas", "time": "120", "nodes": "1", "gres": "gpu:1", "tasks-per-node": "4", "cpus-per-task": "7" }'
    MD_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    if [ "${MD_GRPC_HOSTNAME}" == "thoreau" ] ; then
        # Note: These paths should be distinct per website deployment to avoid mixing projects among site deployments.
        MD_LOCAL_CLUSTER_PATH="/website/userdata/mmservice/md"
        MD_REMOTE_CLUSTER_PATH="/scratch2/thoreau-web/mmservice/swarmtest-md"
    fi
    GM_GRPC_HOST=172.16.4.4
    GM_GRPC_HOSTNAME='harper'
    GM_GRPC_PORT=42029
    GM_SBATCH_ARGS='{ "partition": "gm", "time": "120", "nodes": "1", "gres": "gpu:1", "tasks-per-node": "4", "cpus-per-task": "7" }'
    GM_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    if [ "${GM_GRPC_HOSTNAME}" == "harper" ] ; then
        # WE NEED TO CHANGE FILESYSTEM PATHS FOR LIVE_SWARM 
        GM_LOCAL_CLUSTER_PATH="/website/userdata/complex/gm"
        GM_REMOTE_CLUSTER_PATH="/scratch2/harper-web/complex/swarmtest-gm"
    fi
    AD_GRPC_HOST=172.16.4.2
    AD_GRPC_HOSTNAME='thoreau'
    AD_GRPC_PORT=42030
    AD_JSON_PORT=42031 # UNUSED currently, but needs to be set for AD.
    AD_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    AD_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    if [ "${AD_GRPC_HOSTNAME}" == "thoreau" ] ; then
        # WE NEED TO CHANGE FILESYSTEM PATHS FOR LIVE_SWARM 
        AD_LOCAL_CLUSTER_PATH="/website/userdata/complex/ad"
        AD_REMOTE_CLUSTER_PATH="/scratch2/thoreau-web/complex/swarmtest-ad"
    fi
    GP_GRPC_HOST=172.16.4.2
    GP_GRPC_HOSTNAME='thoreau'
    GP_GRPC_PORT=42030
    GP_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    GP_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    if [ "${GP_GRPC_HOSTNAME}" == "thoreau" ] ; then
        # WE NEED TO CHANGE FILESYSTEM PATHS FOR LIVE_SWARM 
        GP_LOCAL_CLUSTER_PATH="/website/userdata/conjugate/gp"
        GP_REMOTE_CLUSTER_PATH="/scratch2/thoreau-web/conjugate/swarmtest-gp"
    fi



# Generate the preconfig files for the GRPC/Delegator instance and remote hosts.
MD_PRECONFIG_NAME="MDaaS-RunMD_preconfig-git-ignore-me.json"
MD_LOCAL_PRECONFIG_PATH="${GEMS_BASE_PATH}/local.${MD_PRECONFIG_NAME}"
MD_REMOTE_PRECONFIG_PATH="${GEMS_BASE_PATH}/remote.${MD_PRECONFIG_NAME}"

GM_PRECONFIG_NAME="Glycomimetics_preconfig-git-ignore-me.json"
GM_LOCAL_PRECONFIG_PATH="${GEMS_BASE_PATH}/local.${GM_PRECONFIG_NAME}"
GM_REMOTE_PRECONFIG_PATH="${GEMS_BASE_PATH}/remote.${GM_PRECONFIG_NAME}"

AD_PRECONFIG_NAME="AntibodyDocking_preconfig-git-ignore-me.json"
AD_LOCAL_PRECONFIG_PATH="${GEMS_BASE_PATH}/local.${AD_PRECONFIG_NAME}"
AD_REMOTE_PRECONFIG_PATH="${GEMS_BASE_PATH}/remote.${AD_PRECONFIG_NAME}"

GP_PRECONFIG_NAME="GlycoProtein_preconfig-git-ignore-me.json"
GP_LOCAL_PRECONFIG_PATH="${GEMS_BASE_PATH}/local.${GP_PRECONFIG_NAME}"
GP_REMOTE_PRECONFIG_PATH="${GEMS_BASE_PATH}/remote.${GP_PRECONFIG_NAME}"


# Generate local preconfigs, configure the local instance, and just generate the remote preconfigs.
# TODO: Add JSON_PORT to the preconfig generation.
# TODO: skip this complicated cli and just write preconfig jsons instead.
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_LOCAL_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_LOCAL_CLUSTER_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --config "${MD_LOCAL_PRECONFIG_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_REMOTE_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_REMOTE_CLUSTER_PATH}"

python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig Glycomimetics "${GM_LOCAL_PRECONFIG_PATH}" "${GM_GRPC_HOSTNAME}" "${GM_GRPC_HOST}" "${GM_GRPC_PORT}" "${GM_SBATCH_ARGS}" "${GM_LOCAL_PARAMETERS}" "${GM_LOCAL_CLUSTER_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --config "${GM_LOCAL_PRECONFIG_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig Glycomimetics "${GM_REMOTE_PRECONFIG_PATH}" "${GM_GRPC_HOSTNAME}" "${GM_GRPC_HOST}" "${GM_GRPC_PORT}" "${GM_SBATCH_ARGS}" "${GM_LOCAL_PARAMETERS}" "${GM_REMOTE_CLUSTER_PATH}"

python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig AntibodyDocking "${AD_LOCAL_PRECONFIG_PATH}" "${AD_GRPC_HOSTNAME}" "${AD_GRPC_HOST}" "${AD_GRPC_PORT}" "${AD_SBATCH_ARGS}" "${AD_LOCAL_PARAMETERS}" "${AD_LOCAL_CLUSTER_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --config "${AD_LOCAL_PRECONFIG_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig AntibodyDocking "${AD_REMOTE_PRECONFIG_PATH}" "${AD_GRPC_HOSTNAME}" "${AD_GRPC_HOST}" "${AD_GRPC_PORT}" "${AD_SBATCH_ARGS}" "${AD_LOCAL_PARAMETERS}" "${AD_REMOTE_CLUSTER_PATH}"

python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig GlycoProtein "${GP_LOCAL_PRECONFIG_PATH}" "${GP_GRPC_HOSTNAME}" "${GP_GRPC_HOST}" "${GP_GRPC_PORT}" "${GP_SBATCH_ARGS}" "${GP_LOCAL_PARAMETERS}" "${GP_LOCAL_CLUSTER_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --config "${GP_LOCAL_PRECONFIG_PATH}"
python3 "${GEMS_BASE_PATH}/bin/setup-instance.py" --generate-preconfig GlycoProtein "${GP_REMOTE_PRECONFIG_PATH}" "${GP_GRPC_HOSTNAME}" "${GP_GRPC_HOST}" "${GP_GRPC_PORT}" "${GP_SBATCH_ARGS}" "${GP_LOCAL_PARAMETERS}" "${GP_REMOTE_CLUSTER_PATH}"


if [ ! $? -eq 0 ] ; then
    pretty_error_exit "setup-instance.py FAILED IN GRPC/bin/initialize.sh! GRPC/Delegator instance configuration failed."
fi

echo ""
echo "GRPC/Delegator GEMS instance configuration complete, see the generated ${GEMS_BASE_PATH}/instance_config.json"
echo "To manually setup the this local instance, you may back up the generated config and run the following commands:"
echo ""
echo "export GEMSHOME=\"${GEMS_BASE_PATH}\""
echo "\$GEMSHOME/bin/setup-instance.py --config '\${GEMSHOME}/${MD_PRECONFIG_NAME}'"
echo "\$GEMSHOME/bin/setup-instance.py --config '\${GEMSHOME}/${GM_PRECONFIG_NAME}'"
echo "\$GEMSHOME/bin/setup-instance.py --config '\${GEMSHOME}/${AD_PRECONFIG_NAME}'"
echo ""
echo "Note: If you want to regenerate the host preconfigs, you need to run the setup-instance.py script first with the --generate-preconfig flag."
echo "      Please see GRPC/bin/initialize.sh for an example case."
echo ""
echo "MD Cluster Host (MD_GRPC_HOST/PORT): ${MD_GRPC_HOSTNAME}, ${MD_GRPC_HOST}:${MD_GRPC_PORT}"
echo "MD Cluster Filesystem Path: ${MD_CLUSTER_FILESYSTEM_PATH}"
echo ""
echo "GM Cluster Host (GM_GRPC_HOST/PORT): ${GM_GRPC_HOSTNAME}, ${GM_GRPC_HOST}:${GM_GRPC_PORT}"
echo "GM Cluster Filesystem Path: ${GM_CLUSTER_FILESYSTEM_PATH}"
echo ""
echo "AD Cluster Host (AD_GRPC_HOST/PORT): ${AD_GRPC_HOSTNAME}, ${AD_GRPC_HOST}:${AD_GRPC_PORT}"
echo "AD Cluster Host JSON Port: ${AD_JSON_PORT}"
echo "AD Cluster Filesystem Path: ${AD_CLUSTER_FILESYSTEM_PATH}"
echo ""
echo "GP Cluster Host (GP_GRPC_HOST/PORT): ${GP_GRPC_HOSTNAME}, ${GP_GRPC_HOST}:${GP_GRPC_PORT}"
echo "GP Cluster Filesystem Path: ${GP_CLUSTER_FILESYSTEM_PATH}"
echo ""
echo ""
echo "Please note, this script can be run with INTERACTIVE_GRPC_INIT="True" to generate the preconfig files and then prompt the user to copy them to the remote hosts."


# TODO: Automatically run scp/ssh commands
# TODO: Start server script: Read GRPC_PORT from remote-local instance_config.json
# We could use module load, but we already have GEMS paths. If Andrew wants to use module load instead, go ahead.
if [[ -f ../LIVE_SWARM && "${INTERACTIVE_GRPC_INIT}" == "True" ]] ; then
    echo -e "\033[1;33mYou now must copy the generated preconfig jsons to the remote hosts. \033[0m"
    echo -e "\033[1;33mThen run the setup-instance.py script on the remote hosts with their respective configs. \033[0m"
    echo ""
    read -t 300 -p "Do you want to generate the scp and ssh commands for these actions? (y/n):" continue_choice
    if [[ $? -ne 0 || ${continue_choice} != "y" ]] ; then
        # Quit if the user does not want to generate the commands.
        echo ""
        echo "If you want to generate them later, re-run this DevEnv script: 'cd V_2/GRPC/; bash bin/initialize.sh'"
        echo ""
        echo -e "\033[1;32mGRPC/Delegator initialization complete. \033[0m"
        exit 0
    fi
    echo ""
    echo ""
    # Set the remote GEMSHOME paths if not already set and ssh commands for configuring the instance configs on remote hosts.
    if [ -z "${MD_REMOTE_GEMSHOME}" ] ; then
        read -r -p "Please enter the correct GEMSHOME path for the MD remote GEMS instance: " MD_REMOTE_GEMSHOME
    fi
    echo ""
    echo "To set up the MD Cluster Host, run:"
    echo ""
    echo "scp '${MD_REMOTE_PRECONFIG_PATH}' ${MD_GRPC_HOST}:'${MD_REMOTE_GEMSHOME}/${MD_PRECONFIG_NAME}'"
    echo "ssh ${MD_GRPC_HOST} -f \"GEMSHOME='${MD_REMOTE_GEMSHOME}' python3 '${MD_REMOTE_GEMSHOME}/bin/setup-instance.py' --config '${MD_REMOTE_GEMSHOME}/${MD_PRECONFIG_NAME}'\""
    echo ""
    echo ""
    if [ -z "${GM_REMOTE_GEMSHOME}" ] ; then
        echo -e "\033[1;33mAgain, for the GM remote GEMS instance\033[0m"
        read -r -p "Please enter the correct GEMSHOME path for the GM remote GEMS instance: " GM_REMOTE_GEMSHOME
    fi
    echo ""
    echo "or for the GM Cluster Host, run:"
    echo ""
    echo "scp '${GM_REMOTE_PRECONFIG_PATH}' ${GM_GRPC_HOST}:'${GM_REMOTE_GEMSHOME}/${GM_PRECONFIG_NAME}'"
    echo "ssh ${GM_GRPC_HOST} -f \"GEMSHOME='${GM_REMOTE_GEMSHOME}' python3 '${GM_REMOTE_GEMSHOME}/bin/setup-instance.py' --config '${GM_REMOTE_GEMSHOME}/${GM_PRECONFIG_NAME}'\""
    echo ""
    echo ""
    if [ -z "${AD_REMOTE_GEMSHOME}" ] ; then
        echo -e "\033[1;33mAgain, for the AD remote GEMS instance\033[0m"
        read -r -p "Please enter the correct GEMSHOME path for the AD remote GEMS instance: " AD_REMOTE_GEMSHOME
    fi
    echo ""
    echo "or for the AD Cluster Host, run:"
    echo ""
    echo "scp '${AD_REMOTE_PRECONFIG_PATH}' ${AD_GRPC_HOST}:'${AD_REMOTE_GEMSHOME}/${AD_PRECONFIG_NAME}'"
    echo "ssh ${AD_GRPC_HOST} -f \"GEMSHOME='${AD_REMOTE_GEMSHOME}' python3 '${AD_REMOTE_GEMSHOME}/bin/setup-instance.py' --config '${AD_REMOTE_GEMSHOME}/${AD_PRECONFIG_NAME}'\""
    echo ""
    echo "" 
    if [ -z "${GP_REMOTE_GEMSHOME}" ] ; then
        echo -e "\033[1;33mAgain, for the GP remote GEMS instance\033[0m"
        read -r -p "Please enter the correct GEMSHOME path for the GP remote GEMS instance: " GP_REMOTE_GEMSHOME
    fi
    echo ""
    echo "or for the GP Cluster Host, run:"
    echo ""
    echo "scp '${GP_REMOTE_PRECONFIG_PATH}' ${GP_GRPC_HOST}:'${GP_REMOTE_GEMSHOME}/${GP_PRECONFIG_NAME}'"
    echo "ssh ${GP_GRPC_HOST} -f \"GEMSHOME='${GP_REMOTE_GEMSHOME}' python3 '${GP_REMOTE_GEMSHOME}/bin/setup-instance.py' --config '${GP_REMOTE_GEMSHOME}/${GP_PRECONFIG_NAME}'\""
    echo ""
    echo ""
    echo -e "\033[1;33mRemember to start the gRPC/SLURM and if necessary gRPC/JSON servers on the remote hosts. \033[0m"
    echo ""
    echo ""
    # Generate the ssh commands for starting the gRPC servers on the remote hosts.
    read -t 150 -p "Do you want to generate the ssh commands for starting the gRPC servers on the remote hosts? (y/n):" continue_choice
    if [[ $? -ne 0 || ${continue_choice} != 'y' ]] ; then
        # Quit if the user does not want to generate the commands.
        echo ""
        echo -e "\033[1;32mGRPC/Delegator initialization complete. \033[0m"
        exit 0
    fi
    echo ""
    echo ""
    echo "To start the MD Cluster Host gRPC/SLURM server, run:"
    echo ""
    echo "ssh ${MD_GRPC_HOST} -f \"GEMSHOME='${MD_REMOTE_GEMSHOME}' PYTHONPATH='${MD_REMOTE_GEMSHOME}':\$PYTHONPATH GEMS_GRPC_SLURM_PORT=${MD_GRPC_PORT} python3 '${MD_REMOTE_GEMSHOME}/gRPC/SLURM/gems_grpc_slurm_server.py'\""
    echo ""
    echo ""
    echo "To start the GM Cluster Host gRPC/SLURM server, run:"
    echo ""
    echo "ssh ${GM_GRPC_HOST} -f \"GEMSHOME='${GM_REMOTE_GEMSHOME}' PYTHONPATH='${GM_REMOTE_GEMSHOME}':\$PYTHONPATH GEMS_GRPC_SLURM_PORT=${GM_GRPC_PORT} python3 '${GM_REMOTE_GEMSHOME}/gRPC/SLURM/gems_grpc_slurm_server.py'\""
    echo ""
    echo ""
    echo "To start the AD Cluster Host gRPC/SLURM server, run:"
    echo ""
    echo "ssh ${AD_GRPC_HOST} -f \"GEMSHOME='${AD_REMOTE_GEMSHOME}' PYTHONPATH='${AD_REMOTE_GEMSHOME}':\$PYTHONPATH GEMS_GRPC_SLURM_PORT=${AD_GRPC_PORT} python3 '${AD_REMOTE_GEMSHOME}/gRPC/SLURM/gems_grpc_slurm_server.py'\""
    echo ""
    echo "and to start the AD Cluster Host gRPC/JSON server, run:"
    echo ""
    echo "ssh ${AD_GRPC_HOST} -f \"GEMSHOME='${AD_REMOTE_GEMSHOME}' PYTHONPATH='${AD_REMOTE_GEMSHOME}':\$PYTHONPATH GRPC_DELEGATOR_PORT=${AD_JSON_PORT} python3 '${AD_REMOTE_GEMSHOME}/gRPC/JSON/json_server.py'\""
    echo ""
    echo ""
    echo "To start the GP Cluster Host gRPC/SLURM server, run:"
    echo ""
    echo "ssh ${GP_GRPC_HOST} -f \"GEMSHOME='${GP_REMOTE_GEMSHOME}' PYTHONPATH='${GP_REMOTE_GEMSHOME}':\$PYTHONPATH GEMS_GRPC_SLURM_PORT=${GP_GRPC_PORT} python3 '${GP_REMOTE_GEMSHOME}/gRPC/SLURM/gems_grpc_slurm_server.py'\""
    echo ""
    echo ""
fi

echo -e "\033[1;32mGRPC/Delegator initialization complete. \033[0m"
