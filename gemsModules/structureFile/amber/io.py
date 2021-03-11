#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonio
from gemsModules.project import dataio as projectio
from gemsModules.project import projectUtil as projectUtil
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class Services(str, Enum):
    evaluate = 'Evaluate'
    preprocessPdbForAmber = 'PreprocessPdbForAmber'


class PreprocessingOptions(BaseModel):
    unrecognizedAtoms : List[UnrecognizedAtom] = []
    unrecognizedMolecules : List[UnrecognizedMolecule] = []
    missingResidues : List[MissingResidue] = []
    histidineProtonations : List[HistidineProtonation] = []
    disulfideBonds : List[DisulfideBond] = []
    chainTerminations : List[ChainTermination] = []
    replacedHydrogens : List[ReplacedHydrogen] = []



## Data for the table, offers summary
## Used to be unrecognizedHeavyAtoms
class UnrecognizedAtomsTableMetadata(BaseModel):
    tableLabel : str = "Unrecognized Atoms"
    interactionRequirement : str = "none"
    urgency : str = "error"
    count : int = 0
    description: str = "Here is the description for the purpose behind the Unrecognized Atoms data."

    def __init__(self, atomCount):
        super().__init__()
        log.info("Instantiating an unrecognized atoms metadata object.")
        self.count = atomCount

##  A record of a found instance
class UnrecognizedAtom(BaseModel):
    atomIndex : str = None
    atomName : str = None
    residueName : str = None
    chainID : str = None
    residueNumber : str = None

    def __init__(self, atom):
        super().__init__()
        log.info("Instantiating an unrecognized atom.")
        self.atomIndex = atom.GetAtomSerialNumber()
        self.atomName = atom.GetAtomName()
        self.residueName = atom.GetResidueName()
        self.chainID = atom.GetResidueChainId()
        self.residueNumber = str(atom.GetResidueSequenceNumber())



## Data for the table, offers summary
def UnrecognizedMoleculesTableMetadata(BaseModel):
    tableLabel : str = "Unrecognized Molecules",
    interactionRequirement : str = "none",
    urgency : str = "warning",
    count : int = 0
    description : "Here is the description for the purpose behind the Unrecognized Residue data"

    def __init__(self, moleculeCount):
        super().__init__()
        log.info("Instantiating an unrecognized molecules metadata object.")
        self.count = moleculeCount


##  A record of a found instance
##  Used to be Unrecognized Residue
class UnrecognizedMolecule(BaseModel):
    chainID : str = None
    index : str = None
    name : str = None
    isMidChain : bool = True
    canPreprocess : bool = True

    def __init__(self, molecule):
        super().__init__()
        log.info("Instantiating an unrecognized molecule.")
        self.chainID  = molecule.GetResidueChainId()
        self.index  = molecule.GetResidueSequenceNumber()
        insertionCode = molecule.GetResidueInsertionCode()
        if "?" not in insertionCode: 
            newIndex = self.index + insertionCode
            self.index = newIndex

        self.name = molecule.GetResidueName()
        self.isMidChain = str(molecule.GetMiddleOfChain())
        ##TODO: Can we ask gmml if we canPreprocess, rather than hard coding?



## Data for the table, offers summary
def MissingResiduesTableMetadata(BaseModel):
    tableLabel : str = "Missing Residues",
    interactionRequirement : str = "optional",
    urgency : str = "warning",
    count : int = 0
    description : "Here is the description for the purpose behind the Missing Residues data"

    def __init__(self, moleculeCount):
        super().__init__()
        log.info("Instantiating an unrecognized missing residues metadata object.")
        self.count = moleculeCount


##  A record of a found instance
class MissingResidue(BaseModel):
    chainID : str = None
    startSequenceNumber : str = None
    endSequenceNumber : str = None
    residueBeforeGap : str = None
    residueAfterGap : str = None

    def __init__(self, residue):
        super().__init__()
        self.chainID = residue.GetResidueChainId()
        self.startSequenceNumber = residue.GetStartingResidueSequenceNumber()
        startInsertionCode = residue.GetStartingResidueInsertionCode()
        if "?" not in startInsertionCode:
            self.startSequenceNumber = self.startSequenceNumber + startInsertionCode

        self.endSequenceNumber = residue.GetEndingResidueSequenceNumber()
        endInsertionCode = residue.GetEndingResidueInsertionCode()
        if "?" not in endInsertionCode:
            self.endSequenceNumber = self.endSequenceNumber + endInsertionCode

        self.residueBeforeGap = residue.GetResidueBeforeGap()
        self.residueAfterGap = residue.GetResidueAfterGap()


## Data for the table, offers summary
def HistidineProtonationsTableMetadata(BaseModel):
    tableLabel : str = "Histidine Protonation",
    interactionRequirement : str = "optional",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Histidine Protonation data"

    def __init__(self, mappingCount):
        super().__init__()
        log.info("Instantiating a histidine protonations metadata object.")
        self.count = mappingCount

##  A record of a found instance
class HistidineProtonation(BaseModel):
    chainID : str = None
    residueNumber : str = None
    mappingFormat : str = None

    def __init__(self, mapping):
        super().__init__()
        self.chainID = mapping.GetResidueChainId()
        self.residueNumber = mapping.GetResidueSequenceNumber()
        insertionCode = mapping.GetResidueInsertionCode()
        if "?" not in insertionCode:
            self.residueNumber = self.residueNumber + insertionCode

        self.mappingFormat = mapping.GetStringFormatOfSelectedMapping()

## Data for the table, offers summary
def DisulfideBondTablesMetadata(BaseModel):
    tableLabel : str = "Disulfide Bonds",
    interactionRequirement : str = "optional",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Disulfide Bonds data"

    def __init__(self, bondCount):
        super().__init__()
        log.info("Instantiating a disulfide bonds metadata object.")
        self.count = bondCount


##  A record of a found instance
class DisulfideBond(BaseModel):
    residue1ChainId : str = None
    residue1Number : str = None
    residue1AmberResidueName : str = None

    residue2ChainId : str = None
    residue2Number : str = None
    residue2AmberResidueName : str = None
    distance : str = None
    bonded : bool = True

    def __init__(self, bond):
        super().__init__()
        self.residue1ChainId = bond.GetResidueChainId1()
        self.residue1Number = bond.GetResidueSequenceNumber1()
        self.residue1AmberResidueName = bond.getAmberResidueName()

        self.residue2ChainId = bond.GetResidueChainId2()
        self.residue2Number = bond.GetResidueSequenceNumber2()
        self.residue2AmberResidueName = bond.getAmberResidueName()

        self.distance = str(roundHalfUp(bond.GetDistance(), 4))
        self.bonded = bond.GetIsBonded()



## Data for the table, offers summary
def ChainTerminationsTableMetadata(BaseModel):
    tableLabel : str = "Chain Terminations",
    interactionRequirement : str = "optional",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Chain Terminations data"

    def __init__(self, teminalCount):
        super().__init__()
        log.info("Instantiating a chain terminations metadata object.")
        self.count = terminalCount

##  A record of a found instance
class ChainTermination(BaseModel):
    chainID : str = None
    startIndex : str = None
    endIndex : str = None

    def __init__(self, terminal):
        super().__init__()
        self.chainID = terminal.GetResidueChainId()
        self.startIndex = terminal.GetStartingResidueSequenceNumber()
        startInsertion = str(terminal.GetStartingResidueInsertionCode())
        if "?" not in startInsertion:
            self.startIndex = self.startIndex + startInsertion

## Data for the table, offers summary
def ReplacedHydrogensTableMetadata(BaseModel):
    tableLabel : str = "Replaced Hydrogens",
    interactionRequirement : str = "none",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Replaced Hydrogens data"

    def __init__(self, hydrogenCount):
        super().__init__()
        log.info("Instantiating a replaced hydrogens metadata object.")
        self.count = hydrogenCount

##  A record of a found instance
class ReplacedHydrogen(BaseModel):
    index : str = None
    atomName : str = None
    residueName : str = None
    chainID : str = None
    residueNumber : str = None

    def __init__(self, hydrogen):
        super().__init__()
        self.index = hydrogen.GetAtomSerialNumber()
        self.atomName = hydrogen.GetAtomName()
        self.residueName = hydrogen.GetResidueName()
        self.chainID = hydrogen.GetResidueChainId()
        self.residueNumber = hydrogen.GetResidueSequenceNumber()
        insertionCode = str(hydrogen.GetResidueInsertionCode())
        if "?" not in insertionCode:
            self.residueNumber = self.residueNumber + insertionCode


## Services
class EvaluationOutput(BaseModel):
    # PreprocessingOptions
    preprocessingOptions : PreprocessingOptions = List[Union[
            UnrecognizedAtom,
            UnrecognizedMolecule,
            MissingResidue,
            HistidineProtonation,
            DisulfideBond,
            ChainTermination,
            ReplacedHydrogen        
        ]] = None

    # Data about the tables    
    tableMetaData : TableMetaData = List[Union[
            UnrecognizedAtomsTableMetadata,
            UnrecognizedMoleculesTableMetadata,
            MissingResiduesTableMetadata,
            HistidineProtonationsTableMetadata,
            DisulfideBondsTableMetadata,
            ChainTerminationsTableMetadata,
            ReplacedHydrogensTableMetadata
        ]] = None

    def __init__(self, uploadFile):
        super().__init__()
        log.info("Intantiating a EvaluationOutput")
        aminoLibs = getDefaultAminoLibs()
        prepFile = getDefaultPrepFile()
        glycamLibs = gmml.string_vector()
        otherLibs = gmml.string_vector()
        preprocessor = gmml.PdbPreprocessor()

        ## need a pdb file object.
        try:
            log.debug("working dir: " + os.getcwd())
            pdbFileObj = gmml.PdbFile(uploadFile)
            log.debug("pdbFile: " + str(pdbFileObj))

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error

        ## need a preprocessor object.
        try:
            ### GMML's Preprocess
            preprocessor.Preprocess(pdbFile, aminoLibs, glycamLibs, otherLibs, prepFile)
        except Exception as error:
            log.error("There was a prolem creating the preprocessor object: " + str(error))
            log.error(traceback.format_exc)
            raise error

        ##UnrecognizedAtoms
        try: 
            atoms = preprocessor.GetUnrecognizedHeavyAtoms()
            if len(atoms) > 0:
                tableMetaData.append(UnrecognizedAtomsTableMetadata(len(atoms)))
                for atom in atoms:
                    unrecognizedAtom = UnrecognizedAtom(atom)
                    preprocessingOptions.append(unrecognizedAtom)

        except Exception as error:
            log.error("There was a problem evaluating unrecognized atoms: " + str(error))
            log.error(traceback.format_exc)
            raise error

        ##UnrecognizedMolecules
        try: 
            modlecules = preprocessor.GetUnrecognizedResidues()
            if len(modlecules) > 0:
                tableMetaData.append(UnrecognizedMoleculesTableMetadata(len(modlecules)))
                for molecule in modlecules:
                    unrecognizedMolecule = UnrecognizedMolecule(molecule)
                    preprocessingOptions.append(unrecognizedMolecule)
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error

        ##MissingResidues
        try: 
            residues = preprocessor.GetMissingResidues()
            if len(residues) > 0:
                tableMetaData.append(MissingResiduesTableMetadata(len(residues)))
                for residue in residues:
                    missingResidue = MissingResidue(residue)
                    preprocessingOptions.append(missingResidue)
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error

        ##HistidineProtonations
        try: 
            histidineMappings = preprocessor.GetHistidineMappings()
            if len(histidineMappings) > 0:
                tableMetaData.append(HistidineProtonationsTableMetadata(len(residues)))
                for residue in residues:
                    missingResidue = HistidineProtonation(residue)
                    preprocessingOptions.append(missingResidue)

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error

        ##DisulfideBonds
        try: 
            disulfideBonds = preprocessor.GetDisulfideBonds()
            if len(disulfideBonds) > 0:
                tableMetaData.append(DisulfideBondsTableMetadata(disulfideBonds))
                for bond in disulfideBonds:
                    disulfideBondObj = DisulfideBond(bond)
                    preprocessingOptions.append(disulfideBondObj)
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error
        ##ChainTerminations
        try: 
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error
        ##ReplacedHydrogens
        try: 
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc)
            raise error
        
        PreprocessingOptions()








class PreprocessPdbForAmberOutput(BaseModel):
    project_status : str = "submitted"
    payload : str = None
    downloadUrl : str = None


class ServiceResponse(BaseModel):
    """Holds a response from a Service requested of the Sequence Entity."""
    entity : str = "StructureFile"
    typename : Services = Field(
            'Evaluate',
            alias='type',
            title = 'Requested Service',
            description = 'The service that was requested of StructureFile Entity'
            )
    inputs : List[str] = None
    outputs: List[Union[EvaluationOutput, PreprocessPdbForAmber]] = None

    def __init__(self, serviceType: str, inputs= None, outputs = None):
        super().__init__()
        log.info("Instantiating a ServiceResponse")
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

