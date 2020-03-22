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

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##TODO: Refactor for better encapsulation.
##TODO: Redo error handling.
##  Prepare a pdb for use with Amber.
#   @param thisTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called.\n")

    requestDict = thisTransaction.request_dict
    entity = getEntityType(thisTransaction)
    log.debug("requestDict: \n" + str(json.dumps(requestDict, indent=2, sort_keys=False)))
    
    ### Grab the pdb input.
    try:
        uploadFileName = getInput(thisTransaction)
        log.debug("uploadFileName: " + uploadFileName)
    except Exception as error:
        log.error("There was a problem finding the uploadFileName in the transaction.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        return
    
    ### Check for a .pdb file extension.
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
        if thisTransaction.response_dict == None: 
            gemsProject = startPdbGemsProject(thisTransaction, uploadFileName)
        elif 'gems_project' not in thisTransaction.response_dict.keys():
            gemsProject = startPdbGemsProject(thisTransaction, uploadFileName)
        
        try:
            pdbFile = generatePdbOutput(uploadFileName)
        except Exception as error:
            log.error("There was a problem generating the PDB output.")
        else:
        
            try:
                ### Write the output
                writePdbOutput(thisTransaction, pdbFile)
            except Exception as error:
                log.error("There was a problem writing the pdb output.")
            else:
                ##Remove gemsProject if user agent is not website.
                cleanGemsProject(thisTransaction) 

##  Pass in an uploadFileName and get a new, preprocessed pdbFile object, 
#       ready to be written to file.
#   @param uploadFileName
def generatePdbOutput(uploadFileName):
    log.info("generatePdbOutput() was called.\n")
    try:
        gemsHome = getGemsHome()
        log.debug("gemsHome: " + gemsHome)
    except Exception as error:
        log.error("There was a problem getting GEMSHOME.")
        raise error
    else:
        ##TODO: Check if user has provided optional prepFile and libraries.
        aminoLibs = getDefaultAminoLibs(gemsHome)
        prepFile = getDefaultPrepFile(gemsHome)
        glycamLibs = gmml.string_vector()
        otherLibs = gmml.string_vector()
        preprocessor = gmml.PdbPreprocessor()

        #PDB file object:
        pdbFile = gmml.PdbFile(uploadFileName)

        try:
            ### Preprocess
            preprocessor.Preprocess(pdbFile, aminoLibs, glycamLibs, otherLibs, prepFile)
        except Exception as error:
            log.error("There was a problem preprocessing with gmml.")
            raise error
        else:
            try:
                ### Apply preprocessing
                preprocessor.ApplyPreprocessingWithTheGivenModelNumber(pdbFile, aminoLibs, glycamLibs, prepFile)
            except:
                log.error("There was a problem applying the preprocessing.")
                raise error
            else:
                ##Get the sequence mapping.
                try:
                    seqMap = pdbFile.GetSequenceNumberMapping()
                    log.debug("seqMap: " + str(seqMap))
                except Exception as error:
                    log.error("Therre was a problem getting the sequence mapping.")
                    raise error

def writePdbOutput(thisTransaction, pdbFile):
    log.info("writePdbOutput() was called.\n")
    ### Give the output file the same path as the uploaded file, but replace the name.
    try:
        outputDir = getOutputDir(thisTransaction)
        log.debug("outputDir: " + outputDir)  
    except Exception as error:
        log.error("There was a problem getting the output dir from the transaction.")
        raise error
    else:

        ### Write the file
        try:   
            writePdb(pdbFile, outputDir)
        except Exception as error:
            log.error("There was an error writing the pdb file.")
            raise error        
        else:

            ### Build a response
            try:
                responseConfig = buildPdbResponseConfig(thisTransaction)
                appendResponse(thisTransaction, responseConfig)
            except Exception as error:
                log.error("There was a problem building the pdbResponse.")
                raise error
                           


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
def getInput(thisTransaction : Transaction):
    log.info("getInput() was called.\n")
    if 'inputs' in thisTransaction.request_dict['entity'].keys():
        inputs = thisTransaction.request_dict['entity']['inputs']
        project = thisTransaction.request_dict['project']
        for element in inputs:
            log.debug("element: " + str(element))
            ##Only sideload if uploadFileName is not ""
            if "pdb_file_name" in element.keys():
                log.debug("looking for the attached pdb file.")
                uploadFileName = getUploadFileName(project)
                return uploadFileName
            else:
                ##Look for a pdb ID to sideload.
                log.debug("Side-loading pdb from rcsb.org.")
                pdbID = element['pdb_ID']
                uploadDir = project['upload_path']
                try:
                    uploadFileName = sideloadPdbFromRcsb(pdbID, uploadDir)
                except Exception as error:
                    log.error("There was a problem sideloading the pdb from the RCSB.")
                    raise error
                else:
                    log.debug("returning uploadFileName: " + uploadFileName)
                    return uploadFileName
    else:
        log.error("No inputs found in request.")
        raise AttributeError("inputs")




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

def buildPdbResponseConfig(thisTransaction : Transaction):
    log.info("buildPdbResponseConfig() was called.\n")
    gemsProject = thisTransaction.response_dict['gems_project']
    downloadUrl = getDownloadUrl(gemsProject['pUUID'], "pdb")
    config = {
        "entity" : "StructureFile",
        "respondingService" : "PreprocessPdbForAmber",
        "responses" : [
            {
                "project_status" : gemsProject['status'],
                'payload' : gemsProject['pUUID'],
                'downloadUrl' : downloadUrl
            }
        ]
    }
    return config


##Returns the filename of a pdb file that is written to the dir you offer.
#   Creates the dir if it doesn't exist.
#   @param pdbID String to be used for the RCSB search.
#   @param uploadDir Destination path for the sideloaded pdb file.
def sideloadPdbFromRcsb(pdbID, uploadDir):
    log.info("sideloadPdbFromRcsb() was called.\n")

    ##Sideload pdb from rcsb.org
    pdbID = pdbID.upper()
    log.debug("pdbID: " + pdbID)

    rcsbURL = "https://files.rcsb.org/download/" + pdbID + ".pdb1"
    log.debug("rcsbURL: " + rcsbURL)
    try:
        with urllib.request.urlopen(rcsbURL) as response:
            contentBytes = response.read()
    except Exception as error:
        log.error("There was a problem sideloading the requested pdb from RCSB.")
        raise error
    else:

        contentString = str(contentBytes, 'utf-8')
        log.debug("Response content object type: " + str(type(contentString)))
        #log.debug("Response content: \n" + str(contentString))
        ##Get the uploads dir
        log.debug("uploadDir: " + uploadDir)
        if not os.path.exists(uploadDir):
            pathlib.Path(uploadDir).mkdir(parents=True, exist_ok=True)

        uploadFileName = uploadDir  + pdbID + ".pdb"
        log.debug("uploadFileName: " + uploadFileName)
        try:
            ##Save the string to file in the uploads dir.
            with open(uploadFileName, "w") as uploadFile:
                uploadFile.write(contentString)
        except Exception as error:
            log.error("There was a problem writing the sideloaded content into the file.")
            raise error
        else:
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
