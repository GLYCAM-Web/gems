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
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from typing import ForwardRef
from pydantic import BaseModel, Field, Json
from pydantic.schema import schema
from gemsModules.common import io as commonio
from gemsModules.project import io as projectio
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


class TransactionSchema(BaseModel):
    timestamp : str = None
    entity  : Entity = None
    project : projectio.Project = None
    options : Json[str] = None
#    project : Project = None
#    options : commonio.Tags = None

# ####
# ####  Container for use in the modules
# ####
class Transaction:
    """Holds information relevant to a delegated transaction"""
    incoming_string :str = None
    request_dict : {}  = None
    transaction_in : TransactionSchema = None
    transaction_out: TransactionSchema = None
    response_dict : {} = None
    outgoing_string : str = None

    def __init__(self, in_string):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        import json
        print("The in_string is: " + in_string)

        self.incoming_string = in_string
        print("The incoming_string is: " )
        print(self.incoming_string)

        self.request_dict = json.loads(self.incoming_string)
        print("The request_dict is: " )
        print(self.request_dict)

    def populate_transaction(self)

        self.transaction_in = TransactionSchema(**self.request_dict)
        print("The transaction_in is: " )
        print(self.transaction_in.json(indent=2))

    def build_outgoing_string(self):
        import json
        isPretty=False

#        ## TODO: read in whether the output should be pretty
#        # this might work:
#        if self.transaction_in.options is not None:
#            if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
#                isPretty = True
        log.info("build_outgoing_string() was called.")
        if self.response_dict is None:
            msg = "Transaction has no response_dict! request_dict: " + str(self.request_dict)
            #print("transaction.response_dict: " + str(self.response_dict))
            #print("transaction: " + str(self.__dict__))
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
                            self.response_dict['gems_project'][element] = str(self.response_dict['gems_project'][element])

                        #log.debug("~ valueType: " + str(type(self.response_dict['gems_project'][element])))
            try:
                if isPretty is True:
                    self.outgoing_string=json.dumps(self.response_dict, indent=4)
                else:
                    self.outgoing_string=json.dumps(self.response_dict)
            except Exception as error:
                log.error("There was a problem dumping the response_dict to string.")
                raise error


    def build_general_error_output(self, msg=None):
        if msg == None:
            msg = 'fix me there was an error'

        self.outgoing_string="{'entity':{'type':'commonServicer','responses':{'notice': " + msg + "}}}"
       # print("build_general_error_output was called. Still in development.")

#top_level_schema = schema([Entity, Project], title='A GemsModules Transaction')
def generateTransactionSchema():
    import json
    print(TransactionSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateTransactionSchema()
