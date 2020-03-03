import os, sys, importlib.util
import pathlib
import urllib.request
import gemsModules
import gmml
import traceback

from collections import defaultdict
from collections import OrderedDict

from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.DEBUG

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

##TODO: Refactor for better encapsulation.
##TODO: Redo error handling.
##  Prepare a pdb for use with Amber.
#   @param thisTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called.\n")

    requestDict = thisTransaction.request_dict
    entity = getEntityType(thisTransaction)
    log.debug("requestDict: \n" + str(json.dumps(requestDict, indent=2, sort_keys=False)))
    gemsHome = getGemsHome()
    log.debug("gemsHome: " + gemsHome)
    try:
        uploadFileName = getUploadedFileNameFromTransaction(thisTransaction)
        log.debug("uploadFileName: " + uploadFileName)
    except Exception as error:
        log.error("There was a problem finding the uploadFileName in the transaction.")
        log.error("Error type: " + str(type(error)))
        log.errror(traceback.format_exc())
        appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        return
    ##TODO: find a better way to verify that a file is a pdb file, as some may
    ##  legitimately not have the .pdb extension.
    if not hasPdbExtension(uploadFileName):
        noticeBrief = "For now, pdb files must have the .pdb extension. May change later."
        log.error(noticeBrief)
        ##Transaction, noticeBrief, blockID
        appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        return
    else:
        log.debug("We have a file with a .pdb extension. Checking for a gemsProject.")
        ##Projects in which pdb preprocessing is jsut a step will already
        ##  have been created.
        if 'gems_project' not in thisTransaction.response_dict.keys():
            gemsProject =startPdbGemsProject(thisTransaction, uploadFileName)

        ##TODO: Check if user has provided optional prepFile and libraries.
        ##TODO: Error handling needed here.
        aminoLibs = getDefaultAminoLibs(gemsHome)
        glycamLibs = gmml.string_vector()
        otherLibs = gmml.string_vector()
        prepFile = getDefaultPrepFile(gemsHome)

        #PDB file object:
        pdbFile = gmml.PdbFile(uploadFileName)

        preprocessor = gmml.PdbPreprocessor()
        preprocessor.Preprocess(pdbFile, aminoLibs, glycamLibs, otherLibs, prepFile)
        preprocessor.ApplyPreprocessingWithTheGivenModelNumber(pdbFile, aminoLibs, glycamLibs, prepFile)

        ##Doesn't appear to be used. Do we need this for something?
        seqMap = pdbFile.GetSequenceNumberMapping()

        try:
            ##Give the output file the same path as the uploaded file, but replace the name.
            outputDir = gemsProject.output_dir
            log.debug("outputDir: " + outputDir)
            writePdb(pdbFile, outputDir)
        except IOError as error:
            log.error("Failed to write the pdb. Make sure the outputDir exists.")
        except Exception as error:
            noticeBrief = "There was an error writing the pdb file."
            log.error(noticeBrief)
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
            appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        else:
            try:
                buildPdbResponse(thisTransaction)
            except AttributeError as error:
                log.error("There was a problem building the pdbResponse.")
                log.error(traceback.format_exc())
                appendCommonParserNotice(thisTransaction, 'InvalidInput' )
            else:
                ##Remove gemsProject if user agent is not website.
                cleanGemsProject(thisTransaction)


##  Simple. Maybe too simple. Pass a string, if it contains .pdb, returns true. Else false.
#   @param filename as a string
def hasPdbExtension(filename : str):
    log.info("hasPdbExtension was called().\n")
    if ".pdb" in filename:
        return True
    else:
        return False

##  Looks for a project in the transaction,
#       checks for either a pdb file or pdbID.
#   @param thisTransaction
def getUploadedFileNameFromTransaction(thisTransaction : Transaction):
    log.info("getUploadedFileNameFromTransaction() was called.\n")
    if 'inputs' in thisTransaction.request_dict['entity'].keys():
        log.debug("found inputs")
        inputs = thisTransaction.request_dict['entity']['inputs']
        uploadFileName = ""
        project = thisTransaction.request_dict['project']
        for element in inputs:
            log.debug("element: " + str(element))
            ##Only sideload if uploadFileName is not ""
            if "pdb_file_name" in element.keys():
                log.debug("looking for the attached pdb file.")
                uploadFileName = getUploadFileName(project)
            elif uploadFileName == "" and "pdb_ID" in element.keys():
                log.debug("Side-loading pdb from rcsb.org.")
                pdbID = element['pdb_ID']
                uploadDir = project['upload_path']
                uploadFileName = sideloadPdbFromRcsb(pdbID, uploadDir)
            log.debug("returning uploadFileName: " + uploadFileName)
            return uploadFileName
    else:

        log.error("No inputs found in request.")
        raise AttributeError




##  Write the pdb file to the outputDir
#   @param pdbFile as created by gmml.PdbFile()
#   @param outputDir destination for pdb file
def writePdb(pdbFile, outputDir):
    log.info("writePdb() was called.\n")
    if os.path.exists(outputDir):
        log.debug("Writing the preprocessed pdb to 'updated_pdb.pdb'")
        destinationFile = 'updated_pdb.pdb'
        updatedPdbFileName = outputDir + destinationFile
        log.debug("updatedPdbFileName: " + updatedPdbFileName)
        pdbFile.WriteWithTheGivenModelNumber(updatedPdbFileName)
    else:
        raise IOError

## Adds a pdb response to responses. Transaction should have a gems project already.
##  @param thisTransaction The transaction object that needs a response appended to it.
def buildPdbResponse(thisTransaction : Transaction):
    log.info("buildPdbResponse() was called.\n")
    pUUID = getProjectpUUID(thisTransaction)
    if pUUID is not None:
        downloadUrl = getDownloadUrl(pUUID, "pdb")
        thisTransaction.response_dict['responses'].append({
            "PreprocessPdbForAmber" : {
                "payload" : pUUID,
                "downloadUrl" : downloadUrl
            }
        })
    else:
        raise AttributeError


##Returns the filename of a pdb file that is written to the dir you offer.
#   Creates the dir if it doesn't exist.
#   @param pdbID String to be used for the RCSB search.
#   @param uploadDir Destination path for the sideloaded pdb file.
def sideloadPdbFromRcsb(pdbID, uploadDir):
    log.info("sideloadPdbFromRcsb() was called.\n")

    ##Sideload pdb from rcsb.org
    pdbID = pdbID.upper()
    rcsbURL = "https://files.rcsb.org/download/" + pdbID + ".pdb1"
    log.debug("rcsbURL: " + rcsbURL)
    with urllib.request.urlopen(rcsbURL) as response:
        contentBytes = response.read()

    contentString = str(contentBytes, 'utf-8')
    log.debug("Response content object type: " + str(type(contentString)))
    #log.debug("Response content: \n" + str(contentString))
    ##Get the uploads dir
    log.debug("uploadDir: " + uploadDir)
    if not os.path.exists(uploadDir):
        pathlib.Path(uploadDir).mkdir(parents=True, exist_ok=True)

    uploadFileName = uploadDir  + pdbID + ".pdb"

    log.debug("uploadFileName: " + uploadFileName)
    ##Save the string to file in the uploads dir.
    with open(uploadFileName, "w") as uploadFile:
        uploadFile.write(contentString)

    log.debug("Finished side-loading pdb from rcsb.org.")
    return uploadFileName


##Amino libs
def getDefaultAminoLibs(gemsHome):
    log.info("getDefaultAminoLibs() was called.\n")
    amino_libs = gmml.string_vector()
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib")

    return amino_libs

##Prep file
def getDefaultPrepFile(gemsHome):
    log.info("getDefaultPrepFile() was called.\n")
    prepFile = gmml.string_vector()
    prepFile.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep")
    return prepFile


def getUploadFileName(project):
    log.info("getUploadFileName() was called.\n")
    ##Get the file name, combine path and file for full name.
    uploadFileName = ""
    if "uploaded_file_name" in project.keys():
        uploadFileName = project['uploaded_file_name']
        log.debug("uploadFileName: " + uploadFileName)
    else:
        log.error("No uploaded_file_name found in project.")


    if os.path.exists(uploadFileName):
        log.debug("uploadFile found.")
    else:
        log.error("uploadFile not found.")
        ##TODO: return a useful error here, invalid input.

    return uploadFileName

##Starts the project, and updates the transaction.
def startPdbGemsProject(thisTransaction, uploadFileName):
    log.info("startPdbGemsProject() was called.\n")
    ##Start a gemsProject
    if os.path.exists(uploadFileName):
        log.debug("Found the upload file")
        if uploadFileName.endswith(".pdb"):
            log.debug("File extension agrees this is a pdb file.")
            gemsProject = startProject(thisTransaction)
            return gemsProject
        else:
            log.error("File extension is not '.pdb' not sure what to do.")
            ##TODO: Add logic to validate pdb file type if no extension exists.
    else:
        log.error("Upload file could not be found.")
