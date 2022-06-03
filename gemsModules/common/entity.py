#!/usr/bin/env python3
from typing import Dict, List #, Optional, Sequence, Set, Tuple, Union, Any
from pydantic import BaseModel, Field
from gemsModules.common.notices import Notices
from gemsModules.common import settings
from gemsModules.common.services import Service, Response
from gemsModules.common.resources import Resource

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType : str = Field(
            settings.WhoIAm,
            title='Type',
            alias='type'
            )
    requestID : str = Field(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    services : Dict[str,Service] = None
    responses : Dict[str,Response] = None
    resources : List[Resource] = None
    notices : Notices = Notices()
    options : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )

def generateSchema():
    import json
    print(Entity.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
