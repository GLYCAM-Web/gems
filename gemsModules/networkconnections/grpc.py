#!/usr/bin/env python3
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


def get_gems_slurm_host():
    return os.getenv("GEMS_GRPC_SLURM_HOST", None), os.getenv(
        "GEMS_GRPC_SLURM_PORT", None
    )


def is_GEMS_instance_for_SLURM_submission(requesting_ctx=None, requested_instance=None):
    """Uses the GEMS instance_config to determine if this instance is the correct SLURM submitter."""


def _is_GEMS_instance_for_SLURM_submission():
    """Naive check which just attempts to get the submission to the configured SLURM host."""
    this_host = socket.gethostname()
    log.debug(f"This hostname is: {this_host}")
    useGRPC = True

    if this_host is not None and this_host == get_gems_slurm_host():
        useGRPC = False

    useSLURM = not useGRPC
    log.debug(f"Is this a GEMS instance for SLURM submission? {useSLURM}")
    return useSLURM


def _is_correct_GEMS_instance(gems_grpc_host_port=None):
    """Replicates original deprecated/batchcompute behaviour"""
    log.debug(f"This hostname is: {socket.gethostname()}")
    useGRPC = True

    host, port = get_gems_slurm_host().split(":")
    if gems_grpc_host_port is not None:
        host, port = gems_grpc_host_port.split(":")
        port = int(port)

    log.debug("the host is: " + host)
    if host is None:
        log.debug("cant find grpc slurm submission host. using localhost")
        useGRPC = False
    else:
        if host == socket.gethostname():
            useGRPC = False

    return useGRPC


def import_grpc_client():
    global gems_grpc_slurm_client
    gemsPath = os.environ.get("GEMSHOME")
    if gemsPath is None:
        log.warning("GEMSHOME is not set.  Cannot submit via gRPC.")
        return "Failed to submit via gRPC.  GEMSHOME is not set."
    sys.path.append(f"{gemsPath}/gRPC/SLURM")
    import gems_grpc_slurm_client


# gross coupling of slurm submit in batch compute to grpc submissions.
# simplest solution is allowing us to pass a closure to this grpc_submit for the local submit fn.
# that sounds wrong though.
def slurm_grpc_submit(jsonObjectString):
    """ """
    import_grpc_client()

    log.debug("submitting to gems_grpc_slurm_client.")
    # TODO: This needs to be able to take a host/port
    submission = gems_grpc_slurm_client.GemsGrpcSlurmClient(json=jsonObjectString)
    return submission.response


# schedulerGrpcHost: str = Field(
#    None,
#    title='Scheduler gRPC server',
#    description='The server to contact via gRPC for submitting the job.  Normally not required.'
#    )
# schedulerGrpcPort: int = Field(
#    None,
#    title='Scheduler gRPC port',
#    description='The port to contact via gRPC for submitting the job.  Normally not required.'
#    )
