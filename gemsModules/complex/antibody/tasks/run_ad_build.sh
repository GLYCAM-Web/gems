#!/bin/bash
set -e
source ~/.bash_profile
source ad2config

export WD
export PATH="${AAD2_CLI_BIN_PATH}:${PATH}"

cd ${WD}
COMMAND="bash submit_and_spawn_monitor"
eval ${COMMAND}
