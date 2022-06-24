#!/usr/bin/env python3
from enum import Enum
from uuid import UUID
from typing import Dict, List 
from pydantic import BaseModel, Field, Json
from gemsModules.common.notices import Notices
from gemsModules.common.settings import AvailableServices

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class AvailableServices(str, Enum):
    errorNotification = 'ErrorNotification'
    marco = 'Marco'
    status = 'Status'

class Service(BaseModel):
    """
    Holds information about a requested Service.
    This object will have different forms in each Entity.
    """
    typename: AvailableServices = Field(
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

class Services(BaseModel):
    __root__ : Dict[str,Service] = None

    def add_service(self,
            typename  = 'UnknownService',
            inputs  = None,
            givenName = None,
            myUuid = None,
            options = None
            ):
        thisService = Service()
        thisService.typename = typename
        thisService.givenName = givenName
        thisService.myUuid = myUuid
        thisService.inputs = inputs
        thisService.options = options
        if self.__root__ is None :
            self.__root__ : List[Service] = []
        self.__root__.append(thisService)
    
    def is_present(self, typename : str) :
        if self.__root__  is None or self.__root__ == [] :
            return False
        if typename in self.__root__ :
            return True
        else :
            return False

class Responses(BaseModel):
    __root__ : Dict[str,Response] = None

    def add_response(self,
            typename : str = 'UnknownService',
            outputs : Json = {'message': 'A response was requested, but GEMS does not know why.'},
            notices : Notices = None
            ):
        thisResponse = Response()
        thisResponse.typename = typename
        thisResponse.outputs = outputs
        if notices is not None :
            thisResponse.notices = notices
        if self.__root__ is None :
            self.__root__ : List[Response] = []
        self.__root__.append(thisResponse)





def generateSchema():
    import json
    print(Services.schema_json(indent=2))
#    print(Responses.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
