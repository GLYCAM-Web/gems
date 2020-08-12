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
    omega = 'omega'

class LinkageRotamers(BaseModel): 
    indexOrderedLabel : str = None
    userDefinedLabel : str = None
    linkageContext : str = None
    possibleRotamers :  List[Tuple[LinkageRotamerNames,List[str]]] =[]
    likelyRotamers :   List[Tuple[LinkageRotamerNames,List[str]]] =[]
    selectedRotamers :   List[Tuple[LinkageRotamerNames,List[str]]] =[]

class LinkageRotamerSet(BaseModel):
    indexOrderedLabel : str = None
    userDefinedLabel : str = None
    linkageContext : str = None
    possibleRotamerSets :  List[Tuple[str,List[str]]] =[]
    likelyRotamerSets :   List[Tuple[str,List[str]]] =[]
    selectedRotamerSets :   List[Tuple[str,List[str]]] =[]

class ResidueGeometryOptions(BaseModel):
    """Geometry options for residues"""
    ringPuckers : List[ResidueRingPucker] = []

class LinkageGeometryOptions(BaseModel):
    """Geometry options for linkages"""
    rotamers : List[LinkageRotamers] = []
    rotamerSets : List[LinkageRotamerSet] = []

class GeometryOptions(BaseModel):
    Residues : ResidueGeometryOptions = None
    Linkages : LinkageGeometryOptions = None


class BuildOptions(BaseModel):
    """Options for building 3D models"""
    solvationOptions :  SystemSolvationOptions = None
    geometryOptions :  GeometryOptions = None

class DrawOptions(BaseModel):
    """Options for drawing 2D models"""
    Labeled : str = "true"

class SequenceInput(BaseModel):
    other : List[Resource] = []
    sequenceVariants: SequenceVariants = None
#    Definitions : Definitions = None
    buildOptions : BuildOptions = Field(
            None,
            description="Options for building the 3D Structure of the sequence."
            )
    drawOptions : DrawOptions = Field(
            None,
            description="Options for drawing a 2D Structure of the sequence."
            )

class SequenceOutput(SequenceInput):
    sequenceIsValid : str = "false"


class Service(commonio.Service):
    """Holds information about a Service requested of the Sequence Entity."""
    typename : Services = Field(
            'Build3DStructure',
            alias='type',
            title = 'Requested Service',
            description = 'The service requested of the Sequence Entity'
            )
    project: projectio.GemsProject = None
    inputs : SequenceInput = None
    outputs : SequenceOutput = None

class Response(Service):
    """Holds a response from a Service requested of the Sequence Entity."""
    typename : Services = Field(
            'Build3DStructure',
            alias='type',
            title = 'Requested Service',
            description = 'The service that was requested of Sequence Entity'
            )

class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType : str = Field(
            'Sequence',
            title='Type',
            alias='type'
            )
#    inputs :  = None
    requestID : str = Field(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    services : List[Service] = []
    responses : List[Response] = []
    inputs : SequenceInput = None
    options : commonio.Tags = None


def generateSchema():
    import json
    print(Entity.schema_json(indent=2))
#    print(Response.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()

