#!/usr/bin/env python3
#
# ###############################################################
# ##
# ##  The gemsModules are being refactored.
# ##  
# ##  This file:
# ##
# ##      -  Will eventually hold the Transaction class
# ##      -  Might not be in full use by all modules
# ##
# ##  The modules/Entities that are partially or wholly 
# ##  changed so that they use this file are:
# ##
# ##      None yet.
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
from typing import ForwardRef
from pydantic import BaseModel, Field
from pydantic.schema import schema
from gemsModules.common import io as commonio
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class Entities(str, Enum):
    commonServices = 'CommonServices'
    delegator = 'Delegator'
    project = 'Project'
    sequence = 'Sequence'

class Entity(commonio.Entity):
    """Holds information about the main module responsible for a service."""
    entityType : Entities = Field(
            ...,
            title='Type',
            alias='type'
            )

##For the frontend project.
class Project(BaseModel):
    resources : List[commonio.Resource] = None
    options : commonio.Tags = None

class TransactionSchema(BaseModel):
    timestamp : str = None
    entity  : Entity
    project : Project = None
    options : commonio.Tags = None

# ####
# ####  Container for use in the modules
# ####
class Transaction:
    """Holds information relevant to a delegated transaction"""
    def __init__(self, incoming_string):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        self.incoming_string = incoming_string
        self.request_dict : {} = None
        self.transaction_in : TransactionSchema = None
        self.transaction_out : TransactionSchema = None
        self.response_dict : {} = None
        self.outgoing_string : str = None

    def build_outgoing_string(self):
        import json
        isPretty=False

#        ## TODO: read in whether the output should be pretty
#        # this might work:
#        if self.transaction_in.options is not None:
#            if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
#                isPretty = True
        log.info("build_outgoing_string() was called.")
        #log.debug("response_dict: \n" + str(self.response_dict))
        for key in self.response_dict.keys():
            #log.debug("key: " + key)
            #log.debug("valueType: " + str(type(self.response_dict[key])))
            if key == 'gems_project':
                #log.debug("\ngems_project: \n")
                for element in self.response_dict['gems_project'].keys():
                    #log.debug("~ element: " + element)
                    if type(self.response_dict['gems_project'][element]) != str:
                        self.response_dict['gems_project'][element] = str(self.response_dict['gems_project'][element])

                    #log.debug("~ valueType: " + str(type(self.response_dict['gems_project'][element])))
        try:
            if isPretty:
                self.outgoing_string=json.dumps(self.response_dict, indent=4)
            else:
                self.outgoing_string=json.dumps(self.response_dict)
        except Exception as error:
            log.error("There was a problem dumping the response_dict to string.")
            raise error


    def build_general_error_output(self):
        print("build_general_error_output was called. Still in development.")

#top_level_schema = schema([Entity, Project], title='A GemsModules Transaction')
def generateGemsModulesSchema():
    import json
    print(TransactionSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateGemsModulesSchema()
