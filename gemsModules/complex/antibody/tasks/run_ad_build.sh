#!/bin/bash
set -e
source ~/.bash_profile

cd ${WD}
source ad2config

export WD
export PATH="${AAD2_CLI_BIN_PATH}:${PATH}"

bash submit_and_spawn_monitor
