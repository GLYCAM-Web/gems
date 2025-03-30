#!/bin/bash
source ~/.bash_profile
set -e

cd ${WD}
source ad2config

export WD
export PATH="${AAD2_CLI_BIN_PATH}:${PATH}"

# env >$WD/env.log

cd ${AAD2_DOCKER_HOME}
bash ./bin/run_aad2_command.bash "${WD}" AD_Evaluate
