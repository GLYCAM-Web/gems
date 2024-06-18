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


def generate_preconfig(
    contexts,
    grpc_hostnames,
    grpc_hosts,
    grpc_ports,
    sbatch_args_list,
    local_parameters_list,
    cluster_filesystem_paths,
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

    prefixes = list(contexts.keys())

    for i, prefix in enumerate(prefixes):
        grpc_hostname = grpc_hostnames[i]
        grpc_host = grpc_hosts[i]
        grpc_port = grpc_ports[i]
        sbatch_args = sbatch_args_list[i]
        local_parameters = local_parameters_list[i]
        cluster_filesystem_path = cluster_filesystem_paths[i]

        context = contexts[prefix]

        # TODO: use instance config for validation?
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
        with open(
            f"{os.getenv('GEMSHOME')}/REMOTE_{prefix}_preconfig-git-ignore-me.json", "w"
        ) as f:
            json.dump(
                {
                    "hosts": [host_config],
                    "filesystem_paths": {context: cluster_filesystem_path},
                },
                f,
                indent=2,
            )

    return config


def update_instance_config_hosts_from_preconfig(ic, config):
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


def _devenv_generate_preconfig():
    """GLYCAM-Web DevEnv specific

    the gRPC image configures the Instance Configuration, as gRPC is used to route requests
    to hosts known by the instance configuration. GLYCAM-Web's DevEnv stores its hosts
    as environmental variables.

    TODO/THOUGHT: I might want the GRPC/bin/initialize.sh script to perform this logic, but
    it's easier in python to write json. - Grayson M.
    """

    def check_env_var(var_name):
        value = os.getenv(var_name)
        if not value:
            raise RuntimeError(
                f"Environment variable {var_name} is required but not set."
            )
        return value

    context_mapping = check_env_var("GEMS_REMOTE_EXE_CTX_MAP")
    contexts = json.loads(context_mapping)

    grpc_hostnames = []
    grpc_hosts = []
    grpc_ports = []
    sbatch_args_list = []
    local_parameters_list = []
    cluster_filesystem_paths = []

    for prefix in contexts.keys():
        grpc_hostnames.append(check_env_var(f"{prefix}_GRPC_HOSTNAME"))
        grpc_hosts.append(check_env_var(f"{prefix}_GRPC_HOST"))
        grpc_ports.append(check_env_var(f"{prefix}_GRPC_PORT"))

        sbatch_args = check_env_var(f"{prefix}_SBATCH_ARGS")
        try:
            sbatch_args_list.append(json.loads(sbatch_args))
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON in {prefix}_SBATCH_ARGS: {sbatch_args}")

        local_parameters = check_env_var(f"{prefix}_LOCAL_PARAMETERS")
        try:
            local_parameters_list.append(json.loads(local_parameters))
        except json.JSONDecodeError:
            raise RuntimeError(
                f"Invalid JSON in {prefix}_LOCAL_PARAMETERS: {local_parameters}"
            )

        cluster_filesystem_paths.append(
            check_env_var(f"{prefix}_CLUSTER_FILESYSTEM_PATH")
        )

    return generate_preconfig(
        contexts,
        grpc_hostnames,
        grpc_hosts,
        grpc_ports,
        sbatch_args_list,
        local_parameters_list,
        cluster_filesystem_paths,
    )


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

    # TODO/THOUGHT: If the DevEnv should run this, we would need to wrap the python script or pass arguments.
    # Part of the reason we refactored from the granular flags version was to avoid a complicated calling convention.
    if args.generate_preconfig:
        _devenv_generate_preconfig()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)

        update_instance_config_hosts_from_preconfig(ic, config)

    return ic


if __name__ == "__main__":
    main()
