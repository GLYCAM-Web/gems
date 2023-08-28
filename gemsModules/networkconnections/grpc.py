#!/usr/bin/env python3
import sys
import socket

from pydantic import BaseModel, Field
from pydantic.schema import schema
from pydantic import BaseModel, Field

from gemsModules.deprecated.common import transaction
from gemsModules.deprecated.common.loggingConfig import *

from gemsModules.deprecated.batchcompute.slurm.dataio import *


from gemsModules.structurefile.PDBFile.main_settings import WhoIAm

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# gross coupling of slurm submit in batch compute to grpc submissions.
# simplest solution is allowing us to pass a closure to this grpc_submit for the local submit fn.
# that sounds wrong though.
def slurm_grpc_submit(jsonObjectString, thisSlurmJobInfo, gems_grpc_host_port=None):
    useGRPC = True
    # TODO: We probably want to lift the gems instance selection out of slurm grpc_submit.
    # It should probably be figured out earlier in gems. ETA: Now in transit.

    thePort = gems_grpc_host_port or os.environ.get("GEMS_GRPC_SLURM_PORT")
    log.debug("the port is: " + thePort)
    if thePort is None:
        log.debug("cant find grpc slurm submission port. using localhost")
        useGRPC = False
    theHost = os.environ.get("GEMS_GRPC_SLURM_HOST")
    log.debug("the host is: " + theHost)
    if theHost is None:
        log.debug("cant find grpc slurm submission host. using localhost")
        useGRPC = False
    else:
        localHost = socket.gethostname()
        log.debug("the local host is: " + localHost)
        if theHost == localHost:
            useGRPC = False

    log.debug("useGRPC: " + str(useGRPC))
    if useGRPC:
        gemsPath = os.environ.get("GEMSHOME")
        if gemsPath is None:
            return "Cannot determine GEMSHOME."
        sys.path.append(gemsPath + "/gRPC/SLURM")
        import grpc
        import gems_grpc_slurm_client

        log.debug("submitting to gems_grpc_slurm_client.")
        submission = gems_grpc_slurm_client.GemsGrpcSlurmClient(json=jsonObjectString)
        return submission.response

    else:
        # TODO/NOTE: Just a hack as I try to pull grpc out of batchcompute
        from gemsModules.deprecated.batchcompute.slurm.receive import submit

        log.debug("not using grpc.")
        theResponse = submit(thisSlurmJobInfo)
        if theResponse is None:
            log.error("Got none response")
            ##TODO: return a proper error response
        else:
            thisSlurmJobInfo.copyJobinfoInToOut()
            thisSlurmJobInfo.addSbatchResponseToJobinfoOut(theResponse)
            log.debug("The outgoing dictionary is: \n")
            log.debug(str(thisSlurmJobInfo.outgoing_dict))
            log.debug("\n")
            return thisSlurmJobInfo.outgoing_dict


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


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
