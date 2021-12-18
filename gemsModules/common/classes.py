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
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class NoticeTypes(str, Enum):
    note = 'Note'
    warning = 'Warning'
    error = 'Error'
    exit = 'Exit'

class Notice(BaseModel):
    """Description of a Notice."""
    noticeType : NoticeTypes = Field(
            None,
            title='Type',
            alias='type'
            )
    noticeCode : str = Field(
            None,
            title='Code',
            alias='code',
            description='Numeric code associated with this notice, for users who like this sort of thing.'
            )
    noticeBrief: str = Field(
            None,
            title='Brief',
            alias='brief',
            description='Brief title, status or name for this notice or notice type.'
            )
    noticeMessage : str = Field(
            None,
            title='Message',
            alias='message',
            description='A more detailed message for this notice.'
            )
    noticeScope : str = Field(
            None,
            title='Context of notice',
            alias='scope',
            description='The scope at which the error occured.'
            )
    messagingEntity : str = Field(
            None,
            title='Messaging Entity',
            description='The Entity that raised the notice, if known.'
            )
    additionalInfo : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )

class Notices(BaseModel):
    notices : List[Notice] = []

    def generateCommonParserNotice(self, *args, **kwargs) :
        self.notices.append(settings.generateCommonParserNotice(*args, **kwargs))

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
    notices : List[Notice] = None
#    notices : Notices = Notices()  ## This is preferred in code, but is not good for json
    options : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )

    def generateCommonParserNotice(self, *args, **kwargs) :
        self.notices.append(settings.generateCommonParserNotice(*args, **kwargs))


def generateSchema():
    #print(Notice.schema_json(indent=2))
    #print(Notices.schema_json(indent=2))
    print(Resource.schema_json(indent=2))

def generateJson():
    thisResource = Resource()
    thisResource.notices.generateCommonParserNotice()
    print(thisResource.json(indent=2))


if __name__ == "__main__":
  generateSchema()
#  generateJson()
    
