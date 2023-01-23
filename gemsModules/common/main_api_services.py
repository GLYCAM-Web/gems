#!/usr/bin/env python3
from uuid import UUID
from typing import Dict, List
from pydantic import BaseModel, Field, Json

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.settings_main import All_Available_Services

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Service(BaseModel):
    """
    Holds information about a requested Service.
    This object will have different forms in each Entity.
    """
    typename: All_Available_Services = Field(
        'Status',
        alias='type',
        title='Common Services',
        description='The service requested of the Common Servicer'
    )
    givenName: str = Field(
        None,
        title='The name given this object in the transaction',
        description='A place for users to specify a name.'
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

class Response(BaseModel):
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
    givenName: str = Field(
        None,
        title='The name given this object in the transaction',
        description='A place for users to specify a name.'
    )
    myUuid: UUID = Field(
        None,
        title='My UUID',
        description='ID to allow correlations between services and responses.'
    )
    outputs : Json = None
    notices : Notices = Notices()

class Services(BaseModel):
    __root__ : Dict[str,Service] = None

    def add_service(self,
            typename : str ,
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
