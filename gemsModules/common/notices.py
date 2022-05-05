#!/usr/bin/env python3
# ###############################################################
import traceback
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List
from pydantic import BaseModel, Field, Json, PrivateAttr
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
    noticeBrief: str = Field(
            None,
            title='Brief',
            alias='brief',
            description='Brief title, status or name for this notice or notice type.'
            )
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


def makeDefaultNoticesList() :
    from gemsModules.common.noticedata import NoticeData
    theNotices : List[Notice] = []
    for noticedatum in NoticeData :
        tempNotice : Notice = Notice()
        tempNotice.noticeBrief=noticedatum.Brief
        tempNotice.noticeType=noticedatum.Type
        tempNotice.noticeCode=noticedatum.Code
        tempNotice.noticeScope=noticedatum.Scope
        tempNotice.noticeMessage=noticedatum.Message
        tempNotice.messagingEntity=noticedatum.RespondingEntity
        theNotices.append(tempNotice)
    return theNotices
  

class Notices(BaseModel):
    __root__ : List[Notice] = None
    _defaultNoticeTypes : List[Notice] = PrivateAttr(default_factory=makeDefaultNoticesList)

    def printDefaults(self):
        for noticedatum in self._defaultNoticeTypes :
            print(noticedatum.json(indent=2))

    def addCommonParserNotice(self, *args, **kwargs) :
        pass
#        self.__root__.append(settings.generateCommonParserNotice(*args, **kwargs))


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

def generateSchema():
    print(Notices.schema_json(indent=2))

def showDefaultNotices():
    tempNotices=Notices()
    tempNotices.printDefaults()

if __name__ == "__main__":
  generateSchema()
  #showDefaultNotices()
  
    
