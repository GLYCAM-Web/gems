#!/usr/bin/env python3
import shutil, argparse, os, sys, json, datetime

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_config import InstanceConfig, DateReversioner


def argparser():
    """
    ```bash
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --add-host "${MD_GRPC_HOSTNAME};[MDaaS-RunMD];${MD_GRPC_HOST}:${MD_GRPC_PORT}"
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --set-sbatch-arguments "${MD_GRPC_HOSTNAME};MDaaS-RunMD;${SBATCH_ARGS}"
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --set-md-cluster-filesystem-path $MD_CLUSTER_FILESYSTEM_PATH
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --gen_md_cluster_host_config
    ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--add-host",
        type=str,
        help="Add a host to the instance_config.json. Format: 'hostname,contexts,host:port'",
    )

    parser.add_argument(
        "--set-sbatch-arguments",
        type=str,
        help="Set the sbatch_arguments for a host in the instance_config.json. Format: 'hostname,context,sbatch_arguments'",
    )

    parser.add_argument(
        "--set-local-parameters",
        type=str,
        help="Set the local_parameters for a host in the instance_config.json. Format: 'hostname,context,local_parameters'",
    )

    parser.add_argument(
        "--gen-remote-md-cluster-config",
        type=str,
        help="Generate a partial remote MD cluster config file for the MD cluster host with the given filesystem path.",
    )

    parser.add_argument(
        "--set-md-cluster-filesystem-path",
        type=str,
        help="Sets the md_cluster_filesystem_path for the MD cluster host.",
    )

    return parser


def main():
    """Sets up a GEMS instance for the first time.

    Can be used by a DevEnv or manual GEMS setup.
    """
    force_reconfiguration = os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
    if force_reconfiguration or not InstanceConfig.is_configured:
        print("\nAbout to configure this GEMS instance...")
    else:
        print("\nThis GEMS instance is already configured. Exiting.")
        return

    args = argparser().parse_args()
    ic = InstanceConfig()
    if len(ic.config) and "date" not in ic.config:
        # Using an old instance config, lets get the example to modify instead.
        # Theoretically, setup-instance.py can update configs rather than just recreate them.
        ic.set_active_config(ic.get_default_path(example=True))

    SAVE = False
    if args.set_md_cluster_filesystem_path is not None:
        ic.set_md_filesystem_path(args.set_md_cluster_filesystem_path)
        SAVE = True

    if args.add_host is not None:
        hostname, contexts, hostport = args.add_host.split(";")
        host, port = hostport.split(":")
        contexts = contexts.strip("[]").split(",")
        print(
            f"Adding host: {hostname} with contexts: {contexts} and host: {host}:{port}"
        )
        ic.add_host(hostname, host, port, contexts)
        SAVE = True

    if args.set_sbatch_arguments is not None:
        (
            sbatch_hostname,
            sbatch_context,
            sbatch_arguments,
        ) = args.set_sbatch_arguments.split(";")
        sbatch_arguments = json.loads(sbatch_arguments)
        ic.add_keyed_arguments_to_host(
            "sbatch_arguments", sbatch_hostname, sbatch_context, sbatch_arguments
        )
        SAVE = True

    if args.set_local_parameters is not None:
        (
            local_parameters_hostname,
            local_parameters_context,
            local_parameters,
        ) = args.set_local_parameters.split(";")
        local_parameters = json.loads(local_parameters)
        ic.add_keyed_arguments_to_host(
            "local_parameters",
            local_parameters_hostname,
            local_parameters_context,
            local_parameters,
        )
        SAVE = True

    if SAVE:
        saved = ic.save()
        if saved and args.gen_remote_md_cluster_config is not None:
            if args.add_host is None:
                raise RuntimeError(
                    "Cannot generate a remote MD cluster config without adding a host first, please try again."
                )

            md_cluster_host_config_str = (
                f'"{hostname}":\n{json.dumps(ic.config["hosts"][hostname], indent=2)},\n'
                f'"md_cluster_filesystem_path": "{args.gen_remote_md_cluster_config}"\n\n'
            )

            # print out the newly added host sub-dict because it will be useful for configuring the MD cluster host.
            print(
                "Added the following json keys to the instance_config.json:\n\n"
                + md_cluster_host_config_str
                + "(you can use this entry to help initialize the MD cluster host.)\n"
                "Simply ignore this notice if you are in a DevEnv as no further configuration is necessary.\n"
            )
            with open(
                os.path.join(
                    GemsPath, "MD_CLUSTER_HOST_PARTIAL_CONFIG-git-ignore-me.json"
                ),
                "w",
            ) as f:
                f.write(md_cluster_host_config_str)
                print(
                    "Wrote out $GEMSHOME/MD_CLUSTER_HOST_PARTIAL_CONFIG-git-ignore-me.json"
                )

    return ic


if __name__ == "__main__":
    main()
