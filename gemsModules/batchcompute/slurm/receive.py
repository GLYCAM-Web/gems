#!/usr/bin/env python3
import sys, os, socket
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
    log.info("batchcompute.slurm.receive() was called on %s", socket.gethostname())
    log.debug(
        "incoming jsonObjectString: \n" + str(jsonObjectString)
    )  # Actually a dict? SlurmJobInfo?

    # Make a new SlurmJobInfo object for holding I/O information.
    # TODO: newstyle gemsModule - this should be broken out into TransactionManager.
    thisSlurmJobInfo = SlurmJobInfo(jsonObjectString)
    thisSlurmJobInfo.parseIncomingString()

    # Get context from SlurmJobInfo, this could be overwritten based on instance config settings.
    ctx = thisSlurmJobInfo.incoming_dict["context"]

    thisSlurmJobInfo.incoming_dict["slurm_runscript_name"] = "slurm_submit.sh"
    slurm_runscript_path = (
        thisSlurmJobInfo.incoming_dict["workingDirectory"]
        + "/"
        + thisSlurmJobInfo.incoming_dict["slurm_runscript_name"]
    )

    # TODO: This can probably move to the "is correct instance for SLURM submit"
    log.debug("Slurm runscript path: " + slurm_runscript_path + "\n")
    if os.path.exists(slurm_runscript_path):
        log.debug("Found existing Slurm runscript.  Refusing to clobber.")
    else:
        log.debug("Will generate a new Slurm runscript.")

        log.debug("About to create runscript")
        create_contextual_slurm_submission_script(
            ctx, slurm_runscript_path, thisSlurmJobInfo
        )

    # TODO/Q: We might want this "requested context branch" to be more interchangeable.
    log.debug(
        "Checking if this instance is configured to run SLURM. %s %s %s",
        socket.gethostname(),
        jsonObjectString,
        ctx,
    )

    # TODO: PM needs to be run on appropriate host.
    if is_GEMS_instance_for_SLURM_submission(requested_ctx=ctx):
        log.debug(
            "This instance is configured to run SLURM. host=%s requested_ctx=%s",
            os.uname(),
            ctx,
        )
        response = slurm_submit(thisSlurmJobInfo)
    else:
        log.debug(
            "This instance is not configured to run SLURM. host=%s requested_ctx=%s",
            os.uname(),
            ctx,
        )
        # Needs to be a proper GEMS response.
        # TODO/FIX!: This probably needs to be daemonized to not block a gems response before slurm batching.
        # response = seek_correct_host(jsonObjectString, context=ctx)
        # Daemonic seek_correct_host / disowned/nohup
        #
        # This change allows a response, but still gems/grpc_server deadlock.
        from multiprocessing import Process

        p = Process(target=seek_correct_host, args=(jsonObjectString, ctx))
        p.start()

        # TODO: Append this to actual resposne
        response = {
            "notices": ["Seeking correct host for SLURM submission.  Check back later."]
        }

    return response
