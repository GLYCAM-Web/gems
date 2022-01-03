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
from uuid import UUID
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from pydantic import BaseModel, Field, Json
from pydantic.schema import schema
from gemsModules.project.jsoninterface import Project as Project
from gemsModules.common.notices import Notice
from gemsModules.common.resources import Resource
from gemsModules.common import settings

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)



class NoticeTypes(str, Enum):
    note = 'Note'
    warning = 'Warning'
    error = 'Error'
    exit = 'Exit'

# class Tags(BaseModel):
    # options : Dict[str,str] = Field(
    # None,
    #description='Key-value pairs that are specific to each entity, service, etc'
    # )


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
        description='Numeric code associated with this notice, for users who like this sort of thing.'
    )
    noticeBrief: str = Field(
        None,
        title='Brief',
        alias='brief',
        description='Brief title, status or name for this notice or notice type.'
    )
    noticeMessage: str = Field(
        None,
        title='Message',
        alias='message',
        description='A more detailed message for this notice.'
    )
    noticeScope: str = Field(
        None,
        title='Context of notice',
        alias='scope',
        description='The scope at which the error occured.'
    )
    messagingEntity: str = Field(
        None,
        title='Messaging Entity',
        description='The Entity that raised the notice, if known.'
    )
    additionalInfo: Dict[str, str] = Field(
        None,
        description='Key-value pairs that are specific to each entity, service, etc'
    )


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
    payload: Json[str] = Field(
        None,
        description='The thing that is described by the location and format'
    )
    notices: List[Notice] = None
    options: Dict[str, str] = Field(
        None,
        description='Key-value pairs that are specific to each entity, service, etc'
    )

    def generateCommonParserNotice(self, *args, **kwargs):
        self.notices.append(
            settings.generateCommonParserNotice(*args, **kwargs))

# ## Services
# ##


class Services(str, Enum):
    errorNotification = 'ErrorNotification'
    status = 'Status'


class Service(BaseModel):
    """
    Holds information about a requested Service.
    This object will have different forms in each Entity.
    """
    typename: Services = Field(
        'Status',
        alias='type',
        title='Common Services',
        description='The service requested of the Common Servicer'
    )
    givenName: str = Field(
        None,
        title='The name given this object in the transaction'
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

# ## TODO - consider putting Response inside of Service
# ##        I keep changing my mind.   - Lachele


class Response(Service):
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
    outputs : Json = None
    notices : List[Notice] = None


class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType : str = Field(
            settings.WhoIAm,
            title='Type',
            alias='type'
            )
    requestID : str = Field(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    services : Dict[str,Service] = None
    responses : Dict[str,Response] = None
    resources : List[Resource] = None
    notices : List[Notice] = None
    options : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )


class TransactionSchema(BaseModel):
    timestamp : str = None
    entity  : Entity = None
    project : Project = None
    prettyPrint : bool = False
    mdMinimize : bool = True
    options : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )
    notices : List[Notice] = []
    class Config:
        title = 'gemsModulesCommonTransaction'

    def generateCommonParserNotice(self, *args, **kwargs):
        self.notices.append(
            settings.generateCommonParserNotice(*args, **kwargs))

# ####
# ####  Container for use in the modules
# ####


class Transaction:
    """Holds information relevant to a delegated transaction"""
    incoming_string: str = None
    request_dict: {} = None
    transaction_in: TransactionSchema
    transaction_out: TransactionSchema
    response_dict: {} = None
    outgoing_string: str = None

    def __init__(self, in_string):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        import json
        # ## I think it is wrong to have Transaction call something from
        # ## some other place to modify itself, but I don't have time to
        # ## refactor this all to make it right.  Lachele 2021-04-02
        from gemsModules.common import settings as commonSettings

        # The following debug line is sometimes useful, but normally redundant.
        #log.debug("The in_string is: " + in_string)
        self.incoming_string = in_string
        # The following debug lines are also sometimes useful, but normally redundant.
        # log.debug("The incoming_string is: " )
        # log.debug(self.incoming_string)
        if self.incoming_string is None :
            self.transaction_out = TransactionSchema()
            self.transaction_out.generateCommonParserNotice(noticeBrief='InvalidInput', messagingEntity=commonSettings.WhoIAm)
            return
        else : 
            self.request_dict = json.loads(self.incoming_string) 


    def generateCommonParserNotice(self, *args, **kwargs):
        if self.transaction_out is None:
            self.transaction_out = TransactionSchema()
        self.transaction_out.generateCommonParserNotice(*args, **kwargs)

    def populate_transaction_in(self):

        self.transaction_in = TransactionSchema(**self.request_dict)
        log.debug("The transaction_in is: ")
        log.debug(self.transaction_in.json(indent=2))

    def getProjectIn(self):
        log.info("getProjectFromTransactionIn() was called.\n")
        try:
            if all(v is not None for v in [
                    self.transaction_in,
                    self.transaction_in.project]):
                log.debug("Found a non-None project in transaction_in of type : " +
                          str(type(self.transaction_in.project)))
                return self.transaction_in.project
            else:
                return None
        except Exception as error:
            log.error(
                "There was a problem getting the project from transaction_in :  " + str(error))
            raise error

    def getProjectOut(self):
        log.info("getProjectFromTransactionOut() was called.\n")
        try:
            if all(v is not None for v in [
                    self.transaction_out,
                    self.transaction_out.project]):
                log.debug("Found a non-None project in transaction_out of type : " +
                          str(type(self.transaction_out.project)))
                return self.transaction_out.project
            else:
                return None
        except Exception as error:
            log.error(
                "There was a problem getting the project from transaction_out :  " + str(error))
            raise error

    def getSchemaLocation():
        thisProject = self.getProjectOut()
        return thisProject.getFilesystemPath()



    ######
    # This needs to change to look like the method in sequence.io
    ######

    def build_outgoing_string(self):
        import json
        isPretty=False
        log.info("build_outgoing_string() was called.")
        if self.response_dict is None:
            msg = "Transaction has no response_dict! request_dict: " + \
                str(self.request_dict)
            self.build_general_error_output(msg)
        else:
            #log.debug("response_dict: \n" + str(self.response_dict))
            for key in self.response_dict.keys():
                #log.debug("key: " + key)
                #log.debug("valueType: " + str(type(self.response_dict[key])))
                if key == 'gems_project':
                    #log.debug("\ngems_project: \n")
                    for element in self.response_dict['gems_project'].keys():
                        #log.debug("~ element: " + element)
                        if type(self.response_dict['gems_project'][element]) != str:
                            self.response_dict['gems_project'][element] = str(
                                self.response_dict['gems_project'][element])

                        #log.debug("~ valueType: " + str(type(self.response_dict['gems_project'][element])))
            try:
                if isPretty is True:
                    self.outgoing_string = json.dumps(
                        self.response_dict, indent=4)
                else:
                    self.outgoing_string = json.dumps(self.response_dict)
            except Exception as error:
                log.error(
                    "There was a problem dumping the response_dict to string.")
                raise error

    
    def build_general_error_output(self, msg=None):
        if msg == None:
            msg = 'fix me there was an error'

        self.outgoing_string = "{'entity':{'type':'commonServicer','responses':{'notice': " + msg + "}}}"


def generateSchema():
    import json
    # print(Service.schema_json(indent=2))
    print(TransactionSchema.schema_json(indent=2))


if __name__ == "__main__":
    generateSchema()
