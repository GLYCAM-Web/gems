import gmml
from gemsModules.common.loggingConfig import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  REFACTORING - This needs to move into io.py, as part of preprocessPDBForAmber service.
##  Pass in an transaction and get a new, preprocessed pdbFile object, 
#       ready to be written to file.
#   @param transaction
def generatePdbFile(thisTransaction):
    log.info("generatePdbFile() was called.\n")

    try:
        ### Apply preprocessing
        preprocessor.ApplyPreprocessingWithTheGivenModelNumber(pdbFile, aminoLibs, glycamLibs, prepFile)
    except:
        log.error("There was a problem applying the preprocessing.")
        raise error
    
    ##Get the sequence mapping.
    try:
        seqMap = pdbFile.GetSequenceNumberMapping()
        log.debug("seqMap: " + str(seqMap))
    except Exception as error:
        log.error("Therre was a problem getting the sequence mapping.")
        raise error
    
    return pdbFile



## Wrapper for file writing homework
#   @param thisTransaction
#   @param pdbFile
def writePdbOutput(thisTransaction, pdbFile):
    log.info("writePdbOutput() was called.\n")

    ### Give the output file the same path as the uploaded file, but replace the name.
    try:
        projectDir = getProjectDir(thisTransaction)
        log.debug("projectDir: " + projectDir)  
    except Exception as error:
        log.error("There was a problem getting the output dir from the transaction.")
        raise error

    ### Write the file
    try:   
        writePdb(pdbFile, projectDir)
    except Exception as error:
        log.error("There was an error writing the pdb file.")
        raise error        


    ### Build a response
    try:
        responses = buildPdbResponses(thisTransaction)
        appendResponse(thisTransaction, responses)
    except Exception as error:
        log.error("There was a problem building the pdbResponse.")
        raise error
                           
def buildPdbResponses(thisTransaction : Transaction):
    log.info("buildPdbResponses() was called.\n")
    log.debug("thisTransaction.response_dict: ")
    prettyPrint(thisTransaction.response_dict)

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
#   @param request_dict
def getPdbRequestInput(request_dict : dict):
    log.info("getPdbRequestInput() was called.\n")

    ### Grab the inputs from the entity
    if 'inputs' in request_dict['entity'].keys():
        inputs = request_dict['entity']['inputs']

        uploaded_file_name = ""
        ### Get the frontend project
        project = request_dict['project']
        for element in inputs:
            #log.debug("element: " + str(element))

            ### Check for a pdb file or a pdb ID. 
            if "pdb_file_name" in element.keys():
                #log.debug("looking for the attached pdb file.")
                uploaded_file_name = getUploadFileName(project)
                log.debug("uploaded_file_name: " + uploaded_file_name)
                return uploaded_file_name

            elif "pdb_ID" in element.keys():
                ### Look for a pdb ID to sideload.
                log.debug("Side-loading pdb from rcsb.org.")
                pdbID = element['pdb_ID']
                uploadPath = project['upload_path']
                log.debug("uploadPath: " + uploadPath)
                try:
                    uploaded_file_name = sideloadPdbFromRcsb(pdbID, uploadPath)
                except Exception as error:
                    log.error("There was a problem sideloading the pdb from the RCSB.")
                    raise error
                
                log.debug("returning uploaded_file_name: " + uploaded_file_name)
                project['uploaded_file_name'] = uploaded_file_name
                return uploaded_file_name

            elif "metadata" in element.keys():
                if "descriptor" in element['metadata'].keys():
                    descriptor = element['metadata']['descriptor']
                    
                    if "resourceFormat" in descriptor.keys():
                        resourceFormat = descriptor['resourceFormat']
                        if resourceFormat == "PDBID":
                            log.debug("Side-loading pdb from rcsb.org.")
                            if "payload" in element.keys():
                                uploaded_file_name = sideloadPdbFromRcsb(element['payload'], project['upload_path'])
                                project['uploaded_file_name'] = uploaded_file_name
                                return uploaded_file_name
                        else:
                            if "locationType" in descriptor.keys():
                                locationType = descriptor['locationType']
                                if resourceFormat == "PDB" and locationType == "file-path":
                                    log.debug("upload file provided.")
                                    if "payload" in element.keys():
                                        uploaded_file_name = element['payload']
                                        return uploaded_file_name

                    else:
                        log.error("The descriptor element requires a resourceFormat. resourceFormat not found.")
                        raise AttributeError("resourceFormat")
                else:
                    log.error("The metadata element requires a descriptor. descriptor not found.")
                    raise AttributeError("descriptor")


            else:
                log.debug("Input unrelated to pdb preprocessing, skipping. element.keys(): " + str(element.keys()))

        if uploaded_file_name == "":
            raise AttributeError("Either pdb_file_name or pdb_ID must be present in the request's inputs.")
    else:
        log.error("No inputs found in request.")
        raise AttributeError("inputs")


##  Write the pdb file to the projectDir
#   @param pdbFile as created by gmml.PdbFile()
#   @param projectDir destination for pdb file
def writePdb(pdbFile, projectDir):
    log.info("writePdb() was called.\n")
    if os.path.exists(projectDir):
        log.debug("Writing the preprocessed pdb to 'updated_pdb.pdb'")
        destinationFile = 'updated_pdb.pdb'
        updatedPdbFileName = projectDir + "/" + destinationFile
        log.debug("updatedPdbFileName: " + updatedPdbFileName)
        pdbFile.WriteWithTheGivenModelNumber(updatedPdbFileName)
    else:
        raise IOError

## A method for providing default Amino libs
##TODO:  Update these paths to those in programs/Amber
#   @param gemsHome
def getDefaultAminoLibs():
    log.info("getDefaultAminoLibs() was called.\n")

    try:
        gemsHome = getGemsHome()
        log.debug("gemsHome: " + gemsHome)
    except Exception as error:
        log.error("There was a problem getting GEMSHOME.")
        raise error

    amino_libs = gmml.string_vector()
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib")

    for item in amino_libs:
        log.debug("amino_libs item: " + str(item))
    return amino_libs

##Prep file
def getDefaultPrepFile():
    log.info("getDefaultPrepFile() was called.\n")

    try:
        gemsHome = getGemsHome()
        log.debug("gemsHome: " + gemsHome)
    except Exception as error:
        log.error("There was a problem getting GEMSHOME.")
        raise error
    
    prepFile = gmml.string_vector()
    prepFile.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep")
    for item in prepFile:
        log.debug("prepFile item: " + str(item))
    return prepFile

## Used for sideloading.
def makeRequest(url):
    log.info("makeRequest() was called. url: " + url)
    try:
        with urllib.request.urlopen(url) as response:
            contentBytes = response.read()
            return contentBytes
    except Exception as error:
        log.error("There was a problem making the request: " + str(error))
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
            log.debug("First request failed. Trying again with a slight edit...")
            rcsbURL2 = "https://files.rcsb.org/download/" + pdbID + ".pdb"
            log.debug("Trying again with url: " + rcsbURL2)
            contentBytes = makeRequest(rcsbURL2)
            return contentBytes
        except Exception as error:
            log.error("There was a problem requesting this pdb from RCSB.org: " + str(error))
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




#########################################
#References below VVVVVVVVVVVVVVVVVVVVVVV


# ##  Give a transaction and a preprocessor object, get a dict with Missing Residue data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildMissingResiduesDict(thisTransaction, preprocessor):
#     log.info("buildMissingResiduesDict() was called.\n")
    
#     misData = []
#     missingResidues = preprocessor.GetMissingResidues()
#     log.info("length of missingResidues: " + str(len(missingResidues)))

#     for item in missingResidues: 
#         mapping = {}
#         chainID = item.GetResidueChainId()
#         mapping['chainID'] = chainID
#         log.debug("chainID: " + chainID)

#         ### If an insertion code is found, just append it to the sequence number.
#         startSequenceNumber = str(item.GetStartingResidueSequenceNumber())
#         startInsertionCode = item.GetStartingResidueInsertionCode()
#         if "?" not in startInsertionCode:
#             startSequenceNumber = startSequenceNumber + startInsertionCode
#         mapping['startSequenceNumber'] = startSequenceNumber
#         log.debug("startSequenceNumber: " + startSequenceNumber)

#         ### If an insertion code is found, just append it to the sequence number.
#         endSequenceNumber = str(item.GetEndingResidueSequenceNumber())
#         endInsertionCode = item.GetEndingResidueInsertionCode()
#         if "?" not in endInsertionCode:
#             endSequenceNumber = endSequenceNumber + endInsertionCode
#         mapping['endSequenceNumber'] = endSequenceNumber
#         log.debug("endSequenceNumber: " + endSequenceNumber)

#         residueBeforeGap = str(item.GetResidueBeforeGap())
#         mapping['residueBeforeGap'] = residueBeforeGap
#         log.debug("residueBeforeGap: " + residueBeforeGap)

#         residueAfterGap = str(item.GetResidueAfterGap())
#         mapping['residueAfterGap'] = residueAfterGap
#         log.debug("residueAfterGap: " + residueAfterGap)

#         misData.append(mapping)

#     return misData


# ##  Give a transaction and a preprocessor object, get a dict with Unrecognized Heavy Atom data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildUnrecognizedHeavyAtomsDict(thisTransaction, preprocessor):
#     log.info("buildUnrecognizedHeavyAtomsDict() was called.\n")

#     hvyData = []
#     hvyAtoms = preprocessor.GetUnrecognizedHeavyAtoms()
#     log.info("length of hvyAtoms: " + str(len(hvyAtoms)))

#     for item in hvyAtoms:
#         mapping = {}
#         index = str(item.GetAtomSerialNumber())
#         mapping['index'] = index
#         log.debug("index: " + index)

#         atomName = item.GetAtomName()
#         mapping['atomName'] = atomName
#         log.debug("atomName: " + atomName)

#         residueName = item.GetResidueName()
#         mapping['residueName'] = residueName
#         log.debug("residueName: " + residueName)

#         chainID = item.GetResidueChainId()
#         mapping['chainID'] = chainID
#         log.debug("chainID: " + chainID)

#         ### If an insertion code is found, just append it to the sequence number.
#         residueNumber = str(item.GetResidueSequenceNumber())
#         insertionCode = str(item.GetResidueInsertionCode())
#         if "?" not in insertionCode:
#             residueNumber = residueNumber + insertionCode
#         mapping['residueNumber'] = residueNumber
#         log.debug("residueNumber: " + residueNumber)


#         hvyData.append(mapping)

#     return hvyData


# ##  Give a transaction and a preprocessor object, get a dict with Replaced Hydrogen data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildReplacedHydrogensDict(thisTransaction, preprocessor):
#     log.info("buildReplacedHydrogensDict() was called.\n")

#     hydData = []
#     replacedHydrogens = preprocessor.GetReplacedHydrogens()
#     log.info("length of replacedHydrogens: " + str(len(replacedHydrogens)))

#     for item in replacedHydrogens:
#         mapping = {}
#         index = str(item.GetAtomSerialNumber())
#         mapping['index'] = index
#         log.debug("index: " + index)

#         atomName = item.GetAtomName()
#         mapping['atomName'] = atomName
#         log.debug("atomName: " + atomName)

#         residueName = item.GetResidueName()
#         mapping['residueName'] = residueName
#         log.debug("residueName: " + residueName)

#         chainID = item.GetResidueChainId()
#         mapping['chainID'] = chainID
#         log.debug("chainID: " + chainID)

#         ### If an insertion code is found, just append it to the sequence number.
#         residueNumber = str(item.GetResidueSequenceNumber())
#         insertionCode = item.GetResidueInsertionCode()
#         if "?" not in insertionCode:
#             residueNumber = residueNumber + insertionCode

#         mapping['residueNumber'] = residueNumber
#         log.debug("residueNumber: " + residueNumber)


#         hydData.append(mapping)

#     return hydData


# ##  Give a transaction and a preprocessor object, get a dict with Chain Termination data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildChainTerminationsDict(thisTransaction, preprocessor):
#     log.info("buildChainTerminationsDict() was called.\n")

#     terData = []
#     chainTerminations = preprocessor.GetChainTerminations()
#     log.debug("length of chainTerminations: " + str(len(chainTerminations)))

#     for item in chainTerminations:
#         mapping = {}
#         chainID = item.GetResidueChainId()
#         mapping['chainID'] = chainID
#         log.debug("chainID: " + chainID)

#         ### If an insertion code is found, just append it to the start index.
#         startIndex = str(item.GetStartingResidueSequenceNumber())
#         startInsertion = str(item.GetStartingResidueInsertionCode())
#         if "?" not in startInsertion:
#             startIndex = startIndex + startInsertion

#         mapping['startIndex'] = startIndex
#         log.debug("startIndex: " + startIndex)

#         ### If an insertion code is found, just append it to the end index.
#         endIndex = str(item.GetEndingResidueSequenceNumber())
#         endInsertion = str(item.GetEndingResidueInsertionCode())
#         if "?" not in endInsertion:
#             endIndex = endIndex + endInsertion
#         mapping['endIndex'] = endIndex
#         log.debug("endIndex: " + endIndex)

#         terData.append(mapping)

#     return terData       



# ##  Give a transaction and a preprocessor object, get a dict with Unrecognized Residue data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildUnrecognizedResiduesDict(thisTransaction, preprocessor):
#     log.info("buildUnrecognizedResiduesDict() was called.\n")

#     unresData = []
#     unrecognizedResidues = preprocessor.GetUnrecognizedResidues()
#     log.debug("length of unrecognizedResidues: " + str(len(unrecognizedResidues)))

#     for item in unrecognizedResidues:
#         mapping = {}
#         chainID = item.GetResidueChainId()
#         mapping['chainID'] = chainID
#         log.debug("chainID: " + chainID)

#         ### If an insertion code is found, just append it to the index.
#         index = str(item.GetResidueSequenceNumber())
#         insertionCode = item.GetResidueInsertionCode()
#         if "?" not in insertionCode: 
#             index = index + insertionCode
#         mapping['index'] = index
#         log.debug("index: " + index)

#         name = item.GetResidueName()
#         mapping['name'] = name
#         log.debug("name: " + name)

#         isMidChain = str(item.GetMiddleOfChain())
#         mapping['isMidChain'] = isMidChain
#         log.debug("isMidChain: " + isMidChain)

#         unresData.append(mapping)

#     return unresData


# ##  Give a transaction and a preprocessor object, get a dict with Disulfide Bonding data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildDisulfideBondsDict(thisTransaction, preprocessor):
#     log.info("buildDisulfideBondsDict() was called.\n")

#     cysData = []
#     disulfideBonds = preprocessor.GetDisulfideBonds()
#     log.debug("length of disulfideBonds: " + str(len(disulfideBonds)))

#     for item in disulfideBonds:
#         mapping = {}

#         ### TODO:Dummy method. Replace with GMML logic
#         amberResidueName = getAmberResidueName(item)

#         ### Residue 1
#         residue1ChainId = item.GetResidueChainId1()
#         mapping['residue1ChainId'] = residue1ChainId
#         log.debug("residue1ChainId: " + residue1ChainId)

#         residue1Number = str(item.GetResidueSequenceNumber1())
#         mapping['residue1Number'] = residue1Number
#         log.debug("residue1Number: " + residue1Number)

#         mapping['residue1AmberResidueName'] = amberResidueName
#         log.debug("residue1AmberResidueName: " + amberResidueName)

#         ### Residue2
#         residue2ChainId = item.GetResidueChainId2()
#         mapping['residue2ChainId'] = residue2ChainId
#         log.debug("residue2ChainId: " + residue2ChainId)

#         residue2Number = str(item.GetResidueSequenceNumber2())
#         mapping['residue2Number'] = residue2Number
#         log.debug("residue2Number: " + residue2Number)

#         mapping['residue2AmberResidueName'] = amberResidueName
#         log.debug("residue2AmberResidueName: " + amberResidueName)
        
#         ### Distance
#         distance = str(roundHalfUp(item.GetDistance(), 4))
#         mapping['distance'] = distance
#         log.debug("distance: " + distance)

#         ### Bonded
#         bonded = str(item.GetIsBonded())
#         mapping['bonded'] = bonded
#         log.debug("bonded: " + bonded)

#         cysData.append(mapping)

#     return cysData




# ##  Give a transaction and a preprocessor object, get a dict with Histidine mapping data from a pdb
# #   @param thisTransaction
# #   @param preprocessor
# def buildHistidineProtonationsDict(thisTransaction, preprocessor):
#     log.info("buildHistidineProtonationsDict() was called.\n")

#     histidineMappings = preprocessor.GetHistidineMappings()
#     log.debug("length of histidineMappings: " + str(len(histidineMappings)))
#     hisData = []
#     for item in histidineMappings:
#         mapping = {}
#         chainID = item.GetResidueChainId()
#         mapping['chainID'] = chainID
#         log.debug("chainID: " + chainID)

#         ### if an insertionCode is found, just append that to the residueNumber.
#         residueNumber = str(item.GetResidueSequenceNumber())
#         insertionCode = item.GetResidueInsertionCode()
#         if "?" not in insertionCode:
#             residueNumber = residueNumber + insertionCode

#         mapping['residueNumber'] = residueNumber
#         log.debug("residueNumber: " + residueNumber)
        

#         mappingFormat = item.GetStringFormatOfSelectedMapping()
#         mapping['mappingFormat'] = mappingFormat
#         log.debug("mappingFormat: " + mappingFormat)

#         hisData.append(mapping)

#     return hisData



# ##TODO: REFACTOR THIS TO USE PYDANTIC
# ##  Adds any options data to the transaction's response. Used for options tables by the frontend.
# #   @param thisTransaction
# #   @param preprocessor
# def updateTransactionWithPreprocessorOptions(thisTransaction, preprocessor):
#     log.info("updateTransactionWithPreprocessorOptions() was called.\n")

#     if thisTransaction.response_dict == None:
#         thisTransaction.response_dict = {}

#     if 'entity' not in thisTransaction.response_dict.keys():
#         thisTransaction.response_dict['entity'] = {}
#         thisTransaction.response_dict['entity']['type'] = "StructureFile"
#     if 'responses' not in thisTransaction.response_dict.keys():
#         thisTransaction.response_dict['responses'] = []

#     response = {}
#     response["PreprocessingOptions"] = {}
#     tableMetaData ={}

#     ### Update the Histidine Protonation data, HIS
#     hisData = buildHistidineProtonationsDict(thisTransaction, preprocessor)
#     if len(hisData) != 0:
#         response['PreprocessingOptions']['histidineProtonation'] = {}
#         response['PreprocessingOptions']['histidineProtonation'] = hisData

#         tableMetaData.update({
#             "histidineProtonation" : { 
#                 "tableLabel" : "Histidine Protonation",  
#                 "interactionRequirement" : "optional",
#                 "urgency" : "info",
#                 "count" : str(len(hisData)),
#                 "description" : amberStructureSettings.descriptions['histidineProtonation']
#             }
#         })
#     else:
#         log.debug("length of hisData: " + str(len(hisData)))

#     ### Update the Disulfide Bond data, CYS 
#     cysData = buildDisulfideBondsDict(thisTransaction, preprocessor)
#     if len(cysData) != 0:
#         response['PreprocessingOptions']['disulfideBonds'] = {}
#         response['PreprocessingOptions']['disulfideBonds'] = cysData

#         ### a value of "warning" indicates optional action can be taken, but is not needed.
#         tableMetaData.update({
#             'disulfideBonds' : { 
#                 "tableLabel" : "Disulfide Bonds", 
#                 "interactionRequirement" : "optional",
#                 "urgency" : "info",
#                 "count" : str(len(cysData)),
#                 "description" : amberStructureSettings.descriptions['disulfideBonds']
#             }
#         })
#     else:
#         log.debug("length of cysData: " + str(len(cysData)))

#     ### Update the Unrecognized Residue data, UNRES
#     unresData = buildUnrecognizedResiduesDict(thisTransaction, preprocessor)
#     if len(unresData) != 0:
#         response['PreprocessingOptions']['unrecognizedResidues'] = {}
#         response['PreprocessingOptions']['unrecognizedResidues'] = unresData
#         urgencyLevel = getUrgencyLevelForUnrecognizedResidues(unresData)

#          ### Any mid-chain unrecognized residues cause error level urgency,
#          #  terminals just get warnings.
#         tableMetaData.update({
#             'unrecognizedResidues' : { 
#                 "tableLabel" : "Unrecognized Residues", 
#                 "interactionRequirement" : "none",
#                 "urgency" : urgencyLevel,
#                 "count" : str(len(unresData)),
#                 "description" : amberStructureSettings.descriptions['unrecognizedResidues']
#             }
#         })
#     else:
#         log.debug("length of unresData: " + str(len(unresData)))

#     ### Update the Chain Termination data, TER
#     terData = buildChainTerminationsDict(thisTransaction, preprocessor)
#     if len(terData) != 0: 
#         response['PreprocessingOptions']['chainTerminations'] = {}
#         response['PreprocessingOptions']['chainTerminations'] = terData

#         tableMetaData.update({
#             'chainTerminations' : {
#                 "tableLabel" : "Chain Terminations", 
#                 "interactionRequirement" : "optional",
#                 "urgency" : "info",
#                 "count" : str(len(terData)),
#                 "description" : amberStructureSettings.descriptions['chainTerminations']
#             }
#         })
#     else:
#         log.debug("length of terData: " + str(len(terData)))

#     ### Update the Replaced Hydrogen data, HYD
#     hydData = buildReplacedHydrogensDict(thisTransaction, preprocessor)
#     if len(hydData) != 0:
#         response['PreprocessingOptions']['replacedHydrogens'] = {}
#         response['PreprocessingOptions']['replacedHydrogens'] = hydData

#         tableMetaData.update({
#             'replacedHydrogens' : {
#                 "tableLabel" : "Replaced Hydrogens", 
#                 "interactionRequirement" : "none",
#                 "urgency" : "info",
#                 "count" : str(len(hydData)),
#                 "description" : amberStructureSettings.descriptions['replacedHydrogens']
#             }
#         })
#     else:
#         log.debug("length of hydData: " + str(len(hydData)))

#     ### Update the Unrecognized Heavy Atoms data, HVY
#     hvyData = buildUnrecognizedHeavyAtomsDict(thisTransaction, preprocessor)
#     if len(hvyData) != 0:
#         response['PreprocessingOptions']['unrecognizedHeavyAtoms'] = {}
#         response['PreprocessingOptions']['unrecognizedHeavyAtoms'] = hvyData

#         ### If any of these exist, we've got nothing. No can do.
#         tableMetaData.update({
#             'unrecognizedHeavyAtoms' : {
#                 "tableLabel" : "Unrecognized Heavy Atoms", 
#                 "interactionRequirement": "none",
#                 "urgency": "error",
#                 "count" : str(len(hvyData)),
#                 "description" : amberStructureSettings.descriptions['unrecognizedHeavyAtoms']
#             }
#         } )
#     else:
#         log.debug("length of hvyData: " + str(len(hvyData)))

#     ### Update the Missing Residues data, MIS
#     misData = buildMissingResiduesDict(thisTransaction, preprocessor)
#     if len(misData) != 0:
#         response['PreprocessingOptions']['missingResidues'] = {}
#         response['PreprocessingOptions']['missingResidues'] = misData

#         tableMetaData.update({
#             'missingResidues' : {
#                 "tableLabel" : "Missing Residues", 
#                 "interactionRequirement": "optional",
#                 "urgency": "warning",
#                 "count" : str(len(misData)),
#                 "description" : amberStructureSettings.descriptions['missingResidues']
#             }
#         })
#     else:
#         log.debug("length of misData: " + str(len(misData)))

#     ## Add the tableMetaData to the response.
#     response.update({"tableMetaData" : tableMetaData})
#     thisTransaction.response_dict['responses'].append(response)

