#!/usr/bin/env python3
import traceback
import os, sys, subprocess, signal
import grpc 

from gemsModules.networkconnections.grpc import slurm_grpc_submit
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def execute(jsonObjectString, context):
    """Using gRPC, try to reroute the request to the correct host given a context, usually the current one."""

    addresses = InstanceConfig().get_possible_hosts_for_context(
        context, with_slurmport=True
    )

    failed = False
    tried = []
    response = None
    while len(addresses):
        h, p = addresses.pop().split(":")
        try:
            response = slurm_grpc_submit(jsonObjectString, host=h, port=p)
            failed = False
            break
        except grpc.RpcError:
            failed = True
            log.warning(
                "Failed to submit to %s:%s. Trying next host in list.",
                h,
                p,
                exc_info=True,
            )
        finally:
            tried.append(h)

    if failed:
        log.error(
            "All attempts to make a SLURM submission over gRPC failed. servers tried: %s",
            tried,
        )

    return response
