#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Field
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
import common.io as commonio
#from gemsModules.project import io as ProjectModels
from gemsModules.project import dataio as ProjectModels
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


# ##
# ## Services
# ##
class Services(str,Enum):
    build3dStructure = 'Build3dStructure'
    drawGlycan = 'drawGlycan'
    evaluate = 'Evaluate'
    status = 'Status'

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

# ##
# ## Recognized input and output formats
# ##
class Formats(str,Enum):
    glycamCondensed = 'GlycamCondensed'

class Locations(str,Enum):
    internal='internal'

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

