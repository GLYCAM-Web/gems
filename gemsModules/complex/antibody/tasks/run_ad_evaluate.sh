#!/bin/bash
set -e
source ~/.bash_profile
source ad2config

export WD
export PATH="${AAD2_CLI_BIN_PATH}:${PATH}"

cd ${WD}
cd ${AAD2_DOCKER_HOME}
COMMAND="bash bin/run_aad2_command.bash ${WD} AD_Evaluate"
eval ${COMMAND}
