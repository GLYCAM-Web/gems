#!/usr/bin/env python3
import socket
from multiprocessing import Process

from gemsModules.deprecated.common.services import *
from gemsModules.deprecated.common.transaction import *  # might need whole file...
from gemsModules.deprecated.batchcompute.slurm.dataio import *

# TODO: Real batchcompute module
from gemsModules.deprecated.batchcompute.slurm.receive import manageIncomingString

from gemsModules.networkconnections.grpc import (
    is_GEMS_instance_for_SLURM_submission,
)

from .tasks.run_submission import execute as run_submission
from .tasks.generate_submission_script import execute as generate_submission_script
from .tasks.seek_correct_host import execute as seek_correct_host


from gemsModules.logging.logger import new_concurrent_logger


log = new_concurrent_logger(__name__)


def receive(jsonObjectString):
    """batchcompute.slurm Entity reception module.

    This is more or less an intermediate on the way to a proper new-style entity.

    It does not have a complete API.
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

    # Check if this is the appropriate host to submit the SLURM job on.
    # Note: GEMS hosts cannot currently be daisy-chained.
    if is_GEMS_instance_for_SLURM_submission(
        requested_ctx=thisSlurmJobInfo.incoming_dict["context"]
    ):
        log.debug("This is the correct host to submit to.")
        log.debug("thisSlurmJobInfo: %s", thisSlurmJobInfo)

        generate_submission_script(thisSlurmJobInfo)

        response = run_submission(thisSlurmJobInfo)
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
