#!/usr/bin/env python3
from uuid import UUID
from typing import Any, Dict, List
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
    inputs: Json[Any] = None
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
    outputs : Json[Any] = None
    notices : Notices = Notices()

class Services(BaseModel):
    __root__ : Dict[str,Service] = None

    def add_service(self,
            key_string : str ,
            service : Service
            ):
        if self.__root__ is None :
            self.__root__ : Dict[str,Service] = {}
        self.__root__[key_string]=service
    
    def is_present(self, typename : str) :
        if self.__root__  is None or self.__root__ == {} :
            return False
        the_services = self.__root__.values()
        for service in the_services :
            if service.typename == typename :
                return True
        else :
            return False

class Responses(BaseModel):
    __root__ : Dict[str,Response] = None

    def add_response(self,
            key_string : str,
            response : Response
            ):
        if self.__root__ is None :
            self.__root__ : Dict[str,Response] = {}
        self.__root__.append(key_string,response)


def generateSchema():
    import json
    print(Services.schema_json(indent=2))
#    print(Responses.schema_json(indent=2))

