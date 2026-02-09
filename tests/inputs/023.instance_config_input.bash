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

