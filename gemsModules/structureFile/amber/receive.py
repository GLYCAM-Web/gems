import os, sys, importlib.util
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

##TODO: figure out how to stack receive calls to nested modules.
##  Moving on so it won't be a bottleneck
def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called.\n")
    ## Check the files, if not happy with the file type return error.
    requestDict = thisTransaction.request_dict
    entity = requestDict['entity']['type']
    log.debug("requestDict: " + str(json.dumps(requestDict, indent=2, sort_keys=False)))
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
            noticeBrief = "For now, pdb files must have the .pdb extension. May change later."
            log.error(noticeBrief)
            ##Transaction, noticeBrief, blockID
            appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        else:
            log.debug("We have a file with a .pdb extension. Checking for a gemsProject.")
            ##Projects in which pdb preprocessing is jsut a step will already
            ##  have been created.
            if 'gems_project' not in thisTransaction.response_dict.keys():
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
                log.debug("Writing the preprocessed pdb to 'updated_pdb.pdb'")
                try:
                    ##Give the output file the same path as the uploaded file, but replace the name.
                    outputDir = gemsProject['output_dir']
                    destinationFile = 'updated_pdb.pdb'
                    updatedPdbFileName = outputDir + destinationFile
                    log.debug("updatedPdbFileName: " + updatedPdbFileName)
                    pdbFile.WriteWithTheGivenModelNumber(updatedPdbFileName)
                except Exception as error:
                    noticeBrief = "There was an error writing the pdb file."
                    log.error(noticeBrief)
                    log.error("Error type: " + str(type(error)))
                    log.error(traceback.format_exc())
                    appendCommonParserNotice(thisTransaction, 'InvalidInput' )
                else:
                    ##Build a response object for pdb responses
                    #log.debug("responseDict: " + str(thisTransaction.response_dict))
                    if "responses" not in thisTransaction.response_dict:
                        thisTransaction.response_dict['responses'] = []

                    ##Return the pUUID as the payload.
                    thisTransaction.response_dict['responses'].append({
                        "PreprocessPdbForAmber" : {
                            "payload" : gemsProject['pUUID']
                        }
                    })

                    if 'gems_project' in thisTransaction.response_dict.keys():
                        if "website" == thisTransaction.response_dict['gems_project']['requesting_agent']:
                            log.debug("Returning response to website.")
                        else:
                            log.debug("Cleanup for api requests.")
                            del thisTransaction.response_dict['gems_project']

            else:
                noticeBrief = "Request must have a pdb_file_name in inputs section of the entity."
                log.error(noticeBrief)
                appendCommonParserNotice(thisTransaction, 'JsonParseEror' )

    else:
        noticeBrief = "No project found in keys. Still developing command-line interface."
        log.error(noticeBrief)
        ##May be a request from the command line that does not use json api?
        ##TODO: Add logic to do this without the interface to the frontend.
        ##Transaction, noticeBrief, blockID
        appendCommonParserNotice(thisTransaction, 'InvalidInput' )

def getLikelySites(thisTransaction):
    log.info("getLikelySites() was called.\n")
    ##TODO: Check if user has provided optional prepFile and libraries.
    ##Using defaults for now.
    gemsHome = getGemsHome()
    aminoLibs = getDefaultAminoLibs(gemsHome)
    glycamLibs = gmml.string_vector()
    otherLibs = gmml.string_vector()
    prepFile = getDefaultPrepFile(gemsHome)
    log.debug("aminoLibs: " + str(aminoLibs))
    log.debug("prepFile: " + str(prepFile))

    project = thisTransaction.request_dict['project']

    uploadFileName = getUploadFileName(project)
    log.debug("uploadFileName: " + uploadFileName)
    #PDB file object:
    pdbFile = gmml.PdbFile(uploadFileName)

    preprocessor = gmml.PdbPreprocessor()
    preprocessor.Preprocess(pdbFile, aminoLibs, glycamLibs, otherLibs, prepFile)
    residueInfo = preprocessor.GetResidueInfoMap()
    log.debug("residueInfo:\n" + str(residueInfo))
    positionsDict = {}
    for key, value in residueInfo.items():
        log.debug("key: " + str(key))
        log.debug("value: " + str(value))
        chainId = value.GetResidueChainId()
        sequenceNumber = value.GetResidueSequenceNumber()
        residueName = value.GetResidueName()
        log.debug("chainId: " + str(chainId) + ", sequenceNumber: " + str(sequenceNumber) + ", residueName: " + str(residueName))
        if not positionsDict.get(chainId):
            positionsDict[chainId] = {}
        positionsDict[chainId][sequenceNumber] = residueName

    log.debug("positionsDict: " + str(positionsDict))
    for key in positionsDict.keys():
        positionsDict[key] = OrderedDict(sorted(positionsDict[key].items()))

    log.debug("positionsDict: " + str(positionsDict))

    sasa_positions = defaultdict(list)
    likelySites = []
    log.debug("Looking for likely sites.")
    for key in residueInfo.keys():
        log.debug("key: " + key)
        found = False
        if 'ASN' in key or 'NLN' in key:
            log.debug("\nFound one: " + key + "\n")
            value = residueInfo[key]
            chainId = value.GetResidueChainId()
            residueNumber = value.GetResidueSequenceNumber()
            residueName = value.GetResidueName()
            if 'ASN' in key:
                log.debug("ASN in key.")
                if positionsDict.get(residueNumber + 1) != "PRO":
                    log.debug("next residue is not PRO")
                    if positionsDict.get(residueNumber + 2) == "SER":
                        log.debug("next residue is SER \nappend to likely")
                        likelySites.append(key + "_likely")
                    if positionsDict.get(residueNumber + 2) == "THR":
                        log.debug("next residue is THR \nappend to likely")
                        likelySites.append(key + "_likely")
                else:
                    log.debug("Next residue is PRO")
            else:
                log.info("ASN not in key: " + key)


    return likelySites

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
