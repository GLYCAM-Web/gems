from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

from gemsModules.mmservice.mdaas_amber import mdaas_io 


def manageIncomingString(jsonObjectString: str):
    import json

    log.debug("amber.py jsonObjectString is : " + jsonObjectString)
    input_json_dict = json.loads(jsonObjectString)
    log.debug("amber.py input_json_dict is : " + str(input_json_dict))

    try : 
        amber_job = mdaas_io.amberProject(**input_json_dict)
        amber_job.initialize()
        amber_job.copy_protocol_files()
    except:
        log.error("Could not get amber_job to work correctly.")
        raise ValueError ("MDaaS had trouble getting the amber job to run.")

    from gemsModules.deprecated.batchcompute import batchcompute
    outgoing_json_dict = {}
    outgoing_json_dict["partition"] = "amber"
    outgoing_json_dict["user"] = "webdev"
    outgoing_json_dict["name"] = amber_job.submissionName 
    outgoing_json_dict["workingDirectory"] = amber_job.simulationWorkingDirectory
    outgoing_json_dict["sbatchArgument"] = amber_job.simulationControlScriptPath

    batchcompute.batch_compute_delegation(outgoing_json_dict)

