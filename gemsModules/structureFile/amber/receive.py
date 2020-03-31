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
                raise error
            else:

                ### Write the content to file
                try:
                    writePdbOutput(thisTransaction, pdbFile)
                except Exception as error:
                    log.error("There was a problem writing the pdb output.")
                    raise error
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
        prepFile = getDefaultPrepFile(gemsHome)
        glycamLibs = gmml.string_vector()
        otherLibs = gmml.string_vector()
        preprocessor = gmml.PdbPreprocessor()
        log.debug("preprocessor: " + str(preprocessor))


        ### Get the fileName from the transaction.
        project = thisTransaction.request_dict['project']
        try:
            outputDir = getOutputDir(thisTransaction)
        except Exception as error:
            log.error("There was a problem getting the output dir.")
            log.error(traceback.format_exc())
            raise error
        else:
            projectDir  = getProjectUploadsDir(project, outputDir)
            uploadedFileName = project['uploaded_file_name']
            log.debug("uploadedFileName: " + uploadedFileName)
            uploadedPDB = projectDir + uploadedFileName
            #PDB file object:
            log.debug("uploadedPDB: " + uploadedPDB)
            try:
                pdbFile = gmml.PdbFile(uploadedPDB)
                log.debug("pdbFile: " + str(pdbFile))
            except Exception as error:
                log.error("There was a problem creating the pdbFile object from the uploaded pdb file.")
                log.error(traceback.format_exc)
                raise error
            else:
                try:
                    ### Preprocess
                    preprocessor.Preprocess(pdbFile, aminoLibs, glycamLibs, otherLibs, prepFile)
                    updateTransactionWithPreprocessorOptions(thisTransaction, preprocessor)
                    
                except Exception as error:
                    log.error("There was a problem preprocessing with gmml.")
                    log.error(traceback.format_exc())
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
                        else:
                            return pdbFile


##  Adds any options data to the transaction's response. Used for options tables by the frontend.
#   @param thisTransaction
#   @param preprocessor
def updateTransactionWithPreprocessorOptions(thisTransaction, preprocessor):
    log.info("updateTransactionWithPreprocessorOptions() was called.\n")

    ### Update the Histidine Protonation data, HIS
    updateHISData(thisTransaction, preprocessor)

    ### Update the Disulfide Bond data, CYS
    updateCYSData(thisTransaction, preprocessor)

    ### Update the Unrecognized Residue data, UNRES
    updateUNRESData(thisTransaction, preprocessor)

    ### Update the Chain Termination data, TER
    updateTERData(thisTransaction, preprocessor)

    ### Update the Replaced Hydrogen data, HYD
    updateHYDData(thisTransaction, preprocessor)

    ### Update the Unrecognized Heavy Atoms data, HVY
    updateHVYData(thisTransaction, preprocessor)

    ### Update the Missing Residues data, MIS
    updateMISData(thisTransaction, preprocessor)


##  Updates the transaction with Missing Residue data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateMISData(thisTransaction, preprocessor):
    log.info("updateMISData() was called.\n")
    
    missingResidues = preprocessor.GetMissingResidues()
    log.info("length of missingResidues: " + str(len(missingResidues)))

    for item in missingResidues: 
        chainID = item.GetResidueChainId()
        log.debug("chainID: " + chainID)
        startSequenceNumber = str(item.GetStartingResidueSequenceNumber())
        log.debug("startSequenceNumber: " + startSequenceNumber)
        endSequenceNumber = str(item.GetEndingResidueSequenceNumber())
        log.debug("endSequenceNumber: " + endSequenceNumber)
        residueBeforeGap = str(item.GetResidueBeforeGap())
        log.debug("residueBeforeGap: " + residueBeforeGap)
        residueAfterGap = str(item.GetResidueAfterGap())
        log.debug("residueAfterGap: " + residueAfterGap)
        startInsertionCode = item.GetStartingResidueInsertionCode()
        log.debug("startInsertionCode: " + startInsertionCode)
        endInsertionCode = item.GetEndingResidueInsertionCode()
        log.debug("endInsertionCode: " + endInsertionCode)



    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")


##  Updates the transaction with Unrecognized Heavy Atom data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateHVYData(thisTransaction, preprocessor):
    log.info("updateHVYData() was called.\n")

    hvyAtoms = preprocessor.GetUnrecognizedHeavyAtoms()
    log.info("length of hvyAtoms: " + str(len(hvyAtoms)))

    for item in hvyAtoms:
        index = str(item.GetAtomSerialNumber())
        log.debug("index: " + index)
        atomName = item.GetAtomName()
        log.debug("atomName: " + atomName)
        residueName = item.GetResidueName()
        log.debug("residueName: " + residueName)
        chainID = item.GetResidueChainId()
        log.debug("chainID: " + chainID)
        residueNumber = str(item.GetResidueSequenceNumber())
        log.debug("residueNumber: " + residueNumber)
        insertionCode = str(item.GetResidueInsertionCode())
        log.debug("insertionCode: " + insertionCode)

    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")


##  Updates the transaction with Replaced Hydrogen data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateHYDData(thisTransaction, preprocessor):
    log.info("updateHYDData() was called.\n")

    replacedHydrogens = preprocessor.GetReplacedHydrogens()
    log.info("length of replacedHydrogens: " + str(len(replacedHydrogens)))

    for item in replacedHydrogens:
        index = str(item.GetAtomSerialNumber())
        log.debug("index: " + index)
        atomName = item.GetAtomName()
        log.debug("atomName: " + atomName)
        residueName = item.GetResidueName()
        log.debug("residueName: " + residueName)
        chainID = item.GetResidueChainId()
        log.debug("chainID: " + chainID)
        residueNumber = str(item.GetResidueSequenceNumber())
        log.debug("residueNumber: " + residueNumber)
        insertionCode = item.GetResidueInsertionCode()
        log.debug("insertionCode: " + insertionCode)

    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")


##  Updates the transaction with Chain Termination data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateTERData(thisTransaction, preprocessor):
    log.info("updateTERData() was called.\n")

    chainTerminations = preprocessor.GetChainTerminations()
    log.debug("length of chainTerminations: " + str(len(chainTerminations)))

    for item in chainTerminations:
        chainID = item.GetResidueChainId()
        log.debug("chainID: " + chainID)
        startIndex = str(item.GetStartingResidueSequenceNumber())
        log.debug("startIndex: " + startIndex)
        startInsertion = str(item.GetStartingResidueInsertionCode())
        log.debug("startInsertion: " + startInsertion)
        endIndex = str(item.GetEndingResidueSequenceNumber())
        log.debug("endIndex: " + endIndex)
        endInsertion = str(item.GetEndingResidueInsertionCode())
        log.debug("endInsertion: " + endInsertion)

    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")        



##  Updates the transaction with Unrecognized Residue data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateUNRESData(thisTransaction, preprocessor):
    log.info("updateUNRESData() was called.\n")

    unrecognizedResidues = preprocessor.GetUnrecognizedResidues()
    log.debug("length of unrecognizedResidues: " + str(len(unrecognizedResidues)))

    for item in unrecognizedResidues:
        chainID = item.GetResidueChainId()
        log.debug("chainID: " + chainID)
        index = str(item.GetResidueSequenceNumber())
        log.debug("index: " + index)
        insertionCode = item.GetResidueInsertionCode()
        log.debug("insertionCode: " + insertionCode)
        name = item.GetResidueName()
        log.debug("name: " + name)
        isMidChain = str(item.GetMiddleOfChain())
        log.debug("isMidChain: " + isMidChain)

    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")

##  Updates the transaction with Disulfide Bonding data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateCYSData(thisTransaction, preprocessor):
    log.info("updateCYSData() was called.\n")

    disulfideBonds = preprocessor.GetDisulfideBonds()
    log.debug("length of disulfideBonds: " + str(len(disulfideBonds)))

    for item in disulfideBonds:
        residue1Number = str(item.GetResidueSequenceNumber1())
        log.debug("residue1Number: " + residue1Number)
        residue2Number = str(item.GetResidueSequenceNumber2())
        log.debug("residue2Number: " + residue2Number)
        distance = str(item.GetDistance())
        log.debug("distance: " + distance)

    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")

##  Updates the transaction with Histidine mapping data from a pdb
#   @param thisTransaction
#   @param preprocessor
def updateHISData(thisTransaction, preprocessor):
    log.info("updateHISData() was called.\n")

    histidineMappings = preprocessor.GetHistidineMappings()
    log.debug("length of histidineMappings: " + str(len(histidineMappings)))

    for item in histidineMappings:
        chainID = item.GetResidueChainId()
        log.debug("chainID: " + chainID)
        residueNumber = str(item.GetResidueSequenceNumber())
        log.debug("residueNumber: " + residueNumber)
        insertionCode = item.GetResidueInsertionCode()
        log.debug("instertionCode: " + insertionCode)
        mappingFormat = item.GetStringFormatOfSelectedMapping()
        log.debug("mappingFormat: " + mappingFormat)

    ##TODO: Add to the response in the transaction
    log.debug("Add to response in transaction.")

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
                log.debug("uploadFileName: " + uploadFileName)
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
                    frontendProject['uploaded_file_name'] = uploadFileName
                    return uploadFileName

            elif "metadata" in element.keys():
                if "descriptor" in element['metadata'].keys():
                    descriptor = element['metadata']['descriptor']
                    
                    if "resourceFormat" in descriptor.keys():
                        resourceFormat = descriptor['resourceFormat']
                        if resourceFormat == "PDBID":
                            log.debug("Side-loading pdb from rcsb.org.")
                            if "payload" in element.keys():
                                uploadFileName = sideloadPdbFromRcsb(element['payload'], frontendProject['upload_path'])
                                frontendProject['uploaded_file_name'] = uploadFileName

                        else:
                            if "locationType" in descriptor.keys():
                                locationType = descriptor['locationType']
                                if resourceFormat == "PDB" and locationType == "file-path":
                                    log.debug("upload file provided.")
                                    if "payload" in element.keys():
                                        uploadFileName = element['payload']
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

        pdbFileName = pdbID + ".pdb"


        uploadTarget = uploadDir  + pdbFileName
        log.debug("uploadTarget: " + uploadTarget)
        try:
            ##Save the string to file in the uploads dir.
            with open(uploadTarget, "w") as uploadFile:
                uploadFile.write(contentString)
        except Exception as error:
            log.error("There was a problem writing the sideloaded content into the file.")
            raise error
        else:
            return pdbFileName


## A method for providing default Amino libs
##TODO:  Update these paths to those in programs/Amber
#   @param gemsHome
def getDefaultAminoLibs(gemsHome):
    log.info("getDefaultAminoLibs() was called.\n")
    amino_libs = gmml.string_vector()
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib")

    for item in amino_libs:
        log.debug("amino_libs item: " + str(item))
    return amino_libs

##Prep file
def getDefaultPrepFile(gemsHome):
    log.info("getDefaultPrepFile() was called.\n")
    prepFile = gmml.string_vector()
    prepFile.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep")
    for item in prepFile:
        log.debug("prepFile item: " + str(item))
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
        
    
