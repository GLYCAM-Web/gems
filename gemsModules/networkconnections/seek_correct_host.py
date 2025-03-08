#!/usr/bin/env python3
import traceback
import os, sys, subprocess, signal
import grpc 
import json
from typing import Literal

from gemsModules.networkconnections.grpc import slurm_grpc_submit, json_grpc_submit
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)



def execute(jsonObjectString, context, submission_fn_type: Literal["slurm", "json"]="slurm"):
    """Using gRPC, try to reroute the request to the correct host given a context, usually the current one."""
    if submission_fn_type == "slurm":
        submission_fn = slurm_grpc_submit
    elif submission_fn_type == "json":
        submission_fn = json_grpc_submit
    else:
        log.error("Invalid submission_fn_type: %s", submission_fn_type)
        raise ValueError(f"Invalid submission_fn_type: {submission_fn_type}")

    addresses = InstanceConfig().get_possible_hosts_for_context(
        context, with_slurmport=True
    )

    failed = False
    tried = []
    response = {}
    while len(addresses):
        h, p = addresses.pop().split(":")
        try:
            response = submission_fn(jsonObjectString, host=h, port=p)
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
            tried.append(f"{h}:{p}")

    if failed:
        log.error(
            "All attempts to make a SLURM submission over gRPC failed. servers tried: %s",
            tried,
        )
        response = {"Errors": ["All attempts to make a SLURM submission over gRPC failed."],
                    "Tried servers": tried}

    if isinstance(response, dict):
        response = json.dumps(response)
        
    return response
