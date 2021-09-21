from gemsModules.structureFile.amber import io as amberIO
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  Evaluate a pdb for use with Amber.
#   @param receivedTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def evaluatePdb(receivedTransaction : amberIO.Transaction):
    log.info("evaluatePdb() was called. Still in development!!!")

    ## start a project here.
    ## TODO!!!!!!!!!!!!!!!
    ## Add sideloading back in. See amber/logic.py sideloadPdbFromRcsb()
    ## evaluatePdb service will require:
    ##  uploaded_file_name
    ## 

    log.debug("\n\nreceivedTransaction.response_dict: " + str(receivedTransaction.response_dict))
    uploadedFileName = receivedTransaction.response_dict['project']['uploaded_file_name']
    log.debug("uploadedFileName: " + uploadedFileName)

    projectDir = receivedTransaction.response_dict['project']['project_dir']
    uploadFile = projectDir + "/uploads/" + uploadedFileName
    log.debug("uploadFile: " + uploadFile)


    ### generate the processed pdb's content
    try:
        output = amberIO.EvaluationOutput(uploadFile)
        outputDict = output.dict(by_alias=True)
        log.debug("outputDict: \n\n")
        prettyPrint(outputDict)
    except Exception as error:
        log.error("There was a problem evaluating the uploaded file: " + str(error))
        log.error(traceback.format_exc())
        raise error

    ## Add the output to the response.
    try:
        inputs = []
        inputs.append(uploadedFileName)
        outputs = []
        outputs.append(outputDict)
        log.debug("Attempting to build the response.")
        log.debug("inputs: " + repr(inputs))
        log.debug("outputs: " + repr(outputs))
        responseObj = amberIO.ServiceResponse("Evaluate", inputs=inputs, outputs=outputs)
    except Exception as error:
        log.error("There was a problem building an evaluation response: " + str(error))
        log.error(traceback.format_exc())
        raise error

    updateResponse(receivedTransaction, responseObj.dict(by_alias=True))
    try:
        log.debug("About to build the outgoing string.")
        receivedTransaction.build_outgoing_string()
        
    except Exception as error:
        log.error("There was a problem building the outgoing string: " + str(error))
        log.error(traceback.format_exc())
        raise error