#!/usr/bin/env python3
#
# ###############################################################
# ##
# ##  The gemsModules are being refactored so that they use
# ##  this file for the main schema definitions.  This file  
# ##  might not be in full use by all modules.
# ##
# ##  The modules/Entities that are partially or wholly 
# ##  changed so that they use this file are:
# ##
# ##      conjugate
# ##      Sequence
# ##      Project
# ##
# ##  Go see that module for examples, etc.
# ##
# ##  Please add your module to the list when you change 
# ##  it, just to help reduce chaos.
# ##
# ##  Got a better accounting method?  Let's hear it!
# ##
# ###############################################################
import traceback
from enum import Enum, auto
from typing import Dict, List
from pydantic import BaseModel, Field, Json
from pydantic.schema import schema
from gemsModules.common import settings
from gemsModules.common.notices import Notices
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

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


if __name__ == "__main__":
  generateSchema()
#  generateJson()
    
