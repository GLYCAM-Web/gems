#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from typing import ForwardRef
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonIO
from gemsModules.common.logic import prettyPrint
from gemsModules.common.settings import SCHEMA_DIR
from gemsModules.common.services import roundHalfUp
from gemsModules.project import io as projectIO
from gemsModules.project import projectUtil as projectUtil
from gemsModules.structureFile import settings as structureFileSettings
from gemsModules.structureFile.amber import settings as amberSettings
import gmml, traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)



def getAmberResidueName(item):
    log.info("getAmberResidueName() was called.")
    ### TODO: Replace this dummy gems method with gmml logic.
    amberResidueName = ""
    if item.GetIsBonded():
        amberResidueName = "CYX"
    else:
        amberResidueName = "CYS"

    return amberResidueName

## summary data
## Used to be unrecognizedHeavyAtoms
class UnrecognizedAtomsMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Unrecognized Atoms"
    tableKey : str = "unrecognizedAtoms"
    interactionRequirement : str = "none"
    urgency : str = "error"
    count : int = 0
    description: str = "The following atoms were not recognized."

    def setAtomCount(self, atomCount):
        log.info("setAtomCount() was called.")
        self.count = atomCount

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result




##  A record of a found instance
class UnrecognizedAtom(BaseModel):
    app : str = "pdb"
    page : str = "options"
    atomIndex : str = None
    atomName : str = None
    residueName : str = None
    chainID : str = None
    residueNumber : str = None

    def loadAtom(self, atom):
        log.info("loadAtom() was called.")
        self.atomIndex = str(atom.GetAtomSerialNumber())
        self.atomName = atom.GetAtomName()
        self.residueName = atom.GetResidueName()
        self.chainID = atom.GetResidueChainId()
        self.residueNumber = str(atom.GetResidueSequenceNumber())


    def __str__(self):
        result = super().__str__()
        result = result + "\natomIndex: " + self.atomIndex
        result = result + "\natomName: " + self.atomName
        result = result + "\nresidueName: " + self.residueName
        result = result + "\nchainID: " + self.chainID
        result = result + "\nresidueNumber: " + self.residueNumber
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


## summary data
##  Used to be unrecognizedResidues
class UnrecognizedMoleculesMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Unrecognized Molecules"
    tableKey : str = "unrecognizedMolecules"
    interactionRequirement : str = "none"
    urgency : str = "warning"
    count : int = 0
    description : str = "The following unrecognized residues were found. They must be deleted (for you to use this site). If Mid-Chain is False, no further action is required. Otherwise, pleaseinspect the missing residues (see Missing Residues table) to choose how we should handle the new chain termini that are created by removing these residues."

    def loadUnrecognizedMoleculeMetadata(self, moleculeCount, urgencyLevel):
        log.info("loadUnrecognizedMoleculeMetadata() was called.")
        self.count = moleculeCount
        self.urgency = urgencyLevel

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


##  A record of a found instance
##  Used to be Unrecognized Residues
class UnrecognizedMolecule(BaseModel):
    app : str = "pdb"
    page : str = "options"
    chainID : str = None
    index : str = None
    name : str = None
    isMidChain : bool = True
    canPreprocess : bool = True

    def loadUnrecognizedMolecule(self, molecule):
        log.info("loadUnrecognizedMolecule() was called.")
        self.chainID  = molecule.GetResidueChainId()
        self.index  = str(molecule.GetResidueSequenceNumber())
        insertionCode = molecule.GetResidueInsertionCode()
        if "?" not in insertionCode: 
            newIndex = self.index + insertionCode
            self.index = newIndex

        self.name = molecule.GetResidueName()
        self.isMidChain = str(molecule.GetMiddleOfChain())

    def __str__(self):
        result = super().__str__()
        result = result + "\nchainID: " + self.chainID
        result = result + "\nindex: " + self.index
        result = result + "\nname: " + self.name
        result = result + "\nisMidChain: " + self.isMidChain
        result = result + "\ncanPreprocess: " + str(self.canPreprocess)
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


## summary data
class MissingResiduesMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Missing Residues"
    tableKey : str = "missingResidues"
    interactionRequirement : str = "optional"
    urgency : str = "warning"
    count : int = 0
    description : str = "Gaps were detected."

    def setMoleculeCount(self, moleculeCount):
        log.info("setMoleculeCount() was called.")
        self.count = moleculeCount

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


##  A record of a found instance
class MissingResidue(BaseModel):
    app : str = "pdb"
    page : str = "options"
    chainID : str = None
    startSequenceNumber : str = None
    endSequenceNumber : str = None
    residueBeforeGap : str = None
    residueAfterGap : str = None

    def loadMissingResidue(self, residue):
        log.info("loadMissingResidue() was called.")
        self.chainID = residue.GetResidueChainId()
        self.startSequenceNumber = str(residue.GetStartingResidueSequenceNumber())
        startInsertionCode = residue.GetStartingResidueInsertionCode()
        if "?" not in startInsertionCode:
            self.startSequenceNumber = self.startSequenceNumber + startInsertionCode

        self.endSequenceNumber = str(residue.GetEndingResidueSequenceNumber())
        endInsertionCode = residue.GetEndingResidueInsertionCode()
        if "?" not in endInsertionCode:
            self.endSequenceNumber = self.endSequenceNumber + endInsertionCode

        self.residueBeforeGap = str(residue.GetResidueBeforeGap())
        self.residueAfterGap = str(residue.GetResidueAfterGap())

    def __str__(self):
        result = super().__str__()
        result = result + "\nchainID: " + self.chainID
        result = result + "\nstartSequenceNumber: " + self.startSequenceNumber
        result = result + "\nendSequenceNumber: " + self.endSequenceNumber
        result = result + "\nresidueBeforeGap: " + self.residueBeforeGap
        result = result + "\nresidueAfterGap: " + self.residueAfterGap
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


## summary data
class HistidineProtonationsMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Histidine Protonations"
    tableKey : str = "histidineProtonations"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Choose HIS mappings."

    def setMappingCount(self, mappingCount):
        log.info("setMappingCount() was called")
        self.count = mappingCount

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


##  A record of a found instance
class HistidineProtonation(BaseModel):
    app : str = "pdb"
    page : str = "options"
    chainID : str = None
    residueNumber : str = None
    mappingFormat : str = None

    def loadHistidineProtonation(self, mapping):
        log.info("loadHistidineProtonation() was called.")
        self.chainID = mapping.GetResidueChainId()
        self.residueNumber = str(mapping.GetResidueSequenceNumber())
        insertionCode = mapping.GetResidueInsertionCode()
        if "?" not in insertionCode:
            self.residueNumber = self.residueNumber + insertionCode

        self.mappingFormat = mapping.GetStringFormatOfSelectedMapping()

    def __str__(self):
        result = super().__str__()
        result = result + "\nchainID: " + self.chainID
        result = result + "\nresidueNumber: " + self.residueNumber
        result = result + "\nmappingFormat: " + self.mappingFormat
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


## summary data
class DisulfideBondsMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Disulfide Bonds"
    tableKey : str = "disulfideBonds"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Select disulfide bonds."

    def setBondCount(self, bondCount):
        log.info("setBondCount() was called.")
        self.count = bondCount

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result



##  A record of a found instance
class DisulfideBond(BaseModel):
    app : str = "pdb"
    page : str = "options"
    residue1ChainId : str = None
    residue1Number : str = None
    residue1AmberResidueName : str = None

    residue2ChainId : str = None
    residue2Number : str = None
    residue2AmberResidueName : str = None
    distance : str = None
    bonded : bool = True

    def loadDisulfideBond(self, bond):
        log.info("loadDisulfideBond() was called: ")
        self.residue1ChainId = bond.GetResidueChainId1()
        self.residue1Number = str(bond.GetResidueSequenceNumber1())
        self.residue1AmberResidueName = getAmberResidueName(bond)

        self.residue2ChainId = bond.GetResidueChainId2()
        self.residue2Number = str(bond.GetResidueSequenceNumber2())
        self.residue2AmberResidueName = getAmberResidueName(bond)

        self.distance = str(roundHalfUp(bond.GetDistance(), 4))
        self.bonded = bond.GetIsBonded()

    def __str__(self):
        result = super().__str__()
        result = result + "\nresidue1ChainId: " + self.residue1ChainId
        result = result + "\nresidue1Number: " + self.residue1Number
        result = result + "\nresidue1AmberResidueName: " + self.residue1AmberResidueName
        result = result + "\nresidue2ChainId: " + self.residue2ChainId
        result = result + "\nresidue2Number: " + self.residue2Number
        result = result + "\nresidue2AmberResidueName: " + self.residue2AmberResidueName
        result = result + "\ndistance: " + self.distance
        result = result + "\nbonded: " + str(self.bonded)
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result



## Data for the table, offers summary
class ChainTerminationsMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Chain Terminations"
    tableKey : str = "chainTerminations"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Select terminal residues."

    def setTerminalCount(self, terminalCount):
        log.info("setTerminalCount() was called.")
        self.count = terminalCount

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


##  A record of a found instance
class ChainTermination(BaseModel):
    app : str = "pdb"
    page : str = "options"
    chainID : str = None
    startIndex : str = None
    endIndex : str = None

    def loadChainTermination(self, terminal):
        log.info("loadChainTermination() was called.")
        self.chainID = terminal.GetResidueChainId()
        self.startIndex = str(terminal.GetStartingResidueSequenceNumber())
        startInsertion = str(terminal.GetStartingResidueInsertionCode())
        if "?" not in startInsertion:
            self.startIndex = self.startIndex + startInsertion

        self.endIndex = str(terminal.GetEndingResidueSequenceNumber())
        endInsertionCode = terminal.GetEndingResidueInsertionCode()
        if "?" not in endInsertionCode:
            self.endIndex = self.endIndex + endInsertionCode

    def __str__(self):
        result = super().__str__()
        result = result + "\nchainID: " + self.chainID
        result = result + "\nstartIndex: " + self.startIndex
        result = result + "\nendIndex: " + self.endIndex
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


## Data for the table, offers summary
class ReplacedHydrogensMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    label : str = "Replaced Hydrogens"
    tableKey : str = "replacedHydrogens"
    interactionRequirement : str = "none"
    urgency : str = "info"
    count : int = 0
    description : str = "The following atoms were removed..."

    def setHydrogenCount(self, hydrogenCount):
        log.info("setHydrogenCount() was called")
        self.count = hydrogenCount

    def __str__(self):
        result = super().__str__()
        result = result + "\nlabel: " + self.label
        result = result + "\ntableKey: " + self.tableKey
        result = result + "\ninteractionRequirement: " + self.interactionRequirement
        result = result + "\nurgency: " + self.urgency
        result = result + "\ncount: " + str(self.count)
        result = result + "\ndescription: " + self.description
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result


##  A record of a found instance
class ReplacedHydrogen(BaseModel):
    app : str = "pdb"
    page : str = "options"
    index : str = None
    atomName : str = None
    residueName : str = None
    chainID : str = None
    residueNumber : str = None

    def loadReplacedHydrogen(self, hydrogen):
        log.info("loadReplacedHydrogen() was called.")
        self.index = str(hydrogen.GetAtomSerialNumber())
        self.atomName = hydrogen.GetAtomName()
        self.residueName = hydrogen.GetResidueName()
        self.chainID = hydrogen.GetResidueChainId()
        self.residueNumber = str(hydrogen.GetResidueSequenceNumber())
        insertionCode = str(hydrogen.GetResidueInsertionCode())
        if "?" not in insertionCode:
            self.residueNumber = self.residueNumber + insertionCode

    def __str__(self):
        result = super().__str__()
        result = result + "\nindex: " + self.index
        result = result + "\natomName: " + self.atomName
        result = result + "\nresidueName: " + self.residueName
        result = result + "\nchainID: " + str(self.chainID)
        result = result + "\nresidueNumber: " + self.residueNumber
        result = result + "\napp: " + self.app
        result = result + "\npage: " + self.page
        return result

class Evaluator:
    aminoLibs : gmml.string_vector = None
    prepFile : gmml.string_vector = None
    glycamLibs : gmml.string_vector = None
    otherLibs : gmml.string_vector = None
    preprocessor : gmml.PdbPreprocessor = None

    pdbFileObj : gmml.PdbFile = None

    preprocessingOptions = []
    metadata = []
    
    def load_gmml_resources(self):
        log.info("__load_gmml_resources() was called.")
        
        try:
            log.info("Evaluating a PDB file")
            self.aminoLibs = gmml.string_vector()
            self.aminoLibs.push_back(amberSettings.AMINO_LIBS)

            self.prepFile = gmml.string_vector()
            self.prepFile.push_back(amberSettings.PREP_FILE)

            self.glycamLibs = gmml.string_vector()
            self.glycamLibs.push_back(amberSettings.GLYCAM_LIBS)

            self.otherLibs = gmml.string_vector()
            self.otherLibs.push_back(amberSettings.OTHER_LIBS)

            self.preprocessor = gmml.PdbPreprocessor()
        except Exception as error:
            log.error("There was a problem loading gmml resources: " + str(error))
            log.error(traceback.format_exc())
            raise error

    ## Only meant to be used in this class. Python automatically throws an error if methods
    #   that begin with 2 underscores are called from other files.
    def __load_pdb_file(self, uploadFile):
        log.info("__load_pdb_file() was called.")
        # need a pdb file object.
        try:
            #log.debug("working dir: " + os.getcwd())
            self.pdbFileObj = gmml.PdbFile(uploadFile)
            log.debug("pdbFile: " + str(self.pdbFileObj))
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

    def doEvaluation(self, uploadFile):
        log.info("doEvaluation() was called.")
        try:
            self.load_gmml_resources()
        except Exception as error:
            log.error("There was a problem loading resources from gmml: " + str(error))
            log.error(traceback.format_exc())
            raise error
        
        try:
            self.__load_pdb_file(uploadFile)
        except Exception as error:
            log.error("There was a problem uploading the pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ## need a preprocessor object.
        try:
            log.debug("About to preprocess an unevaluated file.")
            log.debug("Evaluator: ")
            log.debug("pdbFileObj: " + str(self.pdbFileObj))

            log.debug("aminoLibs:")
            for item in self.aminoLibs:
                log.debug(str(item))
            log.debug("glycamLibs:")
            for item in self.glycamLibs:
                log.debug(str(item))
            log.debug("otherLibs:")
            for item in self.otherLibs:
                log.debug(str(item))
            log.debug("prepFile:")
            for item in self.prepFile:
                log.debug(str(item))

            ### GMML's Preprocess
            self.preprocessor.Preprocess(self.pdbFileObj, self.aminoLibs, self.glycamLibs, self.otherLibs, self.prepFile)
        except Exception as error:
            log.error("There was a prolem preprocessing the input: " + str(error))
            log.error(traceback.format_exc())
            raise error


        ##UnrecognizedAtoms
        try: 
            log.debug("unrecognized heavy atoms?")
            atoms = self.preprocessor.GetUnrecognizedHeavyAtoms()
            log.debug("atoms: " + repr(atoms))
            if len(atoms) > 0:
                unrecognizedAtomsMetadata = UnrecognizedAtomsMetadata()
                unrecognizedAtomsMetadata.setAtomCount(len(atoms))
                self.metadata.append(unrecognizedAtomsMetadata)
                unrecognizedAtoms = []

                for atom in atoms:
                    unrecognizedAtomObj = UnrecognizedAtom()
                    unrecognizedAtomObj.loadAtom(atom)
                    unrecognizedAtoms.append(unrecognizedAtomObj)
                
                self.preprocessingOptions.append({"unrecognizedAtoms": unrecognizedAtoms})

        except Exception as error:
            log.error("There was a problem evaluating unrecognized atoms: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##UnrecognizedMolecules
        ##  Used to be unrecognizedResidues
        try: 
            modlecules = self.preprocessor.GetUnrecognizedResidues()
            if len(modlecules) > 0:
                urgencyLevel = "warning"
                unrecognizedMolecules = []
                for molecule in modlecules:
                    unrecognizedMoleculeObj = UnrecognizedMolecule()
                    unrecognizedMoleculeObj.loadUnrecognizedMolecule(molecule)
                    unrecognizedMolecules.append(unrecognizedMoleculeObj)
                    if unrecognizedMoleculeObj.isMidChain:
                        urgencyLevel = "error"

                self.preprocessingOptions.append({"unrecognizedMolecules" : unrecognizedMolecules})

                unrecognizedMoleculesMetadata = UnrecognizedMoleculesMetadata()
                unrecognizedMoleculesMetadata.loadUnrecognizedMoleculeMetadata(len(modlecules), urgencyLevel)
                self.metadata.append(unrecognizedMoleculesMetadata)
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##MissingResidues
        try: 
            residues = self.preprocessor.GetMissingResidues()
            if len(residues) > 0:
                missingResiduesMetadata = MissingResiduesMetadata()
                missingResiduesMetadata.setMoleculeCount(len(residues))
                self.metadata.append(missingResiduesMetadata)

                missingResidues = []
                for residue in residues:
                    missingResidueObj = MissingResidue()
                    missingResidueObj.loadMissingResidue(residue)
                    missingResidues.append(missingResidueObj)

                self.preprocessingOptions.append({"missingResidues" : missingResidues})
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##HistidineProtonations
        try: 
            histidineMappings = self.preprocessor.GetHistidineMappings()
            if len(histidineMappings) > 0:
                histidineProtonationsMetadata = HistidineProtonationsMetadata()
                histidineProtonationsMetadata.setMappingCount(len(histidineMappings))
                self.metadata.append( histidineProtonationsMetadata )

                histidineProtonations = []
                for mapping in histidineMappings:
                    mappingObj = HistidineProtonation()
                    mappingObj.loadHistidineProtonation(mapping)
                    histidineProtonations.append(mappingObj)
                
                self.preprocessingOptions.append({"histidineProtonations" : histidineProtonations})

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##DisulfideBonds
        try: 
            disulfideBonds = self.preprocessor.GetDisulfideBonds()
            if len(disulfideBonds) > 0:
                disulfideBondsMetadata = DisulfideBondsMetadata()
                disulfideBondsMetadata.setBondCount(len(disulfideBonds))
                self.metadata.append(disulfideBondsMetadata)
                disulfides = []
                for bond in disulfideBonds:
                    disulfideBondObj = DisulfideBond()
                    disulfideBondObj.loadDisulfideBond(bond)
                    disulfides.append(disulfideBondObj)

                self.preprocessingOptions.append({"disulfideBonds" : disulfides})

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##ChainTerminations
        try: 
            chainTerminations = self.preprocessor.GetChainTerminations()
            if len(chainTerminations) > 0:
                chainTerminationsMetadata = ChainTerminationsMetadata()
                chainTerminationsMetadata.setTerminalCount(len(chainTerminations))
                self.metadata.append(chainTerminationsMetadata)
                terminations = []
                for terminal in chainTerminations:
                    terminalObj = ChainTermination()
                    terminalObj.loadChainTermination(terminal)
                    terminations.append(terminalObj)

                self.preprocessingOptions.append({"chainTerminations" : terminations})

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##ReplacedHydrogens
        try: 
            replacedHydrogens = self.preprocessor.GetReplacedHydrogens()
            if len(replacedHydrogens) > 0:
                replacedHydrogensMetadata = ReplacedHydrogensMetadata()
                replacedHydrogensMetadata.setHydrogenCount(len(replacedHydrogens))
                self.metadata.append(replacedHydrogensMetadata)
                hydrogens = []
                for hydrogen in replacedHydrogens:
                    hydrogenObj = ReplacedHydrogen()
                    hydrogenObj.loadReplacedHydrogen(hydrogen)
                    hydrogens.append(hydrogenObj)

                self.preprocessingOptions.append({"replacedHydrogens" : hydrogens})
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        evaluationData = {
            'preprocessingOptions' : self.preprocessingOptions,
            'metadata' : self.metadata
        }

        try:
            log.debug("evaluationData obj type: " + str(type(evaluationData)))
            log.debug("evaluationData: " + repr(evaluationData))
            evaluationOutput = EvaluationOutput()
            evaluationOutput.loadEvaluationOutput(evaluationData)
            return evaluationOutput
        except Exception as error:
            log.error("There was a problem instantiating an EvaluationOutput obj: " + str(error))
            log.error(traceback.format_exc())
            raise error

## Services
##  @brief This should only be instantiated after uploading/sideloading is finished.
class EvaluationOutput(BaseModel):
    # PreprocessingOptions
    preprocessingOptions : List[Union[
            UnrecognizedAtom,
            UnrecognizedMolecule,
            MissingResidue,
            HistidineProtonation,
            DisulfideBond,
            ChainTermination,
            ReplacedHydrogen        
        ]] = None

    # Data about the tables    
    metadata : List[Union[
            UnrecognizedAtomsMetadata,
            UnrecognizedMoleculesMetadata,
            MissingResiduesMetadata,
            HistidineProtonationsMetadata,
            DisulfideBondsMetadata,
            ChainTerminationsMetadata,
            ReplacedHydrogensMetadata
        ]] = None

    def loadEvaluationOutput(self, data):
        log.debug("loadEvaluationOutput was called.")
        self.preprocessingOptions = data['preprocessingOptions']
        self.metadata = data['metadata']  

    def __str__(self):
        result = super().__str__()
        result = result + "\npreprocessingOptions:"
        for option in self.preprocessingOptions:
            result = result + "\n\t" + str(type(self)) + " option: " + str(option)
            
        result = result + "\nmetadata:"
        for table in self.metadata:
            result = result + "\n\ttable:" + str(table)
        return result
        

class PreprocessPdbForAmberOutput(BaseModel):
    project_status : str = "submitted"
    payload : str = None
    downloadUrl : str = None

class StructureFileInputs(BaseModel):
    pdb_file_name : str = ""
    pdb_ID : str = ""

class StructureFileOutputs(BaseModel):
    evaluationOutput : EvaluationOutput = None 

class StructureFileResponse(BaseModel):
    typename : str = Field(
            None,
            title='Responding Service.',
            alias='type',
            description='The type service that produced this response.'
            )
    inputs : StructureFileInputs = None
    outputs : StructureFileOutputs = None
    # notices : List[Notice] = None

    def __init__(self, serviceType: str, inputs= None, outputs = None):
        super().__init__()
        log.info("Instantiating a StructureFileSchemaResponse")
        log.debug("serviceType: " + serviceType)

        self.typename = serviceType
        if not inputs == None:
            if self.inputs == None:
                self.inputs = []
            for input in inputs:
                self.inputs.append(input)
        if not outputs == None:
            if self.outputs == None:
                self.outputs = []
            for output in outputs:
                self.outputs.append(output)


class StructureFileService(commonIO.Service):
    typename : structureFileSettings.Services = Field(
        'Evaluate',
        alias='type',
        title = 'Requested Service',
        description = 'The service that was requested of StructureFile Entity'
    )
    

    def __init__(self, **data : Any):
        super().__init__()
        log.info("Initializing Service.")
        log.debug("the data " + repr(self))
        log.debug("Init for the Services in StructureFile was called.")


class StructureFileEntity(commonIO.Entity):
    entityType : str = Field(
        structureFileSettings.WhoIAm,
        title='Type',
        alias='type'
    )
    services : Dict[str, StructureFileService] = {}
    inputs : StructureFileInputs =  {}
    outputs : StructureFileOutputs =  None
    

    # def __init__(self, **data: Any):
    #     super().__init__(**data)
    #     log.info("Instantiating a structureFileEntity")
    #     log.debug("entityType: " + self.entityType)


## @brief Override TransactionSchema, setting this entity to StructureFile
class StructureFileTransactionSchema(commonIO.TransactionSchema):
    entity : StructureFileEntity = ...
    project : projectIO.PdbProject = None

    def __init__(self, **data : Any):
        super().__init__(**data)

##  @brief Transactions for PDB Preprocessing.
##  @detail Transaction schema contains entity, options, notices, and projects
class PdbTransaction(commonIO.Transaction):
    transaction_in : StructureFileTransactionSchema 
    transaction_out : StructureFileTransactionSchema

    def populate_transaction_in(self):
        log.info("Populating transaction_in for a PdbTransaction:")
        self.transaction_in = StructureFileTransactionSchema(**self.request_dict)
        log.debug("The transaction_in is: " )
        log.debug(self.transaction_in.json(indent=2))
        


    # ## @brief Copies request input into transaction object, before providing services
    # def populate_transaction_in(self):
    #     log.info("structureFile Transaction populate_transaction_in() was called.")
    #     ##The following debug lines are also sometimes useful, but normally redundant.
    #     #log.debug("self.request_dict: " )
    #     #prettyPrint(self.request_dict)
    #     self.transaction_in = StructureFileTransactionSchema(**self.request_dict)

    #     self.initialize_transaction_out_from_transaction_in() 

    ## @brief Gets started on the output, before providing services.
    def initialize_transaction_out_from_transaction_in(self) :
        log.info("initialize_transaction_out_from_transaction_in() was called.")
        try:
            self.transaction_out=self.transaction_in.copy(deep=True)
            log.debug("The transaction_out is: " )
            log.debug(self.transaction_out.json(indent=2))
        except Exception as error:
            log.error("There was a problem copying transaction in into transaction out: " + str(error))
            log.error(traceback.format_exc())
            raise error


    def createStructureFileResponse(self, serviceType, inputs, outputs):
        log.info("createStructureFileResponse() was called.")
        log.debug("self.transaction")
        self.transaction_out.entity.outputs.append(StructureFileResponse(serviceType, inputs, outputs))

    
    def build_outgoing_string(self) :
        log.info("build_outgoing_string() was called.")
        
        if self.transaction_out.prettyPrint is True : 
            self.outgoing_string = self.transaction_out.json(indent=2)
        else :
            self.outgoing_string = self.transaction_out.json()

        log.debug("self.outgoing_string: " + self.outgoing_string)



def generateSchemaForWeb():
    log.info("generateSchemaForWeb() was called.")
    spaceCount=2
    log.debug("SCHEMA_DIR: " + SCHEMA_DIR)
    moduleSchemaDir = os.path.join(SCHEMA_DIR, "structureFile")

    try:
        if not os.path.isdir(moduleSchemaDir):
            os.makedirs(moduleSchemaDir)
        
        filePath = os.path.join(moduleSchemaDir, 'unrecognizedAtomsMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedAtomsMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'unrecognizedAtomSchema.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedAtom.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'unrecognizedMoleculesMetadata.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedMoleculesMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'unrecognizedMoleculeSchema.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedMolecule.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'missingResiduesMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(MissingResiduesMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'missingResidueSchema.json')
        with open(filePath, 'w') as file:
            file.write(MissingResidue.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'histidineProtonationsMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(HistidineProtonationsMetadata.schema_json(indent=spaceCount))
 
        filePath = os.path.join(moduleSchemaDir, 'histidineProtonationSchema.json')
        with open(filePath, 'w') as file:
            file.write(HistidineProtonation.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'disulfideBondsMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(DisulfideBondsMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'disulfideBondSchema.json')
        with open(filePath, 'w') as file:
            file.write(DisulfideBond.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'chainTerminationsMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(ChainTerminationsMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'chainTerminationSchema.json')
        with open(filePath, 'w') as file:
            file.write(ChainTermination.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'replacedHydrogensMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(ReplacedHydrogensMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'replacedHydrogenSchema.json')
        with open(filePath, 'w') as file:
            file.write(ReplacedHydrogen.schema_json(indent=spaceCount))   

    except Exception as error:
        log.error("There was a problem writing the structureFile schema to file: " + str(error))
        log.error(traceback.format_exc())
        raise error


if __name__ == "__main__":
  generateSchemaForWeb()
