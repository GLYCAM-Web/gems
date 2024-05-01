#!/usr/bin/env python3
import argparse, os, sys, json, re
import socket

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)
sys.path.append(
    GemsPath + "/gemsModules"
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
        "--add-host",
        type=str,
        nargs=3,
        help="Add a host to the instance_config.json. Format: 'hostname,contexts,host:port'",
    )

    parser.add_argument(
        "--set-sbatch-arguments",
        type=str,
        nargs=3,
        help="Set the sbatch_arguments for a host in the instance_config.json. Format: 'hostname,context,sbatch_arguments'",
    )

    parser.add_argument(
        "--set-local-parameters",
        type=str,
        nargs=3,
        help="Set the local_parameters for a host in the instance_config.json. Format: 'hostname,context,local_parameters'",
    )

    parser.add_argument(
        "--gen-remote-cluster-config",
        type=str,
        help="Generate a partial remote MD cluster config file for the MD cluster host with the given filesystem path.",
    )

    parser.add_argument(
        "--set-cluster-filesystem-path",
        type=str,
        nargs=2,
        help="Sets a particular cluster_filesystem_path for a cluster host. Ex. MDaaS or Glycomimetics",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print out what would be done without actually doing it.",
    )

    return parser


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

    SAVE = False

    if args.add_host is not None:
        hostname, contexts, hostport = args.add_host
        host, port = hostport.split(":")
        contexts = contexts.strip("[]").split(",")
        print(
            f"Adding host: {hostname} with contexts: {contexts} and host: {host}:{port}"
        )
        ic.add_host(hostname, host, port, contexts)
        SAVE = True

    if args.set_sbatch_arguments is not None:
        sbatch_hostname, sbatch_context, sbatch_arguments = args.set_sbatch_arguments

        if ip_regex.match(sbatch_hostname):
            print(f"Instance hostname is an IP: {sbatch_hostname}")
            try:
                sbatch_hostname = socket.gethostbyaddr(sbatch_hostname)[0]
            except socket.herror:
                raise ValueError(
                    f"Unable to resolve the GEMS host IP: {sbatch_hostname}"
                )

        sbatch_arguments = json.loads(sbatch_arguments)
        ic.add_keyed_arguments_to_host(
            "sbatch_arguments", sbatch_hostname, sbatch_context, sbatch_arguments
        )
        SAVE = True

    if args.set_local_parameters is not None:
        local_parameters_hostname, local_parameters_context, local_parameters = (
            args.set_local_parameters
        )
        local_parameters = json.loads(local_parameters)
        ic.add_keyed_arguments_to_host(
            "local_parameters",
            local_parameters_hostname,
            local_parameters_context,
            local_parameters,
        )
        SAVE = True

    if args.set_cluster_filesystem_path is not None:
        app, path = args.set_cluster_filesystem_path
        ic.set_filesystem_path(app, path)
        SAVE = True

    if args.gen_remote_cluster_config is not None:
        if args.add_host is None:
            raise RuntimeError(
                "Cannot generate a remote MD cluster config without adding a host first, please try again."
            )
        print(args.gen_remote_cluster_config)
        app = args.gen_remote_cluster_config
        generating_cmd = (
            f"python3 $GEMSHOME/bin/setup-instance.py \\\n"
            f"--add-host '{hostname}' '[{app}]' '{host}' '{port}' \\\n"
            f"--set-sbatch-arguments '{hostname}' '{app}' '{json.dumps(ic['hosts'][hostname]['sbatch_arguments'][app])}' \\\n"
            f"--set-local-parameters '{hostname}' '{app}' '{json.dumps(ic['hosts'][hostname]['local_parameters'][app])}' \\\n"
            f"--set-cluster-filesystem-path {app} {ic['cluster_filesystem_paths'][app]}"
        )

        if not args.dry_run:
            print(
                "Please use the following command on the MD Cluster host if you have not already synchronized your instances:\n\n"
                f"{generating_cmd}\n\n(Ignore this message if you are in a DevEnv, it has been done for you.)\n"
            )

            with open(
                os.path.join(
                    GemsPath,
                    f"REMOTE_{app}_CLUSTER_HOST_SETUP-git-ignore-me.sh",
                ),
                "w",
            ) as f:
                # write bash header - removing it just makes copy-pasting easier and we haven't chmodded it yet anyways.
                # f.write("#!/bin/bash\n\n")
                f.write(f"{generating_cmd}\n")
                print(
                    f"Wrote out $GEMSHOME/REMOTE_{app}_CLUSTER_HOST_SETUP-git-ignore-me.sh"
                )
        else:
            print(
                "Dry run: Did not write out $GEMSHOME/REMOTE_{app}_CLUSTER_HOST_SETUP-git-ignore-me.sh\nWould have written:\n"
                f"{generating_cmd}"
            )
        SAVE = True

    if SAVE:
        ic.save()

    return ic


if __name__ == "__main__":
    main()
