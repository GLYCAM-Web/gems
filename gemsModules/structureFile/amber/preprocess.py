from gemsModules.structureFile.amber import io as amberIO
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def preprocessPdbForAmber(pdbTransaction : amberIO.PdbTransaction):
    log.info("preprocessPdbForAmber was called. Still in Development!!!!!!!!")
    ## Find the input
    try:
        uploadFile = pdbTransaction.getUploadFileFromPdbTransaction()
        log.debug("uploadFile: " + uploadFile)
        customProjectDir = pdbTransaction.getCustomProjectDirFromPdbTransaction()
        log.debug("customProjectDir: " + customProjectDir)
    except Exception as error:
        log.error("There was a problem getting the upload file from the PdbTransaction: " + str(error))
        log.error(traceback.format_exc())
        raise error

    # Ensure a project exists
    try:
        if pdbTransaction.transaction_out.project is None:
            log.debug("Starting a new project for transaction_out.")
            pdbTransaction.transaction_out.project = gemsModules.project.io.PdbProject()
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
        pdbProject.requested_service = "PreprocessPdbForAmber"
        pdbProject.createDirectories()
        pdbProject.writeInitialLogs()
        # Generate the complete incoming JSON object, including all defaults
        incomingString = pdbTransaction.incoming_string
        incomingRequest = pdbTransaction.transaction_in.json(indent=2)
        log.debug("Writing log files.")
        common.logic.writeStringToFile(incomingString, os.path.join(pdbProject.logs_dir, "request-raw.json") )
        common.logic.writeStringToFile(incomingRequest, os.path.join(pdbProject.logs_dir, "request-initialized.json") )
        pdbProject.setHostUrlBasePath()
        pdbProject.setDownloadUrlPath()
        log.debug("Just initialized the outgoing project.  The transaction_out is :   " )
        log.debug(pdbTransaction.transaction_out.json(indent=2))
    except Exception as error:
        log.error("There was a problem starting a PdbProject: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        mngr = amberIO.PreprocessorManager()
        mngr.preprocessPdbForAmber(uploadFile, pdbProject.project_dir)
    except Exception as error:
        log.error("There was a problem preprocessing the pdb for amber: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        pdbTransaction.build_outgoing_string()
        outgoingResponse = pdbTransaction.transaction_out.json(indent=2)
        common.logic.writeStringToFile(outgoingResponse, os.path.join(pdbProject.project_dir, "response.json"))
    except Exception as error:
        log.error("There was a problem generating the output after preprocessing the pdb: " + str(error))
        log.error(traceback.format_exc())
        raise error

    return pdbTransaction


