#!/usr/bin/env python3
from pydantic import BaseModel, Field, validator
from gemsModules.project.project_api import Project as Project
from gemsModules.common.entity import Entity
from gemsModules.common.notices import Notices
from gemsModules.common.services import Responses
from gemsModules.common.options import Options
from gemsModules.common import settings
import traceback

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


class CommonAPI(BaseModel):
    timestamp : str = None
    entity  : Entity 
    project : Project = None
    prettyPrint : bool = False
    mdMinimize : bool = True
    options : Options = Field(
            Options(),
            description='Key-value pairs that are specific to each entity, service, etc'
            )
    notices : Notices = Notices()
    class Config:
        title = 'gemsModulesCommonTransaction'

class Transaction:
    """
    Storage for the input and output (the transaction) relevant to 
    interaction via GEMS API.  Handling of the string prior to first
    initialization of this class is usually the domain of delegator.
    """
    incoming_string: str = None
    transaction_in: CommonAPI = None
    transaction_out: CommonAPI = None
    outgoing_string: str = None

    def get_API_type(self):
        return CommonAPI

    def process_incoming_string(self, 
            in_string : str,  # The JSON input string 
            no_check_fields=False, # Do not perform a check of fields vs schema using Pydantic 
            initialize_out=True # Initialize an outgoing transaction from the incoming one
            ):
        try:
            from gemsModules.common import settings as commonSettings
            log.debug("incoming string is: " + str(in_string))
            self.incoming_string = in_string
            if self.incoming_string is None or self.incoming_string == '':
                log.error("incoming string was empty")
                self.generate_error_response(Brief='InvalidInput')
                return 1
            self.populate_transaction_in(self.incoming_string, no_check_fields)
            if initialize_out :
                self.initialize_transaction_out_from_transaction_in()
            return 0
        except Exception as error:
            errMsg = "problem with call to parse_raw() while instantiating transaction with: " + str(in_string)
            log.error(errMsg)
            log.error(traceback.format_exc())
            self.generate_error_response(Brief='JsonParseEror',AdditionalInfo={'error': str(error)})
            return 1

    def initialize_transaction_out_from_transaction_in(self):
        log.info("initialize_transaction_out_from_transaction_in was called")
        self.transaction_out = self.get_API_type() 
        self.transaction_out = self.transaction_in.copy(deep=True)
        log.debug("The transaction_out is: ")
        log.debug(self.transaction_out.json(indent=2))

    @validator('*',check_fields=False)
    def populate_transaction_in_no_check_fields(self, in_string : str):
        self.transaction_in = self.get_API_type().parse_raw(in_string)

    def populate_transaction_in(self, 
        in_string : str, 
        no_check_fields=False):
        if in_string is None:
            raise Exception("in_string was None for populate_transaction_in")
        if no_check_fields:
            self.populate_transaction_in_no_check_fields(in_string)
        else: 
            self.transaction_in = self.get_API_type().parse_raw(in_string)
        log.debug("The transaction_in is: ")
        log.debug(self.transaction_in.json(indent=2))

    def process(self) :
        if self.transaction_in.entity.services.__root__ is None  or self.transaction_in.entity.services.__root__ == [] :
            self.doDefaultService()
        else :
            self.transaction_in.entity.services.process()

    def doDefaultService(self) :
        self.marco()

    def getEntityModuleName(self):
        return 'common'

    def marco(self) :
        if self.transaction_out is None :
            self.initialize_transaction_out_from_transaction_in()
        self.transaction_out.entity.responses = Responses()
        thisEntity = self.transaction_out.entity.entityType
        if self.transaction_out.entity.services is None or not self.transaction_out.entity.services.is_present('Marco') :
            self.transaction_out.entity.services.add_service(typename='Marco')
        self.transaction_out.entity.responses.add_response(
                typename = thisEntity,
                outputs = {'payload': 'Polo'})
        self.build_outgoing_string()

    def generate_error_response(self, Brief='UnknownError', EntityType=settings.WhoIAm, AdditionalInfo=None) :
        self.transaction_out = CommonAPI.construct(entity=Entity.construct(entityType=EntityType))
        self.transaction_out.notices.addDefaultNotice(Brief=Brief, Messenger=EntityType, AdditionalInfo=AdditionalInfo)
        self.build_outgoing_string()

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

    def build_outgoing_string(self, prettyPrint=False, indent=2, prune_empty_values=True) :
        if self.transaction_out.prettyPrint is True:
            prettyPrint = True
        if prettyPrint :
            self.outgoing_string = self.transaction_out.json(indent=2,exclude_none=prune_empty_values)
        else:
            self.outgoing_string = self.transaction_out.json(exclude_none=prune_empty_values)

    def get_outgoing_string(self):
        if self.outgoing_string is None or self.outgoing_string == "" :
            self.generate_error_response()
        return self.outgoing_string

def generateSchema():
    import json
    print(CommonAPI.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
