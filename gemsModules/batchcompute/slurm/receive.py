#!/usr/bin/env python3
import sys, os
import traceback

import grpc

import gemsModules.deprecated
import gemsModules.deprecated.batchcompute.settings as batchcomputeSettings

from gemsModules.deprecated import common
from gemsModules.deprecated.common.services import *
from gemsModules.deprecated.common.transaction import *  # might need whole file...
from gemsModules.deprecated.batchcompute.slurm.dataio import *
from gemsModules.deprecated.batchcompute.slurm.receive import manageIncomingString


# TODO: Make proper tasks
from gemsModules.batchcompute.slurm.tasks.do_slurm_submission import (
    slurm_submit,
)
from gemsModules.batchcompute.slurm.tasks.prepare_slurm_submission import (
    seek_correct_host,
    create_contextual_slurm_submission_script,
)


from gemsModules.networkconnections.grpc import (
    is_GEMS_instance_for_SLURM_submission,
)

from gemsModules.systemoperations.instance_ops import InstanceConfig
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def receive(jsonObjectString):
    """
    TODO write me a docstring
    """
    import os, sys, socket

    log.info("batchcompute.slurm.receive() was called.\n")
    log.debug(
        "incoming jsonObjectString: \n" + str(jsonObjectString)
    )  # Actually a dict? SlurmJobInfo?

    # Make a new SlurmJobInfo object for holding I/O information.
    # TODO: newstyle gemsModule - this should be broken out into TransactionManager.
    thisSlurmJobInfo = SlurmJobInfo(jsonObjectString)
    thisSlurmJobInfo.parseIncomingString()

    thisSlurmJobInfo.incoming_dict["slurm_runscript_name"] = "slurm_submit.sh"
    slurm_runscript_path = (
        thisSlurmJobInfo.incoming_dict["workingDirectory"]
        + "/"
        + thisSlurmJobInfo.incoming_dict["slurm_runscript_name"]
    )

    create_runscript = False
    log.debug("Slurm runscript path: " + slurm_runscript_path + "\n")
    if os.path.exists(slurm_runscript_path):
        log.debug("Found existing Slurm runscript.  Refusing to clobber.")
    else:
        log.debug("Will generate a new Slurm runscript.")
        create_runscript = True

    # If grpc-delegator, we want to reroute to the correct host with gRPC.
    # See instance_config.json for info on available hosts and contexts.

    response = None
    # TODO/Q: We might want this "requested context branch" to be more interchangeable subcomponents of the slurm entity.
    # TODO/FIX: Right now, it's just checking if the requested context is for MDaaS-RunMD.
    # But it needs to check if the request in the jsonObjectString is for runmd first.
    ctx = "MDaaS-RunMD"
    if is_GEMS_instance_for_SLURM_submission(requested_ctx=ctx):
        if create_runscript:
            log.debug("About to create runscript")
            create_contextual_slurm_submission_script(
                slurm_runscript_path, thisSlurmJobInfo, context=ctx
            )
        slurm_submit(thisSlurmJobInfo)
    else:
        seek_correct_host(jsonObjectString, context=ctx)
