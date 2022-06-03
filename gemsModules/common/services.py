#!/usr/bin/env python3
from enum import Enum, auto
from uuid import UUID
from typing import Dict #, List, Optional, Sequence, Set, Tuple, Union, Any
from pydantic import BaseModel, Field, Json
from gemsModules.common.notices import Notices

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Services(str, Enum):
    errorNotification = 'ErrorNotification'
    status = 'Status'

class Service(BaseModel):
    """
    Holds information about a requested Service.
    This object will have different forms in each Entity.
    """
    typename: Services = Field(
        'Status',
        alias='type',
        title='Common Services',
        description='The service requested of the Common Servicer'
    )
    givenName: str = Field(
        None,
        title='The name given this object in the transaction'
    )
    myUuid: UUID = Field(
        None,
        title='My UUID',
        description='ID to allow correlations between services and responses.'
    )
    inputs: Json = None
    options: Dict[str, str] = Field(
        None,
        description='Key-value pairs that are specific to each entity, service, etc'
    )

class Response(Service):
    """
    Holds information about a response to a service request.
    This object will have different forms in each Entity.
    """
    typename : str = Field(
            None,
            title='Responding Service.',
            alias='type',
            description='The type service that produced this response.'
            )
    outputs : Json = None
    notices : Notices = Notices()


def generateSchema():
    import json
    print(Service.schema_json(indent=2))
    print(Response.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
