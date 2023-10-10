#!/usr/bin/env python3
import pdb
import sys, os, socket
import traceback
import grpc
from datetime import datetime
from multiprocessing import Process

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
from gemsModules.systemoperations.instance_ops import InstanceConfig

from gemsModules.networkconnections.grpc import (
    is_GEMS_instance_for_SLURM_submission,
)

from gemsModules.systemoperations.instance_ops import InstanceConfig
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.logging.logger import new_concurrent_logger


log = new_concurrent_logger(__name__)


def receive(jsonObjectString):
    """batchcompute.slurm Entity reception module.

    This is more or less an intermediate on the way to a proper new-style entity.
    """
    log.info("batchcompute.slurm.receive() was called on %s", socket.gethostname())
    log.debug(
        "incoming jsonObjectString: \n" + str(jsonObjectString)
    )  # Actually a dict? SlurmJobInfo?

    # Make a new SlurmJobInfo object for holding I/O information.
    # TODO: newstyle gemsModule - this should be broken out into TransactionManager.
    thisSlurmJobInfo = SlurmJobInfo(jsonObjectString)
    thisSlurmJobInfo.parseIncomingString()

    log.debug(
        "Checking if this instance is configured to run SLURM. %s %s %s",
        socket.gethostname(),
        jsonObjectString,
        thisSlurmJobInfo.incoming_dict,
    )

    # Only works in dev mode, not in production, because same md cluster path is used (and mounted to volumes in the same places).
    # create_contextual_slurm_submission_script(thisSlurmJobInfo)

    # Check if this is the appropriate host to submit the SLURM job on.
    # Note: GEMS hosts cannot currently be daisy-chained.
    if is_GEMS_instance_for_SLURM_submission(
        requested_ctx=thisSlurmJobInfo.incoming_dict["context"]
    ):
        # pdb.set_trace()
        # Necessarily, we must wait until the correct instance:
        create_contextual_slurm_submission_script(thisSlurmJobInfo)

        response = slurm_submit(thisSlurmJobInfo)
    else:
        log.debug("This is not the correct host to submit to.")
        # Otherwise, we need to seek the correct host to submit to.
        p = Process(
            target=seek_correct_host,
            args=(jsonObjectString, thisSlurmJobInfo.incoming_dict["context"]),
            # daemon=True,
        )
        p.start()
        # seek_correct_host(jsonObjectString, thisSlurmJobInfo.incoming_dict["context"])

        # TODO: Append this to actual GEMS response.
        response = {
            "notices": [
                "Attempting to find correct host for SLURM submission.  Check back later."
            ]
        }

    return response
