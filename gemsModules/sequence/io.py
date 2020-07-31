#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Field
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
    locationType : Locations = Field(
            'internal',
            description='Supported input locations for the Service Entity.'
            )
    resourceFormat : Formats = Field(
            'GlycamCondensed',
            description='Supported input formats for the Service Entity.'
            )

class Service(commonio.Service):
    """Holds information about a Service requested of the Sequence Entity."""
    typename : Services = Field(
            'Build3DStructure',
            title = 'Requested Service',
            description = 'The service requested of the Sequence Entity'
            )
    inputs : List[Resource] = None
    outputs : List[Resource] = None
    project: projectio.GemsProject = None

class Response(Service):
    """Holds a response from a Service requested of the Sequence Entity."""
    # the ordered condensed sequences
    IndexOrder = 'IndexOrder'
    LongestChainOrder = 'LongestChainOrder'
    UserOrdered = 'UserOrdered'  
    # other condensed sequences
    MonospacedTextDiagram = 'MonospacedTextDiagram'
    Suuid = 'Suuid'  
    Smd5sum = 'Smd5sum'  
    # the ordered condensed sequences, labeled
    IndexOrderLabeled = 'IndexOrderLabeled'
    LongestChainOrderLabeled = 'LongestChainOrderLabeled'
    UserOrderedLabeled = 'UserOrderedLabeled'  
    # other condensed sequences, labeled
    MonospacedTextDiagramLabeled = 'MonospacedTextDiagramLabeled'
    SuuidLabeled = 'SuuidLabeled'  
    Smd5sumLabeled = 'Smd5sumLabeled'  
    # entire JSON objects to be parsed
    Definitions = 'Definitions'
    BuildOptions = 'BuildOptions'



# ##
# ## Environment variables
# ##
class Environment(str,Enum):
    ## The entity itself
    sequenceentity   = 'GEMS_MODULES_SEQUENCE_PATH'
    ## Services for this entity, in alphabetical order
    build3DStructure = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'
    graph = 'GEMS_MODULES_SEQUENCE_GRAPH_PATH'
    evaluate         = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'


def generateSchema():
    import json
    print(Service.schema_json(indent=2))
#    print(Response.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()

