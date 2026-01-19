#!/usr/bin/env python3
from pydantic import BaseModel
from abc import ABC, abstractmethod
from ..project.main_api import Project 
from .main_api_entity import Entity
from .main_api_notices import Notices
from . import settings_main
import traceback

from . import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


class Common_API(BaseModel):
    timestamp : str = None
    entity  : Entity       # The only required part of the JSON is the entity.
    project : Project = None
    notices : Notices = Notices()
    prettyPrint : bool = False


class Transaction(ABC):

    @abstractmethod
    def get_API_type(self):  # This allows dependency injection in the children
        return Common_API
        ## If you want to use the schema from this abstract parent without having
        ##    to hand-code 'Common_API", you can do this:
        ##
        ##    return super().get_API_type()
        ##
        ## To check that it does what you think, you can do something like this:
        ##
        ##    __super__ = super().get_API_type()
        ##    print("The api type is " + str(__super__))

    def __init__(self):
        self.incoming_string : str = None
        self.inputs : self.get_API_type() = None
        self.outputs : self.get_API_type() = None
#        self.inputs : Common_API = None
#        self.outputs : Common_API = None
        self.outgoing_string : str = None

    def process_incoming_string(self,
            in_string : str,  # The JSON input string 
            no_check_fields=False, # Do not perform a check of fields vs schema using Pydantic 
            initialize_out=True # Initialize an outgoing transaction from the incoming one
            ):
        try:
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
            errMsg = "problem processing this string: " + str(in_string)
            log.error(errMsg)
            log.error(error)
            log.error(traceback.format_exc())
            self.generate_error_response(Brief='JsonParseEror',AdditionalInfo={'error': str(errMsg)})
            print("problem processing this string: " + str(in_string))
            print("the error message is: ")
            print(error)
            return 1

    def populate_inputs(self, in_string : str, no_check_fields=False):
        self.inputs = self.get_API_type().parse_raw(in_string)
        log.debug("The inputs is: ")
        log.debug(self.inputs.json(indent=2))

    def initialize_outputs_from_inputs(self):
        log.info("initialize_outputs_from_inputs was called")
        self.outputs = self.get_API_type() 
        self.outputs = self.inputs.copy(deep=True)

    # the use of EntityType here will break elsewhere, I think
    def generate_error_response(self, Brief='UnknownError', EntityType=settings_main.WhoIAm, AdditionalInfo=None) :
        self.outputs = self.get_API_type().construct(entity=Entity.construct(entityType=EntityType))
        self.outputs.notices.addDefaultNotice(Brief=Brief, Messenger=EntityType, AdditionalInfo=AdditionalInfo)
        self.build_outgoing_string()

    def build_outgoing_string(self, prettyPrint=False, indent=2, prune_empty_values=True) :
        if self.outputs.prettyPrint is True:  # In case outputs.prettyPrint is None or something else that isn't useful
            prettyPrint = True
        if prettyPrint :
            self.outgoing_string = self.outputs.json(indent=2,exclude_none=prune_empty_values)
        else:
            self.outgoing_string = self.outputs.json(exclude_none=prune_empty_values)

    def get_outgoing_string(self, prettyPrint=False, indent=2, prune_empty_values=True) :
        if self.outgoing_string is None or self.outgoing_string == "" :
            try:
                self.build_outgoing_string(self, prettyPrint, indent, prune_empty_values) 
            except Exception as error:
                self.generate_error_response()
        return self.outgoing_string

    def get_input_services(self):
        return self.inputs.entity.services

    def generate_schema(self):
        return self.get_API_type().schema_json(indent=2)

def generateSchema():
    print(Common_API.schema_json(indent=2))
