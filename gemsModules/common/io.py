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
# ##      Sequence
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
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Field, Json
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
# ##
# ## This should probably not be needed after refactoring for this file
# ## But, it might still be desired, depending
# from gemsModules.project import dataio as ProjectModels


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class NoticeTypes(str, Enum):
    note = 'Note'
    warning = 'Warning'
    error = 'Error'
    exit = 'Exit'

class Tags(BaseModel):
    options : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )

class Notice(BaseModel):
    """Description of a Notice."""
    noticeType: NoticeTypes = Field(
            None,
            title='Type',
            alias='type'
            )
    noticeCode: str = Field(
            None,
            title='Code',
            alias='code',
            description='Code associated with this notice.'
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
    options : Tags = None

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
    tags : Tags = None
    options : Tags = None
    notice : Notice = None

class Service(BaseModel):
    """Holds information about a requested Service."""
    typename : Json[str]  = Field(
            None,
            title='Type of Service.',
            alias='type',
            description='The services available will vary by Entity.'
            )
    inputs : Json = None
    outputs : Json = None
    # requestID : str = Field(
    #         None,
    #         title = 'Request ID',
    #         description = 'User-specified ID that will be echoed in responses.'
    #         )
    # options : Tags = None
    # project : Json = Field(
    #         None,
    #         title='Gems Project Information',
    #         description='See this doc somewhere for more information',
    #         )
    # project : Json = Field(
    #         None,
    #         title='A GEMS Project',
    #         description='This is generally assigned in the project module'
    #         )
    subentities : Json = Field(
            None,
            title='Subentities',
            description='List of Entities, and associated Services, needed by this Service'
            )

class Response(Service):
    """Holds information about a response to a service request."""
    typename : Json[str] = Field(
            None,
            title='Responding Service.',
            alias='type',
            description='The type service that produced this response.'
            )
    # subentities : Json = Field(
    #         None,
    #         title='Responding Subentities',
    #         description='List of Entities, and associated Services, needed by this Response'
    #         )

class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType : Json[str] = Field(
            ...,
            title='Type',
            alias='type'
            )
    inputs : List[Json] = None
    requestID : str = Field(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    services : List[Json] = None
    responses : List[Json] = None
    options : Tags = None


def generateSchema():
    import json
    #print(Service.schema_json(indent=2))
    print(Entity.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
