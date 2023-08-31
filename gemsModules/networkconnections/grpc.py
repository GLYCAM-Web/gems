#!/usr/bin/env python3
import json
import sys
import socket
from typing_extensions import Literal
import grpc

from pydantic import BaseModel, Field
from pydantic.schema import schema
from pydantic import BaseModel, Field

from gemsModules.deprecated.common import transaction
from gemsModules.deprecated.common.loggingConfig import *

from gemsModules.deprecated.batchcompute.slurm.dataio import *

from gemsModules.systemoperations.instance_ops import InstanceConfig

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
    ic = InstanceConfig()

    this_instance_can_run_ctx = False
    if requested_ctx is not None:
        if requested_ctx in ic.get_available_contexts():
            this_instance_can_run_ctx = True

    this_instance_is_requested = False
    if requested_instance is not None:
        if requested_instance == socket.gethostname():
            this_instance_is_requested = True

    return this_instance_can_run_ctx and this_instance_is_requested


def naive_is_GEMS_instance_for_SLURM_submission():
    """Naive check which just attempts to get the submission to the configured SLURM host."""
    this_host = socket.gethostname()
    log.debug(f"This hostname is: {this_host}")
    useGRPC = True

    if this_host is not None and this_host == get_gems_slurm_host_from_env():
        useGRPC = False

    useSLURM = not useGRPC
    log.debug(f"Is this a GEMS instance for SLURM submission? {useSLURM}")
    return useSLURM


def import_grpc_client():
    global gems_grpc_slurm_client
    gemsPath = os.environ.get("GEMSHOME")
    if gemsPath is None:
        log.warning("GEMSHOME is not set.  Cannot submit via gRPC.")
        # raise EnvironmentError("Failed to submit via gRPC.  GEMSHOME is not set.")
    sys.path.append(f"{gemsPath}/gRPC/SLURM")
    import gems_grpc_slurm_client


def slurm_grpc_submit(jsonObjectString, host=None, port=None):
    """Submit a SLURM request to the gRPC server for delegation on another GEMs instance."""
    import_grpc_client()

    log.debug("Sending SLURM request over gRPC to %s:%s...", host, port)
    submission = gems_grpc_slurm_client.GemsGrpcSlurmClient(
        json=jsonObjectString, host=host, port=port
    )
    return json.loads(submission.response)
