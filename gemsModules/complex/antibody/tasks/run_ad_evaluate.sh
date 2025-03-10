#!/bin/bash
cd ${WD}
source ad2dockerconfig
export CONTAINER_NAME_PREFIX
export GW_STACK_PATH_PREFIX

export AAD2_DOCKER_HOME="$GW_STACK_PATH_PREFIX/AAD2_Docker"
export PATH="$GW_STACK_PATH_PREFIX/bin:$PATH"

# source /programs/website_aad2/test/GW_Stack_for_AAD2/node_setup.bash
export GW_AAD2_STACK_HOME="$GW_STACK_PATH_PREFIX/GW_Stack_for_AAD2"
cd ${GW_AAD2_STACK_HOME}
module load iptables/1.8.7
module load docker/24.0.7 
bash ensure_image_is_present.bash 

cd ${AAD2_DOCKER_HOME}
COMMAND="bash bin/run_aad2_command.bash ${WD} AD_Evaluate"
eval ${COMMAND}
