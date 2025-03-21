#!/bin/bash


# Ensure there is a thortunnel entry in $GEMSHOME/instance_config.json
if ! grep -q '"thortunnel"' "$GEMSHOME/instance_config.json"; then
    echo "Please add a thortunnel entry to your $GEMSHOME/instance_config.json."
    echo "The host must be 'localhost', the jsonport must be 42099, and 'AntibodyDocking' must exist in contexts."
    exit 1
else
    # check the host, jsonport, and contexts
    if ! grep -q '"host":\s*"localhost"' "$GEMSHOME/instance_config.json"; then
        echo "Host must be 'thoreau'."
        exit 1
    fi
    if ! grep -q '"jsonport":\s*"42099"' "$GEMSHOME/instance_config.json"; then
        echo "jsonport must be 42099."
        exit 1
    fi
    if ! grep -q '"AntibodyDocking"' "$GEMSHOME/instance_config.json"; then
        echo "AntibodyDocking must exist in contexts."
        exit 1
    fi
fi

# ensure ssh tunnel is running to forward the port for the remote build service
if ! pgrep -f "ssh -L 42099:localhost:42099 -N webdev@thoreau" > /dev/null; then
    echo "Please run 'ssh -L 42099:localhost:42099 -N webdev@thoreau' in a separate terminal."
    echo "You probably will also need to copy your ssh keys and ssh_config into webdev's home in grpc-delegator."
    exit 1
fi

PROJECT_DIR=$(./bin/delegate gemsModules/complex/antibody/tests/inputs/explicit_evaluate-thoreau.json | tee | grep -Po '"project_dir":\s*"\K[^"]*') || exit 1
PUUID=$(echo "$PROJECT_DIR" | awk -F'/' '{print $NF}')
#echo "pUUID: $PUUID"

echo '{
 "entity": {
   "type": "AntibodyDocking",
   "services": {
     "aad2_remote_build-thoreau": {
       "type": "Build",
       "inputs": {
         "pUUID": "'"$PUUID"'"
       },
       "options": {
         "flexibility": "rigid",
         "count": 5
       }
     }
   }
 }
}' | ./bin/delegate
