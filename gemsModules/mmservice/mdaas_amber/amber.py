import json

from gemsModules.batchcompute.slurm.receive import receive as slurm_receive
from gemsModules.mmservice.mdaas_amber import mdaas_io

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# TODO: New-style gems Module for mdaas_amber so we can append notice from no instance config
def manageIncomingString(jsonObjectString: str):
    input_json_dict = json.loads(jsonObjectString)
    log.debug("amber.py input_json_dict is : " + str(input_json_dict))

    try:
        amber_job = mdaas_io.amberProject(**input_json_dict)
    except:
        log.warning("Could not get mdaas_amber reception to work correctly.")

    # This is to become the SLURM job info dict used later for slurm submission.
    outgoing_json_str = json.dumps(
        {
            "partition": "amber",  # TODO: Remove - not a valid partition, overwritten by instance config later.
            "user": "webdev",  # TODO: We could remove this as get it on demand.
            "name": amber_job.submissionName,
            "workingDirectory": amber_job.simulationWorkingDirectory,
            "sbatchArgument": amber_job.simulationControlScriptPath,
            # TODO: THis all needs to be made proper newstyle gemsModules...:(
            "context": input_json_dict["context"],
        }
    )

    log.debug("amber.py: amber_job " + outgoing_json_str)
    # TODO: This receive isn't quite a proper Entity-module, but eventually, we should be able
    # to decouple this call by delegating a submission to the batchcompute/slurm gemsModule like
    # any other GEMS JSON API Request. For now, amber is calling it directly, but eventually
    # delegator.redirector settings should have slurm_receive.
    # We need to use bin/slurmreceive here, basically.
    return slurm_receive(outgoing_json_str)
