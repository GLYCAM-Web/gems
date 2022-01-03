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
from dataclasses import dataclass, field
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

## The key in the following dictionaries is called
##
##       noticeBrief 
##
## These dictionaries contain information about error messages 
## an entity/module might return.
@dataclass
class noticeDatum:
    brief : str = 'UnknownError'
    noticeType : str = 'error'
    scope : str = 'Unknown'
    code : int = 500
    message : str = 'We really have no idea what went wrong.'

@dataclass
class noticeData:
    definedNotices : List[noticeDatum] = field ( default_factory = self.generate_default_notices )

    def generate_default_notices():


ExitTypes = {
    'NoEntityDefined':'error',
    'EntityNotKnown':'error',
    'NoTypeForEntity':'error',
    'JsonParseEror':'error',
    'ServiceNotKnownToEntity':'error',
    'RequestedEntityNotFindable':'error',
    'EmptyPayload':'error',
    'InvalidInput':'error',
    'GmmlError':'error',
    'GemsError':'error',
    'InvalidInputPayload':'error',
    'NoInputPayloadDefined':'error',
    'UnknownError':'error'
}
ExitScopes = {
    'NoEntityDefined':'Transaction',
    'EntityNotKnown':'Entity',
    'NoTypeForEntity':'Entity',
    'JsonParseEror':'Transaction',
    'ServiceNotKnownToEntity':'Service',
    'RequestedEntityNotFindable':'SystemError',
    'EmptyPayload':'Transaction',
    'InvalidInput':'Transaction',
    'GmmlError':'SyatemError',
    'GemsError':'SystemError',
    'InvalidInputPayload':'Transaction',
    'NoInputPayloadDefined':'Transaction',
    'UnknownError':'Unknown'
}
ExitCodes = {
    'NoEntityDefined':'301',
    'EntityNotKnown':'302',
    'NoTypeForEntity':'303',
    'JsonParseEror':'304',
    'ServiceNotKnownToEntity':'305',
    'RequestedEntityNotFindable':'310',
    'GmmlError':'315',
    'EmptyPayload':'400',
    'InvalidInput':'400',
    'GemsError':'315',
    'InvalidInputPayload':'400',
    'NoInputPayloadDefined':'400',
    'UnknownError':'500'
}
ExitMessages = {
    'NoEntityDefined':'The JSON object does not contain an Entity.',
    'EntityNotKnown':'The entity in this JSON Onject is not known to the commonServicer.',
    'NoTypeForEntity':'The Entity does not contain a type.',
    'JsonParseEror':'There was an unknown error parsing the JSON Object.',
    'ServiceNotKnownToEntity':'The requested Entity does not offer this Service.',
    'RequestedEntityNotFindable':'The requested Entity is known, but does not respond.',
    'EmptyPayload':'Missing or empty input payload.',
    'InvalidInput':'error',
    'GmmlError':'An interaction with GMML failed.',
    'GemsError':'There was an error in GEMS',
    'InvalidInputPayload':'An invalid payload was detected.',
    'NoInputPayloadDefined':'No payload could be found.',
    'UnknownError':'We really have no idea what went wrong.'
}

# ## See above for definition of noticeBrief
###
### This should really move to services.py.  It's only here because it relies so
###   much on the notice info above.  
###
def generateCommonParserNotice(
        noticeBrief     : str  = 'UnknownError' ,  # Lookup keyword for the error
        scope           : str  = None,             # Is this from entity? service? transaction?
        messagingEntity : str  = None,             # Which entity sends this message?
        exitType        : str  = None,             # Error, Warning, Info
        exitCode        : str  = None,             # Numeric code because those can be useful
        exitMessage     : str  = None,             # Human-readable brief description
        additionalInfo  : Dict = None              # Free-form dictionary of data to return 
        ):
    log.info("generateCommonParserNotice() was called.\n")

    if ExitTypes[noticeBrief] is None :
        log.info("Unknown noticeBrief, '" + noticeBrief + "', sent to generateCommonParserNotice() \n")
        noticeBrief = 'UnknownError'

    if messagingEntity is None :
        messagingEntity='CommonServicer'

    if scope is None :
        scope : str = ExitScopes[noticeBrief]
    if exitType is None :
        exitType = ExitTypes[noticeBrief],
    if exitCode is None :
        exitCode = ExitCodes[noticeBrief],
    if exitMessage is None :
        exitMessage = ExitMessages[noticeBrief],

    # Build the notice for newer code
    thisNotice = common.io.Notice()
    thisNotice.noticeType=exitType
    thisNotice.noticeCode=exitCode
    thisNotice.noticeBrief=noticeBrief
    thisNotice.noticeScope=scope
    thisNotice.noticeMessage=exitMessage
    thisNotice.messagingEntity=messagingEntity
    if additionalInfo is not None : 
        thisNotice.additionalInfo=additionalInfo

    return thisNotice

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
    __root__ : List[Notice] = []

    def addCommonParserNotice(self, *args, **kwargs) :
        self.__root__.append(settings.generateCommonParserNotice(*args, **kwargs))


def generateSchema():
    print(Notices.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
    
