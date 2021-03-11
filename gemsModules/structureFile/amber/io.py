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
class UnrecognizedAtomsTableMetadata(BaseModel):
    tableLabel : str = "Unrecognized Atoms"
    interactionRequirement : str = "none"
    urgency : str = "error"
    count : int = 0
    description: str = "Here is the description for the purpose behind the Unrecognized Atoms data."

##  A record of a found instance
class UnrecognizedAtom(BaseModel):
    atomIndex : str = None
    atomName : str = None
    residueName : str = None
    chainID : str = None
    residueNumber : str = None


## Data for the table, offers summary
def UnrecognizedMoleculeTableMetadata(BaseModel):
    tableLabel : str = "Unrecognized Molecules",
    interactionRequirement : str = "none",
    urgency : str = "warning",
    count : int = 0
    description : "Here is the description for the purpose behind the Unrecognized Residue data"

##  A record of a found instance
class UnrecognizedMolecule(BaseModel):
    chainID : str = None
    index : str = None
    name : str = None
    isMidChain : bool = True
    canPreprocess : str = None

## Data for the table, offers summary
def MissingResidueTableMetadata(BaseModel):
    tableLabel : str = "Missing Residues",
    interactionRequirement : str = "optional",
    urgency : str = "warning",
    count : int = 0
    description : "Here is the description for the purpose behind the Missing Residues data"

##  A record of a found instance
class MissingResidue(BaseModel):
    chainID : str = None
    startSequenceNumber : str = None
    endSequenceNumber : str = None
    residueBeforeGap : str = None
    residueAfterGap : str = None


## Data for the table, offers summary
def HistidineProtonationTableMetadata(BaseModel):
    tableLabel : str = "Histidine Protonation",
    interactionRequirement : str = "optional",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Histidine Protonation data"

##  A record of a found instance
class HistidineProtonation(BaseModel):
    chainID : str = None
    residueNumber : str = None
    mappingFormat : str = None


## Data for the table, offers summary
def DisulfideBondTableMetadata(BaseModel):
    tableLabel : str = "Disulfide Bonds",
    interactionRequirement : str = "optional",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Disulfide Bonds data"

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


## Data for the table, offers summary
def ChainTerminationTableMetadata(BaseModel):
    tableLabel : str = "Chain Terminations",
    interactionRequirement : str = "optional",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Chain Terminations data"

##  A record of a found instance
class ChainTermination(BaseModel):
    chainID : str = None
    startIndex : str = None
    endIndex : str = None


## Data for the table, offers summary
def ReplacedHydrogenTableMetadata(BaseModel):
    tableLabel : str = "Replaced Hydrogens",
    interactionRequirement : str = "none",
    urgency : str = "info",
    count : int = 0
    description : "Here is the description for the purpose behind the Replaced Hydrogens data"

##  A record of a found instance
class ReplacedHydrogen(BaseModel):
    index : str = None
    atomName : str = None
    residueName : str = None
    chainID : str = None
    residueNumber : str = None


## Services
class EvaluationOutput(BaseModel):
    # PreprocessingOptions
    preprocessingOptions : PreprocessingOptions = Field(
        None,
        description="A series of lists of info and options. These provide the data for the pdb preprocessor's options page."
        ) 

    def __init__(self, )


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

