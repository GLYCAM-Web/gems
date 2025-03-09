#!/bin/bash
cd ${WD}
source ad2dockerconfig
export CONTAINER_NAME_PREFIX
export AAD2_DOCKER_HOME="/programs/website_aad2/test/AAD2_Docker"
export PATH="/programs/website_aad2/test/bin:$PATH"

source /programs/website_aad2/test/GW_Stack_for_AAD2/node_setup.bash

cd ${AAD2_DOCKER_HOME}
COMMAND="bash bin/run_aad2_command.bash ${WD} submit_and_spawn_monitor"
eval ${COMMAND}
