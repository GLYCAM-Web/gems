#!/usr/bin/env python3
import sys
import socket

from gemsModules.deprecated.common.loggingConfig import *
from gemsModules.deprecated.batchcompute.slurm.dataio import *
from gemsModules.configuration.main_api import session_instance_config

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def should_use_GRPC():
    pass


def get_gems_slurm_host_from_env():
    return os.getenv("GEMS_GRPC_SLURM_HOST", None), os.getenv(
        "GEMS_GRPC_SLURM_PORT", None
    )


def get_gems_slurm_instance_by_config():
    pass


def is_GEMS_instance_for_SLURM_submission(requested_ctx=None, requested_instance=None):
    """Uses the GEMS instance_config to determine if this instance is the correct SLURM submitter."""
    ic = session_instance_config

    current_hostname = socket.gethostname()
    current_host = None
    if ic.hosts:
        for host in ic.hosts:
            if current_hostname in (host.name, host.address):
                current_host = host
                break
        if not current_host:
            current_host = ic.get_localhost()

    if not current_host or getattr(current_host, "scheduler", None) != "slurm":
        log.debug(f"Current host {current_hostname} does not have a slurm scheduler configured.")
        return False

    this_instance_can_run_ctx = False
    if requested_ctx is not None:
        if requested_ctx in ic.get_available_contexts(current_hostname):
            this_instance_can_run_ctx = True

    this_instance_is_requested = True
    if requested_instance is not None and requested_instance != current_hostname:
        this_instance_is_requested = False

    log.debug(f"Is this instance configured to run SLURM? {this_instance_can_run_ctx}")
    log.debug(f"Is this instance requested for SLURM? {this_instance_is_requested}")
    return this_instance_can_run_ctx and this_instance_is_requested


def naive_is_GEMS_instance_for_SLURM_submission():
    """Naive check which just attempts to get the submission to the configured SLURM host.

    This mimics old behviour.
    """
    this_host = socket.gethostname()
    log.debug(f"This hostname is: {this_host}")
    useGRPC = True

    if this_host is not None and this_host == get_gems_slurm_host_from_env():
        useGRPC = False

    useSLURM = not useGRPC
    log.debug(f"Is this a GEMS instance for SLURM submission? {useSLURM}")
    return useSLURM


def import_grpc_slurm_client():
    global gems_grpc_slurm_client
    from gemsModules.systemoperations.environment_ops import get_gems_path
    gemsPath = get_gems_path()
    sys.path.append(f"{gemsPath}/gRPC/SLURM")
    import gems_grpc_slurm_client

def import_grpc_delegator_client():
    global gems_json_client
    from gemsModules.systemoperations.environment_ops import get_gems_path
    gemsPath = get_gems_path()
    sys.path.append(f"{gemsPath}/gRPC/JSON")
    import json_client as gems_json_client

def slurm_grpc_submit(jsonObjectString, host=None, port=None):
    """Submit a SLURM request to the gRPC server for delegation on another GEMs instance."""
    import_grpc_slurm_client()

    log.debug(
        "Sending SLURM request over gRPC to %s:%s... Request: %s",
        host,
        port,
        jsonObjectString,
    )
    submission = gems_grpc_slurm_client.GemsGrpcSlurmClient(
        json=jsonObjectString, host=host, port=port
    )
    return submission.response


def json_grpc_submit(jsonObjectString, host=None, port=None):
    """Submit a JSON request to the gRPC server for delegation on another GEMs instance."""
    import_grpc_delegator_client()

    log.debug(
        "Sending JSON request over gRPC to %s:%s... Request: %s",
        host,
        port,
        jsonObjectString,
    )
    submission = gems_json_client.JSONClient(
        json=jsonObjectString, host=host, port=port
    )
    return submission.response
