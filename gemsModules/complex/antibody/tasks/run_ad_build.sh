#!/bin/bash
export PATH="$AAD2_BIN:$PATH"

bash /programs/website_aad2/test/GW_Stack_for_AAD2/set_thoreau_node_docker_modules.bash

cd $1
submit_and_spawn_monitor