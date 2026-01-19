#!/bin/bash
set -e
source ~/.bash_profile
source ${WD}/ad2config

export WD
export PATH="${AAD2_CLI_BIN_PATH}:${PATH}"

# We cd into AAD2_DOCKER_HOME to run the command because we need settings.sh in CWD
cd ${AAD2_DOCKER_HOME}
bash bin/run_aad2_command.bash ${WD} AD_Prep_Glycan
# env >$WD/env.log

cd ${WD}
bash submit_and_spawn_monitor
