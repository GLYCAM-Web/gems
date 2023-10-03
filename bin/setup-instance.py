#!/usr/bin/env python3
import shutil, argparse, os, sys, json, datetime

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_ops import InstanceConfig


def argparser():
    parser = argparse.ArgumentParser()

    return parser.parse_args()


def configure_md_cluster_host_for_swarm(ic: InstanceConfig):
    """For RunMD to function appropriately, you need to configure your MD host, port and datapath."""

    # Set the MD Cluster host and port to configure the instance_config.json with.
    MD_GRPC_HOST, MD_GRPC_PORT = os.getenv("MD_GRPC_HOST"), os.getenv("MD_GRPC_PORT")
    MD_GRPC_HOSTNAME = os.getenv("MD_GRPC_HOSTNAME")
    if MD_GRPC_HOST is None or MD_GRPC_PORT is None or MD_GRPC_HOSTNAME is None:
        print(
            "MD_GRPC_HOST, MD_GRPC_PORT, and MD_GRPC_HOSTNAME must be set in the environment.\n"
            "Please check GRPC/settings.sh for these settings and re-run this script. See env.json for debugging info.\n"
            f"Got: {MD_GRPC_HOST=}, {MD_GRPC_PORT=}, {MD_GRPC_HOSTNAME=}"
        )
        # dump env
        with open("env.json", "w") as f:
            json.dump(dict(os.environ), f)
        exit(1)

    ic.add_host(
        MD_GRPC_HOSTNAME,
        host=MD_GRPC_HOST,
        slurmport=MD_GRPC_PORT,
        contexts=["MDaaS-RunMD"],
    )

    # we now need to use this to update the instance_config with the appropriate md host.
    md_cluster_path = os.getenv("MD_CLUSTER_USERDATA_BASE_PATH")
    if md_cluster_path == "" or md_cluster_path is None:
        print(
            "MD_CLUSTER_USERDATA_BASE_PATH must be set in the environment.\n"
            "Please set this and re-run this script."
        )

    ic.set_md_filesystem_path(md_cluster_path)

    ic.save(ic.get_default_path())

    # print out the newly added host sub-dict because it will be useful for configuring the MD cluster host.
    print(
        "Added the following MD Cluster host to the instance_config.json:\n"
        f'"{MD_GRPC_HOSTNAME}":\n{json.dumps(ic["hosts"][MD_GRPC_HOSTNAME], indent=2)}\n'
        "(you can use this entry to help initialize the MD cluster host)"
    )


def main():
    """Sets up a GEMS instance for the first time.

    Can be used by a DevEnv or manual GEMS setup.
    """
    print("About to configure this GEMS instance...")
    # args = argparser()
    ic = InstanceConfig()

    # Don't reconfigure unless forced.
    if ic.is_configured or os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True":
        print("Backing up current instance_config.json...")
        shutil.move(
            ic.get_default_path(),
            ic.get_default_path().with_name(
                f"instance_config.json.{datetime.datetime.now()}.bak"
            ),
        )
        # ic.is_configured should now return False

    if not ic.is_configured:
        print("Copying instance_config.json.example into place...")
        shutil.copyfile(
            ic.get_default_path(example=True),
            ic.get_default_path(),
        )

        configure_md_cluster_host_for_swarm(ic)


if __name__ == "__main__":
    main()
