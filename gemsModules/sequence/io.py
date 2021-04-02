#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
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

# ## Services
# ##
class Services(str,Enum):
    build3dStructure = 'Build3dStructure'
    drawGlycan = 'drawGlycan'
    evaluate = 'Evaluate'
    status = 'Status'

# ## Environment variables
# ##
class Environment(str,Enum):
    ## The entity itself
    sequenceentity   = 'GEMS_MODULES_SEQUENCE_PATH'
    ## Services for this entity, in alphabetical order
    build3DStructure = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'
    graph = 'GEMS_MODULES_SEQUENCE_GRAPH_PATH'
    evaluate         = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'

# ## Recognized input and output formats
# ##
class Formats(str,Enum):
    """All Sequenes must be in GLYCAM Condensed notation"""
    # the basic sequence as it might arrive, unspecified order, assumed condensed glycam
    sequence = 'Sequence'  

class Locations(str,Enum):
    internal='internal'  ##< All input at this time must be internal to the JSON object(s)

class Resource(commonio.Resource):
    Sequence : str = None
    locationType : Locations = Field(
            'internal',
            description='Supported input locations for the Service Entity.'
            )
    resourceFormat : Formats = Field(
            'GlycamCondensed',
            description='Supported input formats for the Service Entity.'
            )

class SequenceVariants(BaseModel):
    """Different representations of the sequence."""
    # condensed sequence types
    IndexOrder : str = None
    LongestChainOrder : str = None
    UserOrdered : str = None
    MonospacedTextDiagram : str = None
    # ... labeled
    IndexOrderLabeled : str = None
    LongestChainOrderLabeled : str = None
    UserOrderedLabeled : str = None
    MonospacedTextDiagramLabeled : str = None
    # other condensed sequence representations
    Suuid : str = None
    Smd5sum : str = None

class Definitions(BaseModel):
    """TODO:  write this. """
    pass

class SystemSolvationOptions(BaseModel):
    solvationStatus : str = Field(
            'Unsolvated',
            description="Unsolvated, To be solvated, Solvated, Not applicable"
            )
    ionStatus : str = Field(
            'No ions',
            description="No ions, Add ions, Contains ions."
            )

class ResidueRingPucker(BaseModel):
    puckerClassificationSystem : str = Field(
            'BFMP',
            description="The system used to identify the ring pucker (shape)."
            )

class LinkageRotamerNames(str, Enum):
    phi = 'phi'
    psi = 'psi'
    omg = 'omg'
    omega = 'omega'

class DihedralRotamers(BaseModel):
    dihedralName : str = None # phi, psi etc. Use Enum above once anything works :(
    dihedralValues : List[str] = [] # gg, -g, tg, etc

class LinkageRotamers(BaseModel): 
    indexOrderedLabel : str = None
    linkageName : str = None
    firstResidueNumber : str = None
    secondResidueNumber : str = None
    dihedralsWithOptions : List[str] = []
    possibleRotamers : List[DihedralRotamers] = []
    likelyRotamers : List[DihedralRotamers] = []

class ResidueGeometryOptions(BaseModel):
    """Geometry options for residues"""
    ringPuckers : List[ResidueRingPucker] = []

class LinkageGeometryOptions(BaseModel):
    """Geometry options for linkages"""
    linkageRotamersList : List[LinkageRotamers] = []
    totalLikelyRotamers : int = 0
    totalPossibleRotamers : int = 0

# I can't figure out if I can pass gmml classes to functions here, so I just 
# wrote getLinkageOptionsFromGmmlcbBuilder.
class GeometryOptions(BaseModel):
    residues : ResidueGeometryOptions = None # Not yet handled.
    linkages : LinkageGeometryOptions = None
    def __init__(self, validatedSequence : Sequence):
        super().__init__()
        from gemsModules.sequence import evaluate
        self.linkages = evaluate.getLinkageOptionsFromGmmlcbBuilder(validatedSequence)
        #print(self.linkages.json())

class BuildOptions(BaseModel):
    """Options for building 3D models"""
    solvationOptions : SystemSolvationOptions = None  # Not yet handled.
    geometryOptions : GeometryOptions = None
    mdMinimize : bool = Field(
            True,
            title = 'Minimize structure using MD',
            )

    def __init__(self, validatedSequence : Sequence):
        super().__init__()
        log.info("Initializing BuildOptions")
        log.debug("validatedSequence: " + validatedSequence)
        self.geometryOptions = GeometryOptions(validatedSequence)


class DrawOptions(BaseModel):
    """Options for drawing 2D models"""
    Labeled : str = "true"  ## Lachele Mar 2020 - should this be a bool?

# Oliver Oct2020 finds this unnecessary. Not sure what other is going to be.
# class SequenceInput(BaseModel):
#     other : List[Resource] = []
    
class SequenceEvaluationOutput(BaseModel):
    sequenceIsValid : bool = False
    validateOnly : bool = False
    sequenceVariants: SequenceVariants = None
    buildOptions : BuildOptions = Field(
            None,
            description="Options for building the 3D Structure of the sequence."
            )
    drawOptions : DrawOptions = Field(
            None,
            description="Options for drawing a 2D Structure of the sequence."
            )

    def __init__(self, sequence:str, validateOnly):
        super().__init__()
        log.info("Initializing SequenceOutput.")

        log.debug("sequence: " + repr(sequence))
        log.debug("validateOnly: " + repr(validateOnly))

        from gemsModules.sequence import evaluate

        self.validateOnly = validateOnly
        self.sequenceIsValid = evaluate.checkIsSequenceSane(sequence)
        log.debug("self.sequenceIsValid: " + str(self.sequenceIsValid))

        if self.sequenceIsValid:
            self.sequenceVariants = evaluate.getSequenceVariants(sequence)
        if self.sequenceIsValid and not validateOnly:
            self.buildOptions = BuildOptions(sequence)
            
            # self.defaultStructure
            #drawOptions to be developed later.


class Build3DStructureOutput(BaseModel):
    payload : str =  ""
    sequence : str  = ""
    seqID : str = ""
    conformerID : str = ""
    conformerLabel : str = ""
    subDirectory : str = ""
    downloadUrl : str = ""

    def __init__(self, payload:str, sequence:str, seqID:str, conformerID:str, conformerLabel:str):
        super().__init__()
        log.info("Initializing BuildOutput.")
        self.payload = payload
        self.sequence = sequence
        self.seqID = seqID
        self.conformerID = conformerID
        self.conformerLabel = conformerLabel
        self.subDirectory = '/Requested_Builds/' + conformerID + '/'
        #self.downloadUrl = downloadUrl
        self.downloadUrl = projectUtil.getDownloadUrl(payload, "cb", self.conformerID)

        log.debug("payload(projectID): " + self.payload)
        log.debug("sequence: " + self.sequence)
        log.debug("seqID: " + self.seqID)
        log.debug("conformerID: " + self.conformerID)
        log.debug("conformerLabel: " + self.conformerID)
        log.debug("subDirectory: " + self.subDirectory)
        log.debug("downloadUrl: " + self.downloadUrl)


class Service(commonio.Service):
    """Holds information about a Service requested of the Sequence Entity."""
    typename : Services = Field( 
        'Evaluate', 
        alias = 'type', 
        title = 'Requested Service', 
        description = 'The service requested of the Sequence Entity'
        )
    project: projectio.Project = None
    inputs : List[str] = None ##TODO: Make a CondensedSequence class.
    outputs : List[Union[SequenceEvaluationOutput, Build3DStructureOutput]] = None

    def __init__(self, config : dict ):
        super().__init__()

        log.info("Initializing Service.")
        log.debug("config: " + repr(config))

        if self.inputs is None:
            self.inputs = []
        self.inputs.append(config['sequence'])

        if self.outputs == None:
            self.outputs = []

        if config['outputType'] == "Evaluate":
            output = SequenceOutput(config)
            self.outputs.append(output)
        elif config['outputType'] == "Build3DStructure":
            output1 = SequenceOutput(config)
            self.outputs.append(output1)
            output2 = BuildOutput(config)
            self.outputs.append(output2)

## This is a Response and should be called that, and based on Service (Lachele)
class Response(Service):
    """Holds a response from a Service requested of the Sequence Entity."""
    entity : str = "Sequence"
    typename : Services = Field(
            'Evaluate',
            alias='type',
            title = 'Requested Service',
            description = 'The service that was requested of Sequence Entity'
            )
    inputs : List[str] = None
    outputs: List[Union[SequenceEvaluationOutput, Build3DStructureOutput]] = None

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



class Entity(commonio.Entity):
    """Holds information about the main object responsible for a service."""
   
    entityType : str = Field(
            'Sequence',
            title='Type',
            alias='type'
            )
    services : List[Service] = []
    responses : List[Response] = []

    def __init__(self, **data: Any):
        super().__init__(**data)

#    @validator('entityType')
#    def must_be_sequence(cls,v):
#        if v is not 'sequence':
#            pass
#        ## but really call common servicer to whine and exit
#        ## .... what abou sub-entities?  


class TransactionSchema(commonio.TransactionSchema):
    """
    Holds info about the Transaction JSON object used in the Sequence entity.
    """
    entity : Entity = ...
    class Config:
        title = 'gensModulesSequenceTransaction'



def generateSchema():
    import json
 #   print(Entity.schema_json(indent=2))
    print(TransactionSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()

