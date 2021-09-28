from gemsModules.structureFile.amber import io as amberIO
from gemsModules.common.loggingConfig import *
from gemsModules.common.logic import prettyPrint, updateResponse
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  Evaluate a pdb for use with Amber.
#   @param receivedTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def evaluatePdb(receivedTransaction : amberIO.PdbTransaction):
    log.info("evaluatePdb() was called. Still in development!!!")

    ## Grab the input
    try:
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

    # Ensure a project exists
    try:
        if receivedTransaction.transaction_out.project is None:
            log.debug("Starting a new project for transaction_out.")
            receivedTransaction.transaction_out.project = gemsModules.project.io.PdbProject()
        else:
            log.debug("receivedTransaction.transaction_out.project: " + str(receivedTransaction.transaction_out.project))

        pdbProject = receivedTransaction.transaction_out.project 
        pdbProject.setFilesystemPath()
        pdbProject.loadVersionsFileInfo()
        pdbProject.setUploadFile(uploadFile)
        log.debug("pdbProject: " )
        prettyPrint(pdbProject.__dict__)
    except Exception as error:
        log.error("There was a problem starting a PdbProject: " + str(error))
        log.error(traceback.format_exc())
        raise error



    ### Generate the processed pdb's content
    try:
        evaluator = amberIO.Evaluator()
        output = evaluator.doEvaluation(uploadFile)
        log.debug("output obj type: " + str(type(output)))
        outputDict = output.__dict__
        log.debug("outputDict: " + str(outputDict))

    except Exception as error:
        log.error("There was a problem evaluating the uploaded file: " + str(error))
        log.error(traceback.format_exc())
        raise error

    ## Add the output to the response.
    try:
        outputs = []
        outputs.append(outputDict)
        log.debug("Attempting to build the response.")
        responseObj = amberIO.StructureFileResponse("Evaluate", inputs=inputs, outputs=outputs)
        log.debug("responseObj type: " + str(type(responseObj)))
        log.debug("responseObj: " + repr(responseObj))
        receivedTransaction.transaction_out.entity.outputs = responseObj
    except Exception as error:
        log.error("There was a problem building an evaluation response: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        log.debug("About to build the outgoing string.")
        receivedTransaction.build_outgoing_string()
        
    except Exception as error:
        log.error("There was a problem building the outgoing string: " + str(error))
        log.error(traceback.format_exc())
        raise error