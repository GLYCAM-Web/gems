from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

from gemsModules.mmservice.mdaas_amber import mdaas_io


def manageIncomingString(jsonObjectString: str):
    import json

    log.debug("amber.py jsonObjectString is : " + jsonObjectString)
    input_json_dict = json.loads(jsonObjectString)
    log.debug("amber.py input_json_dict is : " + str(input_json_dict))

    try:
        amber_job = mdaas_io.amberProject(**input_json_dict)
    except:
        log.error("Could not get amber_job to work correctly.")
        raise ValueError("MDaaS had trouble getting the amber job to run.")

    from gemsModules.deprecated.batchcompute import batchcompute

    log.debug("amber.py: amber_job.submissionName is: " + amber_job.submissionName)
    outgoing_json_dict = {
        "partition": "amber",
        "user": "webdev",
        "name": amber_job.submissionName,
        "workingDirectory": amber_job.simulationWorkingDirectory,
        "sbatchArgument": amber_job.simulationControlScriptPath,
    }

    batchcompute.batch_compute_delegation(outgoing_json_dict)
    log.debug(
        "got past the batchcompute.batch_compute_delegation(outgoing_json_dict) stuff in amber.py"
    )
