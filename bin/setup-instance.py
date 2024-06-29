#!/usr/bin/env python3
import argparse, os, sys, json


GEMSHOME = os.environ.get("GEMSHOME")
sys.path.append(GEMSHOME)
sys.path.append(
    GEMSHOME + "/gemsModules"
)  # Swarm needs /gemsModules. These sys path hacks would be simplified if we used pip to install gems.
from gemsModules.systemoperations.instance_config import InstanceConfig


def argparser():
    """
    ```bash
        $ python3 "${GEMSHOME}/bin/setup-instance.py" --add-host "${MD_GRPC_HOSTNAME}" "[MDaaS-RunMD]" "${MD_GRPC_HOST}" "${MD_GRPC_PORT}"
        $ python3 "${GEMSHOME}/bin/setup-instance.py" --set-sbatch-arguments "${MD_GRPC_HOSTNAME}" "MDaaS-RunMD" "${SBATCH_ARGS}"
        $ python3 "${GEMSHOME}/bin/setup-instance.py" --set-cluster-filesystem-path "MDaaS-RunMD" "$MD_CLUSTER_FILESYSTEM_PATH"
        $ python3 "${GEMSHOME}/bin/setup-instance.py" --gen-remote-cluster-config "MDaaS-RunMD"
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

    ic.save()


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
