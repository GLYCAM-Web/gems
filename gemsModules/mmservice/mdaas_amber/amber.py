import json

from gemsModules.batchcompute.slurm.receive import receive as slurm_receive
from gemsModules.mmservice.mdaas_amber import mdaas_io

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# TODO: New-style gems Module for mdaas_amber so we can append notice from no instance config
def manageIncomingString(jsonObjectString: str):
    """This is the main function for the mmservice/amber module.

    It creates a job dictionary which can be used to submit a job to the batchcompute/slurm Entity.

    > Eventually, it may do more to request an Amber MD job specifically from batchcompute/SLURM,
    > however GEMS' Instance Configuration currently solves this based on the given context.

    - batchcompute/slurm ensures the job is submitted and executed on the correct host under the correct context.
    """
    input_json_dict = json.loads(jsonObjectString)
    log.debug("amber.py input_json_dict is : " + str(input_json_dict))

    try:
        # This is technically when the project directory first gets created.
        amber_job = mdaas_io.amberProject(**input_json_dict)
    except:
        log.warning("Could not get mdaas_amber reception to work correctly.")

    # This is to become the SLURM job info dict used later for slurm submission.
    outgoing_json_str = json.dumps(
        {
            "pUUID": amber_job.jobID,
            "partition": "amber",  # TODO: Probably invalid in most cases. The IC will handle this later.
            "user": "webdev",  # TODO: We could remove this and obtain it on demand. This is coupled to our DevEnv/Swarm.
            "name": amber_job.submissionName,
            "workingDirectory": amber_job.simulationWorkingDirectory,
            "sbatchArgument": amber_job.simulationControlScriptPath,
            # TODO: THis all needs to be made proper newstyle gemsModules...:(
            "context": input_json_dict["context"],
        }
    )
    log.debug(
        "amber_job to be submitted over SLURM: "
        + json.dumps(outgoing_json_str, indent=2)
    )

    # TODO: Delegate this request instead of calling it directly.
    return slurm_receive(outgoing_json_str)
