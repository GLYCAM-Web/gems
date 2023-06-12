#!/usr/bin/env python3
from typing import Dict, List, Union
from pydantic import BaseModel, Field

from gemsModules.common.main_api_notices import Notices

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Resource(BaseModel):
    """Information describing a resource containing data."""
    typename : str  = Field(
        'Unset',
        alias='type',
        title='Resource type',
        description='The name of the type of Resource.'
    )
    locationType: str = Field(
            None,
            title='Location Type',
            description='Supported locations will vary with each Entity.'
            )
    resourceFormat: str = Field(
            None,
            title='Resource Format',
            description='Supported formats will vary with each Entity.',
            )
    payload : Union[str,int,float] = Field(
            None,
            description='The thing that is described by the location and format'
            )
    notices : Notices = Notices()  
    options : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )

class Resources(BaseModel):
    __root__ : List[Resource] = None
    
    def add_resource(self,
            resource : Resource
            ):
        if self.__root__ is None :
            self.__root__ : List[Resource] = []
        self.__root__.append(resource)
    
    def type_is_present(self, typename : str) :
        if self.__root__  is None or self.__root__ == [] :
            return False
        for resource in self.__root__ :
            if resource.typename == typename :
                return True
        else :
            return False

    def get_resource_by_type(self, typename : str):
        if self.__root__  is None or self.__root__ == [] :
            return False
        for resource in self.__root__ :
            if resource.typename == typename :
                return resource
        else :
            return None



def generateSchema():
    print(Resource.schema_json(indent=2))

def generateJson():
    thisResource = Resource()
    thisResource.notices.addCommonParserNotice()
    print(thisResource.json(indent=2))


