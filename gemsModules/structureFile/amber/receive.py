import os, sys, importlib.util
import gemsModules
import gmml
import traceback

from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

##TODO: figure out how to stack receive calls to nested modules.
##  Moving on so it won't be a bottleneck
def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called.\n")
    ## Check the files, if not happy with the file type return error.
    requestDict = thisTransaction.request_dict
    entity = requestDict['entity']['type']
    log.debug("requestDict: " + str(requestDict))
    log.debug("entity: " + entity)
    gemsHome = getGemsHome()
    log.debug("gemsHome: " + gemsHome)

    ## project, here, is a frontend project, not gemsProject.
    if "project" in requestDict.keys():
        log.debug("found a project in the request.")
        project = requestDict['project']
        uploadFileName = getUploadFileName(project)

        ##TODO: find a better way to verify that a file is a pdb file, as some may
        ##  legitimately not have the .pdb extension.
        if ".pdb" not in uploadFileName:
            log.error("For now, pdb files must have the .pdb extension. May change later.")
            ##TODO: Add logic to return an invalid input error.
        else:
            log.debug("We have a file with a .pdb extension. Starting a gemsProject.")
            startGemsProject(thisTransaction, uploadFileName)
            gemsProject = thisTransaction.response_dict['gems_project']

            ##If no inputs provided, bail.
            if "inputs" in requestDict["entity"]:
                ##TODO: Check if user has provided optional prepFile and libraries.
                ##Using defaults for now.
                aminoLibs = getDefaultAminoLibs(gemsHome)
                glycamLibs = gmml.string_vector()
                otherLibs = gmml.string_vector()
                prepFile = getDefaultPrepFile(gemsHome)
                log.debug("aminoLibs: " + str(aminoLibs))
                log.debug("prepFile: " + str(prepFile))

                #PDB file object:
                pdbFile = gmml.PdbFile(uploadFileName)

                preprocessor = gmml.PdbPreprocessor()
                preprocessor.Preprocess(pdbFile, aminoLibs, glycamLibs, otherLibs, prepFile)
                preprocessor.ApplyPreprocessingWithTheGivenModelNumber(pdbFile, aminoLibs, glycamLibs, prepFile)
                #preprocessor.Print()

                seqMap = pdbFile.GetSequenceNumberMapping()
                log.debug("Writing the preprocessed pdb to 'updatedPdb.pdb'")
                try:
                    ##Give the output file the same path as the uploaded file, but replace the name.
                    outputDir = gemsProject['output_dir']
                    destinationFile = 'updated_pdb.txt'
                    updatedPdbFileName = outputDir + destinationFile
                    log.debug("updatedPdbFileName: " + updatedPdbFileName)
                    pdbFile.WriteWithTheGivenModelNumber(updatedPdbFileName)
                except Exception as error:
                    log.error("There was an error writing the pdb file.")
                    log.error("Error type: " + str(type(error)))
                    log.error(traceback.format_exc())
                    ##TODO return a useful error.
                else:
                    ##Build a response object for pdb responses
                    #log.debug("responseDict: " + str(thisTransaction.response_dict))
                    if "responses" not in thisTransaction.response_dict:
                        thisTransaction.response_dict['responses'] = []

                    thisTransaction.response_dict['responses'].append({
                        "PreprocessPdbForAmber" : {
                            "payload" : updatedPdbFileName
                        }
                    })

                    if 'gems_project' in thisTransaction.response_dict.keys():
                        if "website" == thisTransaction.response_dict['gems_project']['requesting_agent']:
                            log.debug("Returning response to website.")
                        else:
                            log.debug("Cleanup for api requests.")
                            del thisTransaction.response_dict['gems_project']

            else:
                log.error("Request must at least have a pdb_file_name in inputs section of the entity.")
                ##TODO:  return an invalid input error.


    else:
        log.warning("No project found in keys.")
        ##May be a request from the command line that does not use json api?


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
def startGemsProject(thisTransaction, uploadFileName):
    log.info("startGemsProject() was called.\n")
    ##Start a gemsProject
    if os.path.exists(uploadFileName):
        log.debug("Found the upload file")
        if uploadFileName.endswith(".pdb"):
            log.debug("File extension agrees this is a pdb file.")
            startProject(thisTransaction)
        else:
            log.error("File extension is not '.pdb' not sure what to do.")
            ##TODO: Add logic to validate pdb file type if no extension exists.
    else:
        log.error("Upload file could not be found.")
