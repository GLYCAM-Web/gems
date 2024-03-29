from gemsModules.deprecated.structureFile.amber import io as amberIO
from gemsModules.deprecated.common.loggingConfig import *
from gemsModules.deprecated.common.logic import prettyPrint, updateResponse
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)



##  Evaluate a pdb for use with Amber.
#   @param pdbTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def evaluatePdb(pdbTransaction : amberIO.PdbTransaction):
    log.info("evaluatePdb was called.")
    ##Inputs.
    try:
        uploadFile = pdbTransaction.getUploadFileFromPdbTransaction()
        log.debug("uploadFile: " + uploadFile)
        customProjectDir = pdbTransaction.getCustomProjectDirFromPdbTransaction()
    except Exception as error:
        log.error("There was a problem getting the upload file from the PdbTransaction: " + str(error))
        log.error(traceback.format_exc())
        raise error

    # Ensure a project exists
    ##  TODO: Move all instantiation logic into the __init__ for pdbProject.
    try:
        if pdbTransaction.transaction_out.project is None:
            log.debug("Starting a new project for transaction_out.")
            pdbTransaction.transaction_out.project = gemsModules.deprecated.project.io.PdbProject()
        else:
            log.debug("pdbTransaction.transaction_out.project: " + str(pdbTransaction.transaction_out.project))

        pdbProject = pdbTransaction.transaction_out.project 

        #######################################
        ##Derived field values need to be added
        

        ## Default project dir looks like /website/userdata/structurefile/pdb/outputs/<pUUID>
        if customProjectDir != "":
            pdbProject.project_dir = customProjectDir 
        else:
            ## give it the default project dir.
            defaultProjectDir = os.path.join(
                pdbProject.service_dir,
                'outputs',
                pdbProject.pUUID
            )
            pdbProject.project_dir = defaultProjectDir 

        pdbProject.setUploadFile(uploadFile)
        pdbProject.requested_service = "Evaluate"
        pdbProject.createDirectories()
        #########################################
        log.debug("pdbProject: " )
        prettyPrint(pdbProject.__dict__)
    except Exception as error:
        log.error("There was a problem starting a PdbProject: " + str(error))
        log.error(traceback.format_exc())
        raise error



    ### Generate the processed pdb's content
    try:
        log.debug("instantiating the mngr")
        mngr = amberIO.PreprocessorManager()
        output = mngr.doEvaluation(uploadFile)
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
        responseObj = amberIO.StructureFileResponse("Evaluate", inputs=pdbTransaction.request_dict['entity']['inputs'], outputs=outputs)
        log.debug("responseObj type: " + str(type(responseObj)))
        log.debug("responseObj: " + repr(responseObj))
        pdbTransaction.transaction_out.entity.outputs = responseObj
    except Exception as error:
        log.error("There was a problem building an evaluation response: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        log.debug("About to build the outgoing string.")
        pdbTransaction.build_outgoing_string()
        
    except Exception as error:
        log.error("There was a problem building the outgoing string: " + str(error))
        log.error(traceback.format_exc())
        raise error