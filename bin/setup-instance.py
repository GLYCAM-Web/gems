#!/usr/bin/env python3
import argparse, os, sys, json, re
import socket

GEMSHOME = os.environ.get("GEMSHOME")
sys.path.append(GEMSHOME)
sys.path.append(
    GEMSHOME + "/gemsModules"
)  # Swarm needs /gemsModules. These sys path hacks would be simplified if we used pip to install gems.
from gemsModules.systemoperations.instance_config import InstanceConfig


ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


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
    parser.add_argument(
        "--generate-preconfig",
        action="store_true",
        help="Generate a pre-configuration file for GEMS.",
    )

    return parser


def generate_preconfig():
    config = {
        "hosts": [],
        "filesystem_paths": {},
    }

    for prefix in ["MD", "GM"]:
        grpc_hostname = os.getenv(f"{prefix}_GRPC_HOSTNAME")
        grpc_host = os.getenv(f"{prefix}_GRPC_HOST")
        grpc_port = os.getenv(f"{prefix}_GRPC_PORT")
        sbatch_args = json.loads(os.getenv(f"{prefix}_SBATCH_ARGS"))
        local_parameters = json.loads(os.getenv(f"{prefix}_LOCAL_PARAMETERS"))
        cluster_filesystem_path = os.getenv(f"{prefix}_CLUSTER_FILESYSTEM_PATH")

        if prefix == "MD":
            context = "MDaaS-RunMD"
        elif prefix == "GM":
            context = "Glycomimetics"

        host_config = {
            "hostname": grpc_hostname,
            "contexts": [context],
            "host": f"{grpc_host}:{grpc_port}",
            "sbatch_arguments": {context: sbatch_args},
            "local_parameters": {context: local_parameters},
        }

        config["hosts"].append(host_config)
        config["filesystem_paths"][context] = cluster_filesystem_path

        # Generate host-specific JSON configuration file
        with open(f"{GEMSHOME}/REMOTE_{prefix}_preconfig-git-ignore-me.json", "w") as f:
            json.dump(
                {
                    "hosts": [host_config],
                    "filesystem_paths": {context: cluster_filesystem_path},
                },
                f,
                indent=2,
            )

    # with open(f"{GEMSHOME}/preconfig-git-ignore-me.json", "w") as f:
    #     json.dump(config, f, indent=2)


def process_preconfig(ic, config):
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

    force_reconfiguration = os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
    if force_reconfiguration or not ic.is_configured:
        print("\nAbout to configure this GEMS instance...")
    else:
        print("\nThis GEMS instance is already configured. Exiting.")
        return

    if args.generate_preconfig:
        generate_preconfig()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)

        process_preconfig(ic, config)

    return ic


if __name__ == "__main__":
    main()
