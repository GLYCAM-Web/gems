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
        exit 1 # we could test failure cases instead
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
    echo 
    echo "Running anyways to test failure case."
fi

PROJECT_DIR=$(./bin/delegate gemsModules/complex/antibody/tests/inputs/explicit_evaluate-thoreau.json | tee ad2_remote_test_eval_output-gitignoreme.txt | grep -Po '"project_dir":\s*"\K[^"]*')\
  || { echo "Failed to get project_dir from Evaluation delegation, do we have connection?"; exit 1; }

PUUID=$(echo "$PROJECT_DIR" | awk -F'/' '{print $NF}')
if [ -z "$PUUID" ]; then
    echo "Failed to get PUUID from project_dir..."
else
    echo "PUUID: $PUUID"
    rm ad2_remote_test_eval_output-gitignoreme.txt
fi

# echo '{
#  "entity": {
#    "type": "AntibodyDocking",
#    "services": {
#      "aad2_remote_build-thoreau": {
#        "type": "Build",
#        "inputs": {
#          "pUUID": "'"$PUUID"'"
#        },
#        "options": {
#          "flexibility": "rigid",
#          "count": 5
#        }
#      }
#    }
#  }
# }' | ./bin/delegate

# replace ${pUUID}, ${flexibility}, and ${count} with the values
cat gemsModules/complex/antibody/tests/inputs/explicit_build-thoreau.json | \
    sed "s/\${pUUID}/$PUUID/g" | \
    sed "s/\${flexibility}/rigid/g" | \
    sed "s/\${count}/5/g" | \
    ./bin/delegate