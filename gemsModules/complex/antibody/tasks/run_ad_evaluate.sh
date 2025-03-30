#!/bin/bash
set -e
source ~/.bash_profile

cd ${WD}
source ad2config

export WD
export PATH="${AAD2_CLI_BIN_PATH}:${AAD2_DOCKER_HOME}/bin:${PATH}"

bash run_aad2_command.bash "${WD}" AD_Evaluate
