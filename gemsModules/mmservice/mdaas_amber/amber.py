import json

from gemsModules.batchcompute.slurm.receive import receive as slurm_receive
from gemsModules.mmservice.mdaas_amber import mdaas_io

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# TODO: New-style gems Module for mdaas_amber
def manageIncomingString(jsonObjectString: str):
    input_json_dict = json.loads(jsonObjectString)
    log.debug("amber.py input_json_dict is : " + str(input_json_dict))

    try:
        amber_job = mdaas_io.amberProject(**input_json_dict)
    except:
        log.error("Could not get amber_job to work correctly.")
        raise ValueError("MDaaS had trouble getting the amber job to run.")

    outgoing_json_str = json.dumps(
        {
            "partition": "amber",
            "user": "webdev",
            "name": amber_job.submissionName,
            "workingDirectory": amber_job.simulationWorkingDirectory,
            "sbatchArgument": amber_job.simulationControlScriptPath,
        }
    )

    log.debug("amber.py: amber_job.submissionName is: " + outgoing_json_str)
    # TODO: This receive isn't quite a proper Entity-module, but eventually, we should be able
    # to decouple this call by delegating a submission to the batchcompute/slurm gemsModule like
    # any other GEMSrequest.
    slurm_receive(outgoing_json_str)
