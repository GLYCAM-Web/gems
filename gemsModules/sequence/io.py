#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonio
from gemsModules.project import dataio as projectio
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
    def InitializeClass(self, validatedSequence : Sequence):
        from gemsModules.sequence import evaluate
        self.linkages = evaluate.getLinkageOptionsFromGmmlcbBuilder(validatedSequence)
        #print(self.linkages.json())

class BuildOptions(BaseModel):
    """Options for building 3D models"""
    solvationOptions : SystemSolvationOptions = None  # Not yet handled.
    geometryOptions : GeometryOptions = None
    def InitializeClass(self, validatedSequence : Sequence):
        self.geometryOptions = GeometryOptions ()
        self.geometryOptions.InitializeClass(validatedSequence)
        #print(self.geometryOptions.json())

class DrawOptions(BaseModel):
    """Options for drawing 2D models"""
    Labeled : str = "true"

# Oliver Oct2020 finds this unnecessary. Not sure what other is going to be.
# class SequenceInput(BaseModel):
#     other : List[Resource] = []
    
class SequenceOutput(BaseModel):
    sequenceIsValid : str = "false"
    sequenceVariants: SequenceVariants = None
    buildOptions : BuildOptions = Field(
            None,
            description="Options for building the 3D Structure of the sequence."
            )
    drawOptions : DrawOptions = Field(
            None,
            description="Options for drawing a 2D Structure of the sequence."
            )
    def InitializeClass(self, sequence : Sequence, validateOnly : bool):
        from gemsModules.sequence import evaluate
        self.sequenceIsValid = evaluate.checkIsSequenceSane(sequence)
        if self.sequenceIsValid and not validateOnly:
            self.sequenceVariants = evaluate.getSequenceVariants(sequence)
            self.buildOptions = BuildOptions()
            self.buildOptions.InitializeClass(sequence)
            #drawOptions to be developed later.
        return self.sequenceIsValid
        
class Service(commonio.Service):
    """Holds information about a Service requested of the Sequence Entity."""
    typename : Services = Field(
            'Build3DStructure',
            alias = 'type',
            title = 'Requested Service',
            description = 'The service requested of the Sequence Entity'
            )
    project: projectio.GemsProject = None
    inputs : Sequence = None
    outputs : SequenceOutput = None
    def InitializeClass(self, sequence : Sequence, validateOnly : bool):
        self.inputs = sequence
        self.outputs = SequenceOutput()
        self.outputs.InitializeClass(sequence, validateOnly)
        

class Response(Service):
    """Holds a response from a Service requested of the Sequence Entity."""
    entity : str = "Sequence"
    typename : Services = Field(
            'Build3DStructure',
            alias='type',
            title = 'Requested Service',
            description = 'The service that was requested of Sequence Entity'
            )
    # This in herits from Service, so can all its InitialiseClass().

# Drafted by Lachele, but probably not needed. Oliver Oct2020
# class Entity(BaseModel):
#     """Holds information about the main object responsible for a service."""
    
#     entityType : str = Field(
#             'Sequence',
#             title='Type',
#             alias='type'
#             )
# #    inputs :  = None
#     requestID : str = Field(
#             None,
#             title = 'Request ID',
#             description = 'User-specified ID that will be echoed in responses.'
#             )
#     services : List[Service] = []
#     responses : List[Response] = []
#   #  inputs : SequenceInput = None # This is already in Service...
#     options : commonio.Tags = None

def generateSchema():
    import json
    print(Response.schema_json(indent=2))
#    print(Response.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()

