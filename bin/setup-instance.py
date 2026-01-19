#!/usr/bin/env python3
""" This script is used to configure the current GEMS installation.

This configuration is primarily used by GEMS for request routing and filesystem mappings.
"""

import argparse, os, sys, json


GEMSHOME = os.environ.get("GEMSHOME")
sys.path.append(GEMSHOME)
sys.path.append(
    GEMSHOME + "/gemsModules"
)  # Swarm needs /gemsModules. These sys path hacks would be simplified if we used pip to install gems.
from gemsModules.systemoperations.instance_config import InstanceConfig


def argparser():
    """
    
    Example from the DevEnv:
    ```bash
    MD_GRPC_HOST='gw-slurm-head'
	MD_GRPC_HOSTNAME='swarm'
	MD_GRPC_PORT=50052
    MD_SBATCH_ARGS='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
    MD_LOCAL_PARAMETERS='{ "numProcs": "4" }'
    MD_LOCAL_CLUSTER_PATH="/website/userdata/mmservice/md"
    MD_REMOTE_CLUSTER_PATH=${MD_LOCAL_CLUSTER_PATH} # WILL NOT BE THE SAME IF REALLY A REMOTE.
    
    # ... Similar arguments for GM configured by DevEnv ... 
    
    MD_PRECONFIG_NAME="MDaaS-RunMD_preconfig-git-ignore-me.json"
    GM_PRECONFIG_NAME="Glycomimetics_preconfig-git-ignore-me.json"
    MD_LOCAL_PRECONFIG_PATH="${GEMSHOME}/local.${MD_PRECONFIG_NAME}"
    GM_LOCAL_PRECONFIG_PATH="${GEMSHOME}/local.${GM_PRECONFIG_NAME}"
    MD_REMOTE_PRECONFIG_PATH="${GEMSHOME}/remote.${MD_PRECONFIG_NAME}"
    GM_REMOTE_PRECONFIG_PATH="${GEMSHOME}/remote.${GM_PRECONFIG_NAME}"

    python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_LOCAL_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_LOCAL_CLUSTER_PATH}"
    python3 "${GEMSHOME}/bin/setup-instance.py" --config "${MD_LOCAL_PRECONFIG_PATH}"

    python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig  Glycomimetics "${GM_LOCAL_PRECONFIG_PATH}" "${GM_GRPC_HOSTNAME}" "${GM_GRPC_HOST}" "${GM_GRPC_PORT}" "${GM_SBATCH_ARGS}" "${GM_LOCAL_PARAMETERS}" "${GM_LOCAL_CLUSTER_PATH}"
    python3 "${GEMSHOME}/bin/setup-instance.py" --config "${GM_LOCAL_PRECONFIG_PATH}"

    python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig MDaaS-RunMD "${MD_REMOTE_PRECONFIG_PATH}" "${MD_GRPC_HOSTNAME}" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}" "${MD_SBATCH_ARGS}" "${MD_LOCAL_PARAMETERS}" "${MD_REMOTE_CLUSTER_PATH}"
    python3 "${GEMSHOME}/bin/setup-instance.py" --generate-preconfig Glycomimetics "${GM_REMOTE_PRECONFIG_PATH}" "${GM_GRPC_HOSTNAME}" "${GM_GRPC_HOST}" "${GM_GRPC_PORT}" "${GM_SBATCH_ARGS}" "${GM_LOCAL_PARAMETERS}" "${GM_REMOTE_CLUSTER_PATH}"
    
    # scp the remote preconfigs (last two generated) to the remote host 
    # then run setup-instance.py --config on them on the remote host
    ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the JSON pre-configuration file.",
    )
    # # store the args to generate preconfig as a list
    parser.add_argument(
        "--generate-preconfig",
        nargs=8,
        metavar=(
            "context",
            "output_path",
            "grpc_hostname",
            "grpc_host",
            "grpc_port",
            "sbatch_args",
            "local_parameters",
            "cluster_filesystem_path",
        ),
        help="Generate a preconfig JSON file.",
    )
    return parser


def generate_preconfig(
    context,
    output_path,
    grpc_hostname,
    grpc_host,
    grpc_port,
    sbatch_args,
    local_parameters,
    cluster_filesystem_path,
):
    """Preconfigs, or Remote configs are necessary to store separate from
    the Instance Configuration so that they can be re-used on the remote host.

    As a remote host can identify itself by it's hostname, it needs it's own host
    entry to know what contexts it supports and will be requested of it by the swarm host.
    """
    config = {
        "hosts": [],
        "filesystem_paths": {},
    }

    # TODO: Use InstanceConfig methods
    host_config = {
        "hostname": grpc_hostname,
        "contexts": [context],
        "host": f"{grpc_host}:{grpc_port}",
        "sbatch_arguments": {context: json.loads(sbatch_args)},
        "local_parameters": {context: json.loads(local_parameters)},
    }

    config["hosts"].append(host_config)
    config["filesystem_paths"][context] = cluster_filesystem_path

    # Generate host-specific JSON configuration file
    with open(output_path, "w") as f:
        json.dump(
            {
                "hosts": [host_config],
                "filesystem_paths": {context: cluster_filesystem_path},
            },
            f,
            indent=2,
        )

    return config


def update_instance_config_from_preconfig(ic, config):
    """When we process a preconfig, or a remote config, we will update the instance config with the new hosts given."""
    for host_config in config.get("hosts", []):
        hostname = host_config["hostname"]
        contexts = host_config["contexts"]
        host, port = host_config["host"].split(":")
        print(
            f"Adding host: {hostname} with contexts: {contexts} and host: {host}:{port}"
        )
        ic.add_host(hostname, host, port, contexts)

        for context, sbatch_args in host_config.get("sbatch_arguments", {}).items():
            ic.add_keyed_arguments_to_host(
                "sbatch_arguments", hostname, context, sbatch_args
            )

        for context, local_params in host_config.get("local_parameters", {}).items():
            ic.add_keyed_arguments_to_host(
                "local_parameters", hostname, context, local_params
            )

    for context, path in config.get("filesystem_paths", {}).items():
        ic.set_filesystem_path(context, path)

    ic.save(force_update=True)


def main():
    """Sets up a GEMS instance for the first time.

    Can be used by a DevEnv or manual GEMS setup.
    """
    ic = InstanceConfig()
    args = argparser().parse_args()

    # TODO/THOUGHT: If the DevEnv should run this, we would need to wrap the python script or pass arguments.
    # Part of the reason we refactored from the granular flags version was to avoid a complicated calling convention.
    if args.generate_preconfig:
        generate_preconfig(*args.generate_preconfig)

    if args.config:
        with open(args.config) as f:
            config = json.load(f)

        update_instance_config_from_preconfig(ic, config)

    return ic


if __name__ == "__main__":
    main()
