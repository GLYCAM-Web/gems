#!/usr/bin/env python3
from typing import Dict, List
from pydantic import BaseModel, Field, Json

from gemsModules.common.main_api_notices import Notices

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Resource(BaseModel):
    """Information describing a resource containing data."""
    locationType: Json[str] = Field(
            None,
            title='Location Type',
            description='Supported locations will vary with each Entity.'
            )
    resourceFormat: Json[str] = Field(
            None,
            title='Resource Format',
            description='Supported formats will varu with each Entity.',
            )
    payload : Json[str] = Field(
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
    

def generateSchema():
    print(Resource.schema_json(indent=2))

def generateJson():
    thisResource = Resource()
    thisResource.notices.addCommonParserNotice()
    print(thisResource.json(indent=2))


