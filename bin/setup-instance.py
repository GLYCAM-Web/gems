#!/usr/bin/env python3
import shutil, argparse, os, sys, json, datetime

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_ops import InstanceConfig


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


def configure_instance_config_md(args):
    print("\nAbout to configure this GEMS instance...")
    ic = InstanceConfig()

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
        ic.add_sbatch_arguments_to_host(
            sbatch_hostname, sbatch_context, sbatch_arguments
        )
        SAVE = True

    if args.gen_remote_md_cluster_config is not None:
        md_cluster_host_config_str = (
            f'"{hostname}":\n{json.dumps(ic["hosts"][hostname], indent=2)},\n'
            f'"md_cluster_filesystem_path": "{args.gen_remote_md_cluster_config}"\n\n'
        )

        # print out the newly added host sub-dict because it will be useful for configuring the MD cluster host.
        print(
            "Added the following json keys to the instance_config.json:\n\n"
            + md_cluster_host_config_str
            + "(you can use this entry to help initialize the MD cluster host, but the\n"
            "given md_cluster_filesystem_path is only valid for the MD host thoreau.)\n\n"
            "Simply ignore this notice if you are in a DevEnv as no further configuration is necessary.\n"
        )
        with open(
            os.path.join(GemsPath, "MD_CLUSTER_HOST_PARTIAL_CONFIG-git-ignore-me.json"),
            "w",
        ) as f:
            f.write(md_cluster_host_config_str)
            print(
                "Wrote out $GEMSHOME/MD_CLUSTER_HOST_PARTIAL_CONFIG-git-ignore-me.json"
            )

    if SAVE:
        ic.save(ic.get_default_path())


def main():
    """Sets up a GEMS instance for the first time.

    Can be used by a DevEnv or manual GEMS setup.
    """
    args = argparser().parse_args()

    # Don't reconfigure unless forced, back up if forced.
    if (
        InstanceConfig.is_configured()
        and os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
    ):
        print("Backing up current instance_config.json...")
        shutil.move(
            InstanceConfig.get_default_path(),
            InstanceConfig.get_default_path().with_name(
                f"instance_config.json.{datetime.datetime.now()}.bak"
            ),
        )
        # ic.is_configured should now return False

    # Configure the instance_config.json if it is not already configured.
    if (
        not InstanceConfig.is_configured()
        or os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
    ):
        print("Copying instance_config.json.example into place...")
        shutil.copyfile(
            InstanceConfig.get_default_path(example=True),
            InstanceConfig.get_default_path(),
        )

        configure_instance_config_md(args)


if __name__ == "__main__":
    main()
