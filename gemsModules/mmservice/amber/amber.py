import os, sys
from gemsModules.common.loggingConfig import *
from . import conf
from . import jsoninterface as amberio

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def manageIncomingString(jsonObjectString: str):
    import json

    log.debug("amber.py jsonObjectString is : " + jsonObjectString)
    input_json_dict = json.loads(jsonObjectString)
    log.debug("amber.py input_json_dict is : " + str(input_json_dict))

    try : 
        amber_job = amberio.amberProject(**input_json_dict)
        amber_job.initialize()
        amber_job.copy_protocol_files()
    except:
        log.error("Could not get amber_job to work correctly.")
        raise

    from gemsModules.batchcompute import batchcompute
    outgoing_json_dict = {}
    outgoing_json_dict["partition"] = "amber"
    outgoing_json_dict["user"] = "webdev"
    outgoing_json_dict["name"] = amber_job.submissionName 
    outgoing_json_dict["workingDirectory"] = amber_job.simulationWorkingDirectory
    outgoing_json_dict["sbatchArgument"] = amber_job.simulationControlScriptPath

    batchcompute.batch_compute_delegation(outgoing_json_dict)

def main():
    import importlib.util, os, sys
    if importlib.util.find_spec("gemsModules") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../")
        if importlib.util.find_spec("common") is None:
            print("I cannot find the Common Servicer.  No clue what to do. Exiting")
            sys.exit(1)
        else:
            from common import utils
    else:
        from gemsModules.common import utils
    jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
    try:
        responseObject=manageIncomingString(jsonObjectString)
    except Exception as error:
        print("\nThe mmservice.amber module captured an error.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())
        ##TODO: see about exploring this error and returning more info. Temp solution for now.
        responseObject = {
            'response' : {
                'type' : 'UnknownError',
                'notice' : {
                    'code' : '500',
                    'brief' : 'unknownError',
                    'blockID' : 'unknown',
                    'message' : 'Not sure what went wrong. Error captured by the mmservice.amber gemsModule.'
                }
            }
        }
        responseObjectString = str(responseObject)


    print("\nmmservice.amber is returning this: \n" +  responseObjectString)


if __name__ == "__main__":
    main()

