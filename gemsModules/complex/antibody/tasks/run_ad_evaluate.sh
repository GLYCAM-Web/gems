#!/bin/bash
export PATH="/programs/website_aad2/test/bin:$PATH"

bash /programs/website_aad2/test/GW_Stack_for_AAD2/set_thoreau_node_docker_modules.bash

cd ${WD}
source ad2dockerconfig



cd ${AAD2_DOCKER_HOME}
export CONTAINER_NAME_PREFIX
COMMAND="bash bin/run_aad2_command.bash ${WD} AD_Evaluate"
## uncomment these for debugging
#echo "The cwd is:
#$(pwd)
#The script will run this command:
#${COMMAND}"
##
# Run the actual command
eval ${COMMAND}
