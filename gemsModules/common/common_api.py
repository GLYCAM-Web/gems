#!/usr/bin/env python3
from pydantic import BaseModel, Field, validator
from gemsModules.project.project_api import Project as Project
from gemsModules.common.entity import Entity
from gemsModules.common.notices import Notices
from gemsModules.common.services_responses import Responses
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
#    incoming_string: str = None
#    inputs: CommonAPI = None
#    outputs: CommonAPI = None
#    outgoing_string: str = None

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
            self.populate_inputs(self.incoming_string, no_check_fields)
            if initialize_out :
                self.initialize_outputs_from_inputs()
            return 0
        except Exception as error:
            errMsg = "problem with call to parse_raw() while instantiating transaction with: " + str(in_string)
            log.error(errMsg)
            log.error(traceback.format_exc())
            self.generate_error_response(Brief='JsonParseEror',AdditionalInfo={'error': str(error)})
            return 1

    def initialize_outputs_from_inputs(self):
        log.info("initialize_outputs_from_inputs was called")
        self.outputs = self.get_API_type() 
        self.outputs = self.inputs.copy(deep=True)
        log.debug("The outputs is: ")
        log.debug(self.outputs.json(indent=2))

    @validator('*',check_fields=False)
    def populate_inputs_no_check_fields(self, in_string : str):
        self.inputs = self.get_API_type().parse_raw(in_string)

    def populate_inputs(self, 
        in_string : str, 
        no_check_fields=False):
        if in_string is None:
            raise Exception("in_string was None for populate_inputs")
        if no_check_fields:
            self.populate_inputs_no_check_fields(in_string)
        else: 
            self.inputs = self.get_API_type().parse_raw(in_string)
        log.debug("The inputs is: ")
        log.debug(self.inputs.json(indent=2))

    def process(self) :
        if self.inputs.entity.services.__root__ is None  or self.inputs.entity.services.__root__ == [] :
            self.doDefaultService()
        else :
            self.inputs.entity.services.process()

    def doDefaultService(self) :
        self.marco()

    def getEntityModuleName(self):
        return 'common'

    def marco(self) :
        if self.outputs is None :
            self.initialize_outputs_from_inputs()
        self.outputs.entity.responses = Responses()
        thisEntity = self.outputs.entity.entityType
        if self.outputs.entity.services is None or not self.outputs.entity.services.is_present('Marco') :
            self.outputs.entity.services.add_service(typename='Marco')
        self.outputs.entity.responses.add_response(
                typename = thisEntity,
                outputs = {'payload': 'Polo'})
        self.build_outgoing_string()

    def generate_error_response(self, Brief='UnknownError', EntityType=settings.WhoIAm, AdditionalInfo=None) :
        self.outputs = CommonAPI.construct(entity=Entity.construct(entityType=EntityType))
        self.outputs.notices.addDefaultNotice(Brief=Brief, Messenger=EntityType, AdditionalInfo=AdditionalInfo)
        self.build_outgoing_string()

    def getProjectIn(self):
        log.info("getProjectFromTransactionIn() was called.\n")
        try:
            if all(v is not None for v in [
                    self.inputs,
                    self.inputs.project]):
                log.debug("Found a non-None project in inputs of type : " +
                          str(type(self.inputs.project)))
                return self.inputs.project
            else:
                return None
        except Exception as error:
            log.error(
                "There was a problem getting the project from inputs :  " + str(error))
            raise error

    def getProjectOut(self):
        log.info("getProjectFromTransactionOut() was called.\n")
        try:
            if all(v is not None for v in [
                    self.outputs,
                    self.outputs.project]):
                log.debug("Found a non-None project in outputs of type : " +
                          str(type(self.outputs.project)))
                return self.outputs.project
            else:
                return None
        except Exception as error:
            log.error(
                "There was a problem getting the project from outputs :  " + str(error))
            raise error

    def build_outgoing_string(self, prettyPrint=False, indent=2, prune_empty_values=True) :
        if self.outputs.prettyPrint is True:
            prettyPrint = True
        if prettyPrint :
            self.outgoing_string = self.outputs.json(indent=2,exclude_none=prune_empty_values)
        else:
            self.outgoing_string = self.outputs.json(exclude_none=prune_empty_values)

    def get_outgoing_string(self):
        if self.outgoing_string is None or self.outgoing_string == "" :
            self.generate_error_response()
        return self.outgoing_string

def generateSchema():
    import json
    print(CommonAPI.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
