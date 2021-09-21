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

    try:
        #
        inputs = receivedTransaction.request_dict['entity']['inputs']
        log.debug("inputs.keys(): " + str(inputs.keys()))
        if 'pdb_file_name' in inputs.keys():
            uploadFile = inputs['pdb_file_name']
        elif 'pdb_ID' in inputs.keys():
            uploadFile = sideloadPdbFromRcsb(inputs['pdb_ID'])
    except Exception as error:
        log.error("There was a problem finding the input in the evaluate PDB request: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        if receivedTransaction.transaction_out.project is None:
            log.debug("Starting a new project for transaction_out.")
            receivedTransaction.transaction_out.project = gemsModules.project.io.PdbProject()
        else:
            log.debug("receivedTransaction.transaction_out.project: " + str(receivedTransaction.transaction_out.project))

        pdbProject = receivedTransaction.transaction_out.project 
        log.debug("pdbProject: " + repr(pdbProject))
        pdbProject.setFilesystemPath()
        pdbProject.loadVersionsFileInfo()
        pdbProject.setUploadFile(uploadFile)
        log.debug("pdbProject: " + repr(pdbProject))

    except Exception as error:
        log.error("There was a problem starting a PdbProject: " + str(error))
        log.error(traceback.format_exc())
        raise error

    # log.debug("\n\nreceivedTransaction.response_dict: " + str(receivedTransaction.response_dict))
    # ##TODO:
    # ## This is now an input
    # uploadedFileName = receivedTransaction.response_dict['project']['uploaded_file_name']
    # log.debug("uploadedFileName: " + uploadedFileName)

    # projectDir = receivedTransaction.response_dict['project']['project_dir']
    # uploadFile = projectDir + "/uploads/" + uploadedFileName
    # log.debug("uploadFile: " + uploadFile)


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