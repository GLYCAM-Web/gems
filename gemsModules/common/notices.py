#!/usr/bin/env python3
# ###############################################################
import traceback
from enum import Enum, auto
from typing import Dict, List
from pydantic import BaseModel, Field, PrivateAttr
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
    Brief: str = Field(
            None,
            title='Brief',
            alias='brief',
            description='Brief title, status or name for this notice or notice type.'
            )
    Type : NoticeTypes = Field(
            None,
            title='Type',
            alias='type'
            )
    Code : str = Field(
            None,
            title='Code',
            alias='code',
            description='Numeric code associated with this notice, for users who like this sort of thing.'
            )
    Message : str = Field(
            None,
            title='Message',
            alias='message',
            description='A more detailed message for this notice.'
            )
    Scope : str = Field(
            None,
            title='Context of notice',
            alias='scope',
            description='The scope at which the error occured.'
            )
    Messenger : str = Field(
            None,
            title='Messaging Entity',
            description='The Entity that raised the notice, if known.'
            )
    AdditionalInfo : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )


def makeDefaultNoticesList() :
    from gemsModules.common.noticedata import NoticeData
    theNotices : List[Notice] = []
    tempNotice : Notice = Notice()   
    for noticedatum in NoticeData :
        tempNotice.Brief      =  noticedatum.Brief
        tempNotice.Type       =  noticedatum.Type
        tempNotice.Code       =  noticedatum.Code
        tempNotice.Scope      =  noticedatum.Scope
        tempNotice.Message    =  noticedatum.Message
        tempNotice.Messenger  =  noticedatum.Messenger
        theNotices.append(tempNotice.copy())
    return theNotices
  

class Notices(BaseModel):

    __root__ : List[Notice] = None
    _defaultNoticeTypes : List[Notice] = PrivateAttr(default_factory=makeDefaultNoticesList)


    def printDefaults(self, sendTo='logs', style='easyRead'):
        self.printNotices(sendTo=sendTo, style=style, whatToPrint='Defaults')


    def printNotices(self, sendTo='logs', style='easyRead', whatToPrint='Notices'):
        if whatToPrint == 'Notices':
            printString = "Printing the Notices: \n" + self.noticesString(style, whatToPrint=whatToPrint)
        elif whatToPrint == 'Defaults' :
            printString = "Printing the Default Notices: \n" + self.defaultNoticesString(style)
        else :
            log.error("Unknown printTarget (whatToPrint) in printNotices")
            return ""
        if sendTo == 'logs' :
            log.debug(printString)
        elif sendTo == 'stdout' :
            print(printString)
        else :
            log.error("The sendTo option given to Notices.printDefaults() is not known.  Cannot print.")


    def defaultNoticesString(self, style='easyRead'):
        return self.noticesString(style=style, whatToPrint='Defaults')


    def noticesString(self, style='easyRead', whatToPrint='Notices'):
        if whatToPrint == 'Notices':
            printTarget = self.__root__
        elif whatToPrint == 'Defaults' :
            printTarget = self._defaultNoticeTypes
        else :
            log.error("Unknown printTarget (whatToPrint) in noticesString")
            return ""
        if style == 'easyRead' :
            printString = ""
            for noticedatum in printTarget:
                printString = printString + noticedatum.json(indent=2) 
        elif style == 'minified' :
            printString = ""
            for noticedatum in printTarget:
                printString = printString + noticedatum.json() 
        elif style == 'terse' :
            import pprint 
            printString = pprint.pformat(printTarget)
        else: 
            log.error("Style type given to Notices.defaultNoticesString() is not known.  Cannot generate string.")
            printString = "'Unable to generate'"
        return printString


    def addDefaultNotice(self,
            brief           : str  = 'UnknownError' ,  # Lookup keyword for the error
            scope           : str  = None,             # Is this from entity? service? transaction?
            messenger       : str  = None,             # Which entity sends this message?
            noticeType      : str  = None,             # Error, Warning, Info
            code            : str  = None,             # Numeric code because those can be useful
            message         : str  = None,             # Human-readable brief description
            additionalInfo  : Dict = None  # Free-form dictionary of data to return 
            ):
        log.info("addDefaultNotice() was called.\n")
      
        baseNotice = None

        for N in self._defaultNoticeTypes :
            if N.Brief == brief :
                baseNotice = N
                break

        if baseNotice is None :
            errorMessage="Request to addDefaultNotice for unknown Brief -  " + brief 
            log.error(errorMessage)
            for N in self._defaultNoticeTypes :
                if N.Brief == 'UnknownError' :
                    baseNotice = N
                    break
            if additionalInfo is None :
                additionalInfo = {}
            additionalInfo['commonServicerMessage']=errorMessage

        if scope is None :
            scope = baseNotice.Scope 
        if noticeType is None :
            noticeType = baseNotice.Type
        if code is None :
            code = baseNotice.Code
        if messenger is None :
            messenger = baseNotice.Messenger
        if message is None :
            message = baseNotice.Message

        self.addNotice(brief=brief, scope=scope, messenger=messenger, noticeType=noticeType, code=code, message=message, additionalInfo=additionalInfo)


    def addNotice(self,
            brief           : str,    # Lookup keyword for the error
            scope           : str,    # Is this from entity? service? transaction?
            messenger       : str,    # Which entity sends this message?
            noticeType      : str,    # Error, Warning, Info
            code            : str,    # Numeric code because those can be useful
            message         : str,    # Human-readable brief description
            additionalInfo  : Dict = None  # Free-form dictionary of data to return 
            ):
        log.info("addNotice() was called.\n")
        
        # Build the notice 
        thisNotice = Notice()
        thisNotice.Brief=brief
        thisNotice.Scope=scope
        thisNotice.Type=noticeType
        thisNotice.Code=code
        thisNotice.Message=message
        thisNotice.Messenger=messenger
        if additionalInfo is not None : 
            thisNotice.AdditionalInfo=additionalInfo
    
        if self.__root__ is None:
            self.__root__ : List[Notice] = []
        self.__root__.append(thisNotice)


def generateSchema():
    from pydantic.schema import schema
    print(Notices.schema_json(indent=2))


def showDefaultNotices():
    tempNotices=Notices()
    ##  Examples of other ways to output the default notice types
    #tempNotices.printDefaults(style='easyRead')
    #tempNotices.printDefaults(style='minified')
    ## Print the default notice types to the screen
    tempNotices.printDefaults(style='terse', sendTo='stdout')


def testDefaultNoticeAddition():
    tempNotices=Notices()
    #tempNotices.addDefaultNotice(brief='notKnownBrief')
    tempNotices.addDefaultNotice(brief='GemsError')
    tempNotices.printNotices(style='terse',sendTo='stdout')


if __name__ == "__main__":
    generateSchema()
    showDefaultNotices()
    testDefaultNoticeAddition()
    pass

