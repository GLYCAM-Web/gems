#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from typing import ForwardRef
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonio
from gemsModules.project import io as projectio
from gemsModules.project import projectUtil as projectUtil
from gemsModules.sequence import settings
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class Resource(commonio.Resource):
    locationType : settings.Locations = Field(
            'internal',
            description='Supported input locations for the Service Entity.'
            )
    resourceFormat : settings.Formats = Field(
            'GlycamCondensed',
            description='Supported input formats for the Service Entity.'
            )

class TheSequence(BaseModel) :
    payload : str = ''
    sequenceFormat : str = Field(
            'GlycamCondensed',
            alias='format',
            description =  'The format of the sequence in the payload'
            )
    class Config:
        title = 'Sequence'

class TheSequenceVariants(BaseModel):
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

class TheSystemSolvationOptions(BaseModel):
    solvationStatus : str = Field(
            'Unsolvated',
            description="Unsolvated, To be solvated, Solvated, Not applicable"
            )
    ionStatus : str = Field(
            'No ions',
            description="No ions, Add ions, Contains ions."
            )

class TheResidueRingPucker(BaseModel):
    puckerClassificationSystem : str = Field(
            'BFMP',
            description="The system used to identify the ring pucker (shape)."
            )

class TheDihedralRotamers(BaseModel):
    dihedralName : str = None # phi, psi etc. Use Enum above once anything works :(
    dihedralValues : List[str] = [] # gg, -g, tg, etc

class TheLinkageRotamers(BaseModel): 
    indexOrderedLabel : str = None
    linkageName : str = None
    firstResidueNumber : str = None
    secondResidueNumber : str = None
    dihedralsWithOptions : List[str] = []
    possibleRotamers : List[TheDihedralRotamers] = []
    likelyRotamers : List[TheDihedralRotamers] = []

class TheResidueGeometryOptions(BaseModel):
    """Geometry options for residues"""
    ringPuckers : List[TheResidueRingPucker] = []

class TheLinkageGeometryOptions(BaseModel):
    """Geometry options for linkages"""
    linkageRotamersList : List[TheLinkageRotamers] = []
    totalLikelyRotamers : int = 0
    totalPossibleRotamers : int = 0

# I can't figure out if I can pass gmml classes to functions here, so I just 
# wrote getLinkageOptionsFromGmmlcbBuilder.
class TheGeometryOptions(BaseModel):
    residues : TheResidueGeometryOptions = None # Not yet handled.
    linkages : TheLinkageGeometryOptions = None

    def __init__(self, **data : Any):
        super().__init__(**data)

    def setLinkages(self, validatedSequence : Sequence):
        from gemsModules.sequence import evaluate
        self.linkages = evaluate.getLinkageOptionsFromGmmlcbBuilder(validatedSequence)
        log.debug(self.linkages.json())

class TheBuildOptions(BaseModel):
    """Options for building 3D models"""
    solvationOptions : TheSystemSolvationOptions = None  # Not yet handled.
    geometryOptions : TheGeometryOptions = None
    mdMinimize : bool = Field(
            True,
            title = 'Minimize structure using MD',
            )

    def __init__(self, **data : Any):
        super().__init__(**data)

    def setGeometryOptions(self, validatedSequence : Sequence):
        log.info("Setting geometryOptions in BuildOptions")
        log.debug("validatedSequence: " + validatedSequence)
        self.geometryOptions = GeometryOptions.setLinkage(validatedSequence)


class TheDrawOptions(BaseModel):
    """Options for drawing 2D models"""
    Labeled : str = "true"  ## Lachele Mar 2020 - should this be a bool?


class SequenceEvaluationOutput(BaseModel):
    sequenceIsValid : bool = False
    validateOnly : bool = False
    sequenceVariants: TheSequenceVariants = None
    buildOptions : TheBuildOptions = Field(
            None,
            description="Options for building the 3D Structure of the sequence."
            )
    drawOptions : TheDrawOptions = Field(
            None,
            description="Options for drawing a 2D Structure of the sequence."
            )

    def __init__(self, **data : Any):
        super().__init__(**data)

    def getEvaluation(self, sequence:str, validateOnly):
        log.info("Getting the Evaluation for SequenceEvaluationOutput.")

        log.debug("sequence: " + repr(sequence))
        log.debug("validateOnly: " + repr(validateOnly))

        from gemsModules.sequence import evaluate

        self.validateOnly = validateOnly
        self.sequenceIsValid = evaluate.checkIsSequenceSane(sequence)
        log.debug("self.sequenceIsValid: " + str(self.sequenceIsValid))

        if self.sequenceIsValid:
            self.sequenceVariants = evaluate.getSequenceVariants(sequence)
        if self.sequenceIsValid and not validateOnly:
            self.buildOptions = BuildOptions.setGeometryOptions(sequence)
            
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

    def __init__(self, **data : Any):
        super().__init__(**data)

        log.debug("These are the values at initialization of Build3DStructureOutput")
        log.debug("payload(projectID): " + self.payload)
        log.debug("sequence: " + self.sequence)
        log.debug("seqID: " + self.seqID)
        log.debug("conformerID: " + self.conformerID)
        log.debug("conformerLabel: " + self.conformerID)
        log.debug("subDirectory: " + self.subDirectory)
        log.debug("downloadUrl: " + self.downloadUrl)

#    def getTheOutput(self, payload:str, sequence:str, seqID:str, conformerID:str, conformerLabel:str):

    def setSubDirectory() :
        self.subDirectory = '/Requested_Builds/' + conformerID + '/'
    def setDownloadUrl() :
        self.downloadUrl = projectUtil.getDownloadUrl(payload, "cb", self.conformerID)


# ## These do not need to be named with 'sequence, e.g., 'sequenceService'.  
# ## Doing that just makes me feel more comfortable about referencing things.
# ## 
# ## Regarding capitalization, my current ad-hoc convention:
# ##    - initial is lower case = this is a child class of something else and
# ##      the first word is the modifier.  
# ##          example:  sequenceService is a child of Service, modified by sequence
# ##    - initial is upper case = this is not a child, except of BaseModel.
# ##          example:  SequenceInputs is not a child of another class.
# $$ (Lachele)
class sequenceService(commonio.Service):
    """Holds information about a Service requested of the Sequence Entity."""
    typename : settings.Services = Field( 
        'Evaluate', 
        alias = 'type', 
        title = 'Requested Service', 
        description = 'The service requested of the Sequence Entity'
        )

    def __init__(self, **data : Any):
        super().__init__(**data)
        log.info("Initializing Service.")
        log.debug("the data " + repr(self))
        log.debug("Init for the Services in sequence was called.")


## This is a Response and should be called that, and based on Service (Lachele)
class sequenceResponse(sequenceService) : 
    """Holds a response from a Service requested of the Sequence Entity."""
    respondingEntity : str = settings.WhoIAm
    outputs : List[Union[SequenceEvaluationOutput, Build3DStructureOutput, Resource]] = []

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a sequenceResponse")
        log.debug("respondingEntity: " + self.respondingEntity)

class SequenceInputs(BaseModel) :
    Sequence : TheSequence = None
    SequenceVariants : TheSequenceVariants = None
    SystemSolvationOptions : TheSystemSolvationOptions = None 
    ResidueRingPucker : TheResidueRingPucker = None 
    DihedralRotamers : TheDihedralRotamers = None 
    LinkageRotamers : TheLinkageRotamers = None 
    ResidueGeometryOptions : TheResidueGeometryOptions = None 
    LinkageGeometryOptions : TheLinkageGeometryOptions = None 
    GeometryOptions : TheGeometryOptions = None 
    BuildOptions : TheBuildOptions = None 
    DrawOptions : TheDrawOptions = None


class sequenceEntity(commonio.Entity):
    """Holds information about the main object responsible for a service."""
    entityType : str = Field(
            settings.WhoIAm,
            title='Type',
            alias='type'
            )
    services : List[Dict[str,sequenceService]] = []
    responses : List[Dict[str,sequenceResponse]] = []
    inputs : List[Union[SequenceInputs,Resource]] =  None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a sequenceEntity")
        log.debug("entityType: " + self.entityType)

    def initialize_responses_from_services(self) :
        self.responses(**self.services)

    def append_input_resource(self, theResource : Resource) :
        self.inputs.append(theResource)

    def append_output_resource(self, theResource : Resource) :
        self.outputs.append(theResource)

class sequenceTransactionSchema(commonio.TransactionSchema):
    """
    Holds info about the Transaction JSON object used in the Sequence entity.
    """
    entity : sequenceEntity = ...
    project : projectio.CbProject = None

    def __init__(self, **data : Any):
        super().__init__(**data)

    class Config:
        title = 'gensModulesSequenceTransaction'

class Transaction(commonio.Transaction):
    transaction_in : sequenceTransactionSchema 
    transaction_out: sequenceTransactionSchema 
    
    def populate_transaction_in(self) :

        self.transaction_in = sequenceTransactionSchema(**self.request_dict)
        log.debug("The transaction_in is: " )
        log.debug(self.transaction_in.json(indent=2))

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self) :
        if self.transaction_in is None :
            return None
        if self.transaction_in.entity is None :
            return None
        if self.transaction_in.entity.inputs is None :
            return None
        for i in self.transaction_in.entity.inputs : 
            if i.Sequence is not None :
                if i.Sequence.payload is not None :
                    if i.Sequence.payload is not "" :
                        return i.Sequence.payload
        return None


def generateSchema():
    import json
 #   print(Entity.schema_json(indent=2))
    print(sequenceTransactionSchema.schema_json(indent=2))

inputJSON='{ "entity": { "type": "Sequence", "services": [ { "Build": { "type": "Build3DStructure" } } ], "inputs": [ { "Sequence": { "payload": "DManpa1-OH" } } ] } }'

def troubleshoot():
    thisTransaction=Transaction(inputJSON)
    print(thisTransaction.incoming_string)
    print(thisTransaction.request_dict)
    thisTransaction.populate_transaction_in()
    print(thisTransaction.transaction_in)

if __name__ == "__main__":
  generateSchema()
  troubleshoot()

