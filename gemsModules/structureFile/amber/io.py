#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from typing import ForwardRef
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonio
from gemsModules.common.settings import SCHEMA_DIR
from gemsModules.project import dataio as projectio
from gemsModules.project import projectUtil as projectUtil
from gemsModules.structureFile.amber.logic import*
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)



## Data for the table, offers summary
## Used to be unrecognizedHeavyAtoms
class UnrecognizedAtomsTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Unrecognized Atoms"
    tableKey : str = "unrecognizedAtoms"
    interactionRequirement : str = "none"
    urgency : str = "error"
    count : int = 0
    description: str = "The following atoms were not recognized."

    def __init__(self, atomCount):
        super().__init__()
        log.info("Instantiating an unrecognized atoms metadata object.")
        self.count = atomCount

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, atom):
        super().__init__()
        log.info("Instantiating an unrecognized atom.")
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


## Data for the table, offers summary
##  Used to be unrecognizedResidues
class UnrecognizedMoleculesTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Unrecognized Molecules"
    tableKey : str = "unrecognizedMolecules"
    interactionRequirement : str = "none"
    urgency : str = "warning"
    count : int = 0
    description : str = "The following unrecognized residues were found. They must be deleted (for you to use this site). If Mid-Chain is False, no further action is required. Otherwise, pleaseinspect the missing residues (see Missing Residues table) to choose how we should handle the new chain termini that are created by removing these residues."

    def __init__(self, moleculeCount, urgencyLevel):
        super().__init__()
        log.info("Instantiating an unrecognized molecules metadata object.")
        self.count = moleculeCount
        self.urgency = urgencyLevel

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, molecule):
        super().__init__()
        log.info("Instantiating an unrecognized molecule.")
        self.chainID  = molecule.GetResidueChainId()
        self.index  = str(molecule.GetResidueSequenceNumber())
        insertionCode = molecule.GetResidueInsertionCode()
        if "?" not in insertionCode: 
            newIndex = self.index + insertionCode
            self.index = newIndex

        self.name = molecule.GetResidueName()
        self.isMidChain = str(molecule.GetMiddleOfChain())
        ##TODO: Can we ask gmml if we canPreprocess, rather than hard coding?

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


## Data for the table, offers summary
class MissingResiduesTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Missing Residues"
    tableKey : str = "missingResidues"
    interactionRequirement : str = "optional"
    urgency : str = "warning"
    count : int = 0
    description : str = "Gaps were detected."

    def __init__(self, moleculeCount):
        super().__init__()
        log.info("Instantiating an unrecognized missing residues metadata object.")
        self.count = moleculeCount

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, residue):
        super().__init__()
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


## Data for the table, offers summary
class HistidineProtonationsTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Histidine Protonations"
    tableKey : str = "histidineProtonations"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Choose HIS mappings."

    def __init__(self, mappingCount):
        super().__init__()
        log.info("Instantiating a histidine protonations metadata object.")
        self.count = mappingCount

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, mapping):
        super().__init__()
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


## Data for the table, offers summary
class DisulfideBondsTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Disulfide Bonds"
    tableKey : str = "disulfideBonds"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Select disulfide bonds."

    def __init__(self, bondCount):
        super().__init__()
        log.info("Instantiating a disulfide bonds metadata object.")
        self.count = bondCount

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, bond):
        super().__init__()
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


def getAmberResidueName(item):
    log.info("getAmberResidueName() was called.")
    ### TODO: Replace this dummy gems method with gmml logic.
    amberResidueName = ""
    if item.GetIsBonded():
        amberResidueName = "CYX"
    else:
        amberResidueName = "CYS"

    return amberResidueName

## Data for the table, offers summary
class ChainTerminationsTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Chain Terminations"
    tableKey : str = "chainTerminations"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Select terminal residues."

    def __init__(self, terminalCount):
        super().__init__()
        log.info("Instantiating a chain terminations metadata object.")
        self.count = terminalCount

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, terminal):
        super().__init__()
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
class ReplacedHydrogensTableMetadata(BaseModel):
    app : str = "pdb"
    page : str = "options"
    tableLabel : str = "Replaced Hydrogens"
    tableKey : str = "replacedHydrogens"
    interactionRequirement : str = "none"
    urgency : str = "info"
    count : int = 0
    description : str = "The following atoms were removed..."

    def __init__(self, hydrogenCount):
        super().__init__()
        log.info("Instantiating a replaced hydrogens metadata object.")
        self.count = hydrogenCount

    def __str__(self):
        result = super().__str__()
        result = result + "\ntableLabel: " + self.tableLabel
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

    def __init__(self, hydrogen):
        super().__init__()
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


## Services
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
        ]] = []

    # Data about the tables    
    tableMetadata : List[Union[
            UnrecognizedAtomsTableMetadata,
            UnrecognizedMoleculesTableMetadata,
            MissingResiduesTableMetadata,
            HistidineProtonationsTableMetadata,
            DisulfideBondsTableMetadata,
            ChainTerminationsTableMetadata,
            ReplacedHydrogensTableMetadata
        ]] = []

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
            log.error(traceback.format_exc())
            raise error

        ## need a preprocessor object.
        try:
            ### GMML's Preprocess
            preprocessor.Preprocess(pdbFileObj, aminoLibs, glycamLibs, otherLibs, prepFile)
        except Exception as error:
            log.error("There was a prolem preprocessing the input: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##UnrecognizedAtoms
        try: 
            atoms = preprocessor.GetUnrecognizedHeavyAtoms()
            if len(atoms) > 0:
                metadata = UnrecognizedAtomsTableMetadata(len(atoms))
                log.debug("metadata: " + str(type(metadata)))
                self.tableMetadata.append(metadata)
                unrecognizedAtoms = []

                for atom in atoms:
                    unrecognizedAtomObj = UnrecognizedAtom(atom)
                    unrecognizedAtoms.append(unrecognizedAtomObj)
                
                self.preprocessingOptions.append({"unrecognizedAtoms": unrecognizedAtoms})

        except Exception as error:
            log.error("There was a problem evaluating unrecognized atoms: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##UnrecognizedMolecules
        ##  Used to be unrecognizedResidues
        try: 
            modlecules = preprocessor.GetUnrecognizedResidues()
            if len(modlecules) > 0:
                urgencyLevel = "warning"
                unrecognizedMolecules = []
                for molecule in modlecules:
                    unrecognizedMoleculeObj = UnrecognizedMolecule(molecule)
                    unrecognizedMolecules.append(unrecognizedMoleculeObj)
                    if unrecognizedMoleculeObj.isMidChain:
                        urgencyLevel = "error"

                self.preprocessingOptions.append({"unrecognizedMolecules" : unrecognizedMolecules})
                metadata = UnrecognizedMoleculesTableMetadata(len(modlecules), urgencyLevel)
                self.tableMetadata.append(metadata)
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##MissingResidues
        try: 
            residues = preprocessor.GetMissingResidues()
            if len(residues) > 0:
                self.tableMetadata.append(MissingResiduesTableMetadata(len(residues)))
                missingResidues = []
                for residue in residues:
                    missingResidueObj = MissingResidue(residue)
                    missingResidues.append(missingResidueObj)

                self.preprocessingOptions.append({"missingResidues" : missingResidues})
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##HistidineProtonations
        try: 
            histidineMappings = preprocessor.GetHistidineMappings()
            if len(histidineMappings) > 0:
                self.tableMetadata.append( HistidineProtonationsTableMetadata(len(histidineMappings)))
                histidineProtonations = []
                for mapping in histidineMappings:
                    mappingObj = HistidineProtonation(mapping)
                    histidineProtonations.append(mappingObj)
                
                self.preprocessingOptions.append({"histidineProtonations" : histidineProtonations})

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

        ##DisulfideBonds
        try: 
            disulfideBonds = preprocessor.GetDisulfideBonds()
            if len(disulfideBonds) > 0:
                self.tableMetadata.append(DisulfideBondsTableMetadata(len(disulfideBonds)))
                disulfides = []
                for bond in disulfideBonds:
                    disulfideBondObj = DisulfideBond(bond)
                    disulfides.append(disulfideBondObj)

                self.preprocessingOptions.append({"disulfideBonds" : disulfides})

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error
        ##ChainTerminations
        try: 
            chainTerminations = preprocessor.GetChainTerminations()
            if len(chainTerminations) > 0:
                self.tableMetadata.append(ChainTerminationsTableMetadata(len(chainTerminations)))
                terminations = []
                for terminal in chainTerminations:
                    terminalObj = ChainTermination(terminal)
                    terminations.append(terminalObj)

                self.preprocessingOptions.append({"chainTerminations" : terminations})

        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error
        ##ReplacedHydrogens
        try: 
            replacedHydrogens = preprocessor.GetReplacedHydrogens()
            if len(replacedHydrogens) > 0:
                self.tableMetadata.append(ReplacedHydrogensTableMetadata(len(replacedHydrogens)))
                hydrogens = []
                for hydrogen in replacedHydrogens:
                    hydrogenObj = ReplacedHydrogen(hydrogen)
                    hydrogens.append(hydrogenObj)

                self.preprocessingOptions.append({"replacedHydrogens" : hydrogens})
            
        except Exception as error:
            log.error("There was a problem creating the pdbFile object from the uploaded pdb file: " + str(error))
            log.error(traceback.format_exc())
            raise error

    def __str__(self):
        result = super().__str__()
        result = result + "\npreprocessingOptions:"
        for option in self.preprocessingOptions:
            result = result + "\n\t" + str(type(self)) + " option: " + str(option)
            
        result = result + "\ntableMetadata:"
        for table in self.tableMetadata:
            result = result + "\n\ttable:" + str(table)
        return result
        

class PreprocessPdbForAmberOutput(BaseModel):
    project_status : str = "submitted"
    payload : str = None
    downloadUrl : str = None

    ##TODO: needs an init


class StructureFileInputs(BaseModel):
    pdb_file_name : str = ""
    pdb_ID : str = ""

class StructureFileOutputs(BaseModel):
    structureFileEvaluationOutput : EvaluationOutput = None 



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


class StructureFileService(commonio.Service):
    typename : StructureFileServices = Field(
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


class StructureFileEntity(commonio.Entity):
    entityType : str = Field(
        settings.WhoIAm,
        title='Type',
        alias='type'
    )
    services : Dict[str, StructureFileService] = {}
    inputs : StructureFileInputs =  {}
    outputs : StructureFileOutputs =  None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a structureFileEntity")
        log.debug("entityType: " + self.entityType)


class structureFileTransactionSchema(commonio.TransactionSchema):
    entity : StructureFileEntity = None

    def __init__(self, **data : Any):
        super().__init__(**data)


class Transaction(commonio.Transaction):
    transaction_in : structureFileTransactionSchema 
    transaction_out : structureFileTransactionSchema

    def populate_transaction_in(self):
        log.info("structureFile Transaction populate_transaction_in() was called.")
        log.debug("self.request_dict: " )
        prettyPrint(self.request_dict)
        self.transaction_in = structureFileTransactionSchema(**self.request_dict)

        self.initialize_transaction_out_from_transaction_in() 

    def initialize_transaction_out_from_transaction_in(self) :
        log.info("structureFile - Transaction.initialize_transaction_out_from_transaction_in was called")
        self.transaction_out=self.transaction_in.copy(deep=True)
        log.debug("The transaction_out is: " )
        log.debug(self.transaction_out.json(indent=2))

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
        
        filePath = os.path.join(moduleSchemaDir, 'unrecognizedAtomsTableMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedAtomsTableMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'unrecognizedAtomSchema.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedAtom.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'unrecognizedMoleculesTableMetadata.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedMoleculesTableMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'unrecognizedMoleculeSchema.json')
        with open(filePath, 'w') as file:
            file.write(UnrecognizedMolecule.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'missingResiduesTableMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(MissingResiduesTableMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'missingResidueSchema.json')
        with open(filePath, 'w') as file:
            file.write(MissingResidue.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'histidineProtonationsTableMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(HistidineProtonationsTableMetadata.schema_json(indent=spaceCount))
 
        filePath = os.path.join(moduleSchemaDir, 'histidineProtonationSchema.json')
        with open(filePath, 'w') as file:
            file.write(HistidineProtonation.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'disulfideBondsTableMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(DisulfideBondsTableMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'disulfideBondSchema.json')
        with open(filePath, 'w') as file:
            file.write(DisulfideBond.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'chainTerminationsTableMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(ChainTerminationsTableMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'chainTerminationSchema.json')
        with open(filePath, 'w') as file:
            file.write(ChainTermination.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'replacedHydrogensTableMetadataSchema.json')
        with open(filePath, 'w') as file:
            file.write(ReplacedHydrogensTableMetadata.schema_json(indent=spaceCount))

        filePath = os.path.join(moduleSchemaDir, 'replacedHydrogenSchema.json')
        with open(filePath, 'w') as file:
            file.write(ReplacedHydrogen.schema_json(indent=spaceCount))   

    except Exception as error:
        log.error("There was a problem writing the structureFile schema to file: " + str(error))
        log.error(traceback.format_exc())
        raise error


if __name__ == "__main__":
  generateSchemaForWeb()
