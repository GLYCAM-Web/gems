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

##  Prepare a pdb for use with Amber.
#   @param thisTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called.\n")
    log.debug("requestDict: \n" + str(json.dumps(thisTransaction.request_dict, indent=2, sort_keys=False)))
    
    ### Grab the pdb input.
    try:
        uploadFileName = getInput(thisTransaction)
        log.debug("~~~uploadFileName: " + uploadFileName)
    except Exception as error:
        log.error("There was a problem finding the uploadFileName in the transaction.")
        raise error
    else:

        try:
            ### Some projects will already have been created. 
            if thisTransaction.response_dict == None: 
                gemsProject = startPdbGemsProject(thisTransaction)
            elif 'gems_project' not in thisTransaction.response_dict.keys():
                gemsProject = startPdbGemsProject(thisTransaction)

        except Exception as error:
            log.error("There was a problem starting a pdb gemsProject.")
            raise error
        else:

            ###build the path to the uploaded pdb file.
            # outputDir = getOutputDir(thisTransaction)
            # frontendProject = thisTransaction.request_dict['project']
            # uploadFileName = getUploadsDestinationDir(frontendProject, outputDir)
            log.debug("completed uploadFileName: " + uploadFileName)
            ### generate the processed pdb's content
            try:
                pdbFile = generatePdbOutput(thisTransaction)
                log.debug("pdbFile output: " + str(pdbFile))
            except Exception as error:
                log.error("There was a problem generating the PDB output.")
            else:

                ### Write the content to file
                try:
                    writePdbOutput(thisTransaction, pdbFile)
                except Exception as error:
                    log.error("There was a problem writing the pdb output.")
                else:
                    ##Remove gemsProject if user agent is not website.
                    cleanGemsProject(thisTransaction) 

##  Pass in an uploadFileName and get a new, preprocessed pdbFile object, 
#       ready to be written to file.
#   @param uploadFileName
def generatePdbOutput(thisTransaction):
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
        log.debug("aminoLibs: " + str(aminoLibs))
        prepFile = getDefaultPrepFile(gemsHome)
        log.debug("prepFile: " + str(prepFile))
        glycamLibs = gmml.string_vector()
        log.debug("glycamLibs: " + str(glycamLibs))
        otherLibs = gmml.string_vector()
        log.debug("otherLibs: " + str(otherLibs))
        preprocessor = gmml.PdbPreprocessor()
        log.debug("preprocessor: " + str(preprocessor))

        try:
            ### Get the fileName from the transaction.
            gemsProject = thisTransaction.response_dict['gems_project']
            uploadFileName = gemsProject['upload_file_name']
            #PDB file object:
            log.debug("uploadFileName: " + uploadFileName)
            pdbFile = gmml.PdbFile(uploadFileName)
            log.debug("pdbFile: " + str(pdbFile))
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file.")
            raise error
        else:
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

    ### Grab the inputs from the entity
    if 'inputs' in thisTransaction.request_dict['entity'].keys():
        inputs = thisTransaction.request_dict['entity']['inputs']

        uploadFileName = ""
        ### Get the frontend project
        frontendProject = thisTransaction.request_dict['project']
        for element in inputs:
            log.debug("element: " + str(element))

            ### Check for a pdb file or a pdb ID. 
            if "pdb_file_name" in element.keys():
                log.debug("looking for the attached pdb file.")
                uploadFileName = getUploadFileName(frontendProject)

                return uploadFileName


            elif "pdb_ID" in element.keys():
                ### Look for a pdb ID to sideload.
                log.debug("Side-loading pdb from rcsb.org.")
                pdbID = element['pdb_ID']
                uploadDir = frontendProject['upload_path']
                log.debug("uploadDir: " + uploadDir)
                try:
                    uploadFileName = sideloadPdbFromRcsb(pdbID, uploadDir)
                except Exception as error:
                    log.error("There was a problem sideloading the pdb from the RCSB.")
                    raise error
                else:
                    log.debug("returning uploadFileName: " + uploadFileName)
                    return uploadFileName
            else:
                log.debug("element.keys(): " + str(element.keys()))

        if uploadFileName == "":
            raise AttributeError("Either pdb_file_name or pdb_ID must be present in the request's inputs.")
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

def makeRequest(url):
    log.info("makeRequest() was called. url: " + url)
    try:
        with urllib.request.urlopen(url) as response:
            contentBytes = response.read()
            return contentBytes
    except Exception as error:
        raise error

def getContentBytes(pdbID):
    log.info("getContentBytes() was called. \n")
    try:
        rcsbURL = "https://files.rcsb.org/download/" + pdbID + ".pdb1"
        contentBytes = makeRequest(rcsbURL)
        return contentBytes
    except Exception as error:
        ## Check if the 1 at the end is the issue.
        try:
            rcsbURL = "https://files.rcsb.org/download/" + pdbID + ".pdb"
            log.debug("Trying again with url: " + rcsbURL)
            with urllib.request.urlopen(rcsbURL) as response:
                contentBytes = response.read()
                return contentBytes
        except Exception as error:
            log.error("There was a problem requesting this pdb from RCSB.org.")
            raise error


##Returns the filename of a pdb file that is written to the dir you offer.
#   Creates the dir if it doesn't exist.
#   @param pdbID String to be used for the RCSB search.
#   @param uploadDir Destination path for the sideloaded pdb file.
def sideloadPdbFromRcsb(pdbID, uploadDir):
    log.info("sideloadPdbFromRcsb() was called.\n")

    ##Sideload pdb from rcsb.org
    pdbID = pdbID.upper()
    log.debug("pdbID: " + pdbID)
    try:
        contentBytes =  getContentBytes(pdbID)
    except Exception as error:
        log.error("There was a problem getting the content from the RCSB.")
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

## Only gets the file name. Not the path.
#   @aparam project
def getUploadFileName(project):
    log.info("getUploadFileName() was called.\n")
    
    uploadFileName = ""
    if "uploaded_file_name" in project.keys():
        uploadFileName = project['uploaded_file_name']
        log.debug("uploadFileName: " + uploadFileName)
        return uploadFileName
    else:
        log.error("No uploaded_file_name found in project.")
        raise AttributeError("uploadFileName")

    

##Starts the project, and updates the transaction.
def startPdbGemsProject(thisTransaction):
    log.info("startPdbGemsProject() was called.\n")
    try:
        ##Start a gemsProject        
        gemsProject = startProject(thisTransaction)
        return gemsProject
    except Exception as error:
        log.error("There was a problem starting the gemsProject.")
        raise error
        
    
