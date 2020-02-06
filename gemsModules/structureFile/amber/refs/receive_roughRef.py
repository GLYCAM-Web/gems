import os, sys, importlib.util
import gemsModules
import gmml
from collections import defaultdict
from collections import OrderedDict

#from swigwrapper import SwigObj

from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
import gemsModules.mmservice.settings as mmSettings
import traceback

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.DEBUG

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

class MenuItem():
    def __init__(self, name = None, status=None, shortname = None, enabled = None, url = None, summary = None):
        self.status = status#Enum('Status','GOOD NEEDS_ATTENTION BAD')
        self.name = name
        self.shortname = shortname
        self.enabled = enabled
        self.url=url
        self.summary=summary
        self.items = []

def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called.")
    ## Check the files, if not happy with the file type return error.
    requestDict = thisTransaction.request_dict
    log.debug("requestDict: " + str(requestDict))
    entity = requestDict['entity']['type']
    log.debug("entity: " + entity)
    gemsHome = getGemsHome()

    menuSections = []
    ##Orchestrate things here, break out methods where possible.
    ##TODO: Get it working first, then refactor.
    if "project" in requestDict.keys():
        project = requestDict['project']
        uploadFileName = getUploadFileName(project)
        log.debug("Starting a gemsProject for the structureFile/amber module.")
        startGemsProject(thisTransaction, uploadFileName)

        ##Instantiate a pdbPreprocessor object.
        pdbPreprocessor = gmml.PdbPreprocessor()

        amino_libs = getAminoLibs(gemsHome)
        glycam_libs = gmml.string_vector()
        other_libs = gmml.string_vector()
        prepFile = getPrepFile(gemsHome)
        pdbFile = gmml.PdbFile(uploadFileName)

        ##HistidineMappings
        pdbPreprocessor.ExtractHISResidues(pdbFile)
        histidineMappings = pdbPreprocessor.GetHistidineMappings()
        showHistidineMappings = False
        if len(histidineMappings) > 0:
            showHistidineMappings = True
        log.debug("showHistidineMappings: " + str(showHistidineMappings))
        histidineSection = MenuItem(
            "Histidine Protonation",
            "GOOD",
            "his",
            showHistidineMappings,
            None,
            len(histidineMappings)
        )
        histidineSection.items = histidineMappings
        menuSections.append(histidineSection)

        ##DisulfideBonds
        pdbPreprocessor.ExtractCYSResidues(pdbFile)
        disulfideBonds = pdbPreprocessor.GetDisulfideBonds()
        showDisulfideBonds = False
        if len(disulfideBonds) > 0:
            showDisulfideBonds = True
        log.debug("showDisulfideBonds: " + str(showDisulfideBonds))
        disulfideSection = MenuItem(
            "Disulfide Bonds",
            "GOOD",
            "cys",
            showDisulfideBonds,
            None,
            len(disulfideBonds)
        )
        disulfideSection.items = disulfideBonds
        menuSections.append(disulfideSection)

        ##UnrecognizedResidues
        pdbPreprocessor.ExtractUnrecognizedResidues(pdbFile, amino_libs, glycam_libs, other_libs, prepFile)
        unrecognizedResidues = pdbPreprocessor.GetUnrecognizedResidues()
        showUnrecognizedResidues = False
        unrecognizedResidueStatus = "GOOD"
        if len(unrecognizedResidues) > 0:
            showUnrecognizedResidues = True
            unrecognizedResidueStatus = "BAD"
        log.debug("showUnrecognizedResidues: " + str(showUnrecognizedResidues))
        log.debug("unrecognizedResidueStatus: " + unrecognizedResidueStatus)
        unrecognizedResidueSection = MenuItem(
            "Unrecognized Residues",
            unrecognizedResidueStatus,
            "unres",
            showUnrecognizedResidues,
            None,
            len(unrecognizedResidues)
        )
        unrecognizedResidueSection.items = unrecognizedResidues
        menuSections.append(unrecognizedResidueSection)

        ##ChainTerminations
        pdbPreprocessor.ExtractAminoAcidChains(pdbFile)
        chainTerminations = pdbPreprocessor.GetChainTerminations()
        showChainTerminations = False
        if len(chainTerminations) > 0:
            showChainTerminations = True
        log.debug("showChainTerminations: " + str(showChainTerminations))
        chainTerminationSection = MenuItem(
            "Chain Termination",
            "GOOD",
            "ter",
            showChainTerminations,
            None,
            len(chainTerminations)
        )
        chainTerminationSection.items = chainTerminations
        menuSections.append(chainTerminationSection)

        ##ReplacedHydrogens
        pdbPreprocessor.ExtractRemovedHydrogens(pdbFile, amino_libs, glycam_libs, other_libs, prepFile )
        replacedHydrogens = pdbPreprocessor.GetUnrecognizedHeavyAtoms()
        showReplacedHydrogens = False
        if len(replacedHydrogens) > 0:
            showReplacedHydrogens = True
        log.debug("showReplacedHydrogens: " + str(showReplacedHydrogens))
        replacedHydrogenSection = MenuItem(
            "Replaced Hydrogens",
            "GOOD",
            "hyd",
            showReplacedHydrogens,
            None,
            len(replacedHydrogens)
        )
        replacedHydrogenSection.items = replacedHydrogens
        menuSections.append(replacedHydrogenSection)

        ##UnknownHeavyAtoms
        pdbPreprocessor.ExtractUnknownHeavyAtoms(pdbFile, amino_libs, glycam_libs, other_libs, prepFile)
        unrecognizedHeavyAtoms = pdbPreprocessor.GetUnrecognizedHeavyAtoms()
        unrecognizedHeavyAtomsStatus = "GOOD"
        showUnrecognizedHeavyAtoms = False
        if len(unrecognizedHeavyAtoms) > 0:
            showUnrecognizedHeavyAtoms = True
            unrecognizedHeavyAtomsStatus = "BAD"
        log.debug("showUnrecognizedHeavyAtoms: " + str(showUnrecognizedHeavyAtoms))
        log.debug("unrecognizedHeavyAtomsStatus: " + unrecognizedHeavyAtomsStatus)
        unrecognizedHeavyAtomsSection = MenuItem(
            "Unrecognized Heavy Atoms",
            unrecognizedHeavyAtomsStatus,
            "hvy",
            showUnrecognizedHeavyAtoms,
            None,
            len(unrecognizedHeavyAtoms)
        )
        unrecognizedHeavyAtomsSection.items = unrecognizedHeavyAtoms
        menuSections.append(unrecognizedHeavyAtomsSection)

        ##MissingResidues
        pdbPreprocessor.ExtractGapsInAminoAcidChains(pdbFile, amino_libs)
        missingResidues = pdbPreprocessor.GetMissingResidues()
        showMissingResidues = False
        if len(missingResidues) > 0:
            showMissingResidues = True
        log.debug("showMissingResidues: " + str(showMissingResidues))
        missingResidueSection = MenuItem(
            "Missing Residues",
            "GOOD",
            "mis",
            showMissingResidues,
            None,
            len(missingResidues)
        )
        missingResidueSection.items = missingResidues
        menuSections.append(missingResidueSection)

        ##ResidueInfo
        pdbPreprocessor.ExtractResidueInfo(pdbFile, amino_libs, glycam_libs, other_libs, prepFile)
        residueInfo = pdbPreprocessor.GetResidueInfoMap()
        log.debug("residueInfo object type: " + str(type(residueInfo)))

        ##PositionsDict
        positionsDict = {}
        for key, value in residueInfo.items():
            residueChainId = value.GetResidueChainId()
            residueSequenceNumber = value.GetResidueSequenceNumber()
            residueName = value.GetResidueName()
            #log.debug("residueChainId: "  + residueChainId + ", residueSequenceNumber: " + str(residueSequenceNumber) + ", residueName: " + residueName)

            if not positionsDict.get(residueChainId):
                positionsDict[residueChainId] = {}

            positionsDict[residueChainId][residueSequenceNumber] = residueName
        #log.debug("positionsDict: \n" + str(positionsDict))
        ##Now sort the positionsDict.
        for key in positionsDict.keys():
            #log.debug("key: " + key)
            positionsDict[key] = OrderedDict(sorted(positionsDict[key].items()))
        #log.debug("positionsDict, after ordering:\n " + str(positionsDict))

        sequenceMap = pdbFile.GetSequenceNumberMapping()
        log.debug("sequenceMap: " + str(sequenceMap))

        #COPY PASTA ALERT:
        #for section in menuSections:
        #    section.items = [SwigObj(obj) for obj in section.items]

        if "gems_project" in requestDict.keys():
            outputDir = requestDict['gems_project']["outut_dir"]
            log.debug("outputDir: " + outputDir)

            if not os.path.isdir(outputDir):
                os.mkdir(outputDir)

            pickleFile = outputDir + "pickle_dump"
            log.debug("Writing pickle file: " + pickleFile)
            with open(pickleFile, "wb") as handle:
                pickle.dump(
                    (menuSections, sasaPositions),
                    handle,
                    protocol=pickle.HIGHEST_PROTOCOL
                )

            gemsDoneFile = outputDir + "run_gems_done"
            log.debug("Writing gems done file: " + gemsDoneFile)
            with open(gemsDoneFile, "w") as done:
                done.write("pdb preprocessing done")

            log.debug("Finished writing output to disc.")

            return menuSections, sasaPositions
        else:
            log.error("No gems_project found in request.")

    else:
        log.error("No project found in request.")

    #log.debug("thisTransaction: \n" + str(thisTransaction.__dict__))


def getPrepFile(gemsHome):
    log.info("getPrepFile() was called.\n")
    prepFile = gmml.string_vector()
    prepFile.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep")
    return prepFile

def getAminoLibs(gemsHome):
    log.info("getAminoLibs() was called.\n")
    amino_libs = gmml.string_vector()
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
    ##Why is this duplicated? Does it need two? Looks like an error from the past copied and pasted forward.
    amino_libs.push_back(gemsHome + "/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
    return amino_libs

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

def getUploadFileName(project):
    log.info("getUploadFileName() was called.\n")
    ##Get the file name, combine path and file for full name.
    uploadFileName = ""
    if "uploaded_file_name" in project.keys():
        uploadFileName = project['uploaded_file_name']
        log.debug("uploadFileName: " + uploadFileName)
    else:
        log.error("No uploaded_file_name found in project.")

    if "upload_path" in project.keys():
        uploadPath = project['upload_path']
        log.debug("uploadPath: " + uploadPath)
        uploadFileName = uploadPath + uploadFileName
        log.debug("Updated uploadFileName: " + uploadFileName)
    else:
        log.error("No upload_path found in project.")

    return uploadFileName

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.\n")
    ##Preprocess PDB will be the default
    preprocessPdbForAmber(thisTransaction)


""" Some potentially useful logic when working with the GP builder:
##SASA Positions _
        sasaPositions = defaultdict(list)
        for key in residueInfo.keys():
            #log.debug("key: " + key)
            if "ASN" in key or "NLN" in key:
                log.debug("Found one. key: " + key)
                value = residueInfo[key]
                chainId =  value.GetResidueChainId()
                index =  value.GetResidueSequenceNumber()
                name = value.GetResidueName()
                log.debug("value: " + str(value))
                log.debug("name: " + name)
                log.debug("chainId: " + str(chainId))
                log.debug("index: " + str(index))

                neighborIndex = str(index + 1)
                nextNeighborIndex = str(index + 2)
                if "ASN" in key:
                    chain = positionsDict[chainId]
                    if chain.get(neighborIndex) != 'PRO':
                        thisName = chain.get(nextNeighborIndex)
                        log.debug("thisName: " + str(thisName))
                        if thisName in ('SER', 'THR'):
                            key += '_likely'
                            log.debug("key: " + key)

                        sasaPositions['ND2'].append(key)
            if "SER" in key or "OLS" in key:
                sasaPositions['OG'].append(key)
            if "OLT" in key or "THR" in key:
                sasaPositions['OG1'].append(key)
        log.debug("sasaPositions: \n"  + str(sasaPositions))
"""

"""
python pdbpreprocessing.py
    -amino_libs
        "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib",
        "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib",
        "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib"
    -prep
        "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep"
    -pdb
        "gmml/example/pdb/1RVZ_New.pdb"
"""
