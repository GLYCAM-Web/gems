#!/usr/bin/env python3
from typing import Dict #, List, Optional, Sequence, Set, Tuple, Union, Any
from pydantic import BaseModel, Field
from gemsModules.project.jsoninterface import Project as Project
from gemsModules.common.notices import Notices
from gemsModules.common import settings
from gemsModules.common.entity import Entity

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


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
    notices : Notices = Notices()
    class Config:
        title = 'gemsModulesCommonTransaction'

class Transaction:
    """Holds information relevant to a delegated transaction"""
    incoming_string: str = None
    transaction_in: TransactionSchema
    transaction_out: TransactionSchema
    outgoing_string: str = None

    def __init__(self, 
        in_string="", 
        allow_empty_string=False,
        no_check_fields=False, 
        initialize_out=True):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        log.info("called __init__ for Transaction")

        try:

            from gemsModules.common import settings as commonSettings
            self.incoming_string = in_string
            log.debug("incoming string is: " + str(in_string))
            if self.incoming_string is None or self.incoming_string == '':
                if allow_empty_string:
                    log.debug("allow_empty_string was True, so returning")
                    return 0
                else:
                    log.error("incoming string was empty")
                    self.transaction_out = TransactionSchema()
                    self.transaction_out.entity.entityType = settings.WhoIAm
                    self.transaction_out.notices.addDefaultNotice(Brief='InvalidInput')
                    self.build_outgoing_string()
                    #raise Exception("incoming string was empty") #is this useful?
                    return 1
            try:
                self.populate_transaction_in(in_string, no_check_fields)
                if initialize_out:
                    self.initialize_transaction_out_from_transaction_in()
                return 0
            except Exception as error:
                log.error("Error parsing incoming string: " + str(error))
                self.transaction_out = TransactionSchema()
                self.transaction_out.notices.addDefaultNotice(
                    Brief='JsonParseEror', 
                    Messenger=commonSettings.WhoIAm,
                    AdditionalInfo={"errorMessage": "The incoming string could not be parsed."})
                self.build_outgoing_string()
                errMsg = "problem with call to parse_raw() while instantiating transaction with: " + str(in_string)
                log.error(errMsg)
                log.error(traceback.format_exc())
                return 1
        except Exception as error:
            errMsg = "problem with call to __init__() while instantiating transaction with: " + str(in_string)
            log.error(errMsg)
            log.error("Error: " + str(error))
            log.error(traceback.format_exc())
            self.transaction_out = TransactionSchema()
            self.transaction_out.notices.addDefaultNotice(
                Brief='UnknownError', 
                Messenger=settings.WhoIAm,
                AdditionalInfo={"errorMessage": "The transaction could not be initialized from the incoming string."})
            self.build_outgoing_string()
            return 1

    def initialize_transaction_out_from_transaction_in(self):
        log.info("initialize_transaction_out_from_transaction_in was called")
        self.transaction_out = self.transaction_in.copy(deep=True)
        log.debug("The transaction_out is: ")
        log.debug(self.transaction_out.json(indent=2))

    def populate_transaction_in(self, 
        in_string : str, 
        no_check_fields=False):
        if in_string is None:
            raise Exception("in_string was None")
        if no_check_fields:
            self.transaction_in = TransactionSchema.parse_raw(
                in_string,
                check_fields=False)
        else: 
            self.transaction_in = TransactionSchema.parse_raw(in_string)
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

    def build_outgoing_string(self):
        if self.transaction_out.prettyPrint is True:
            self.outgoing_string = self.transaction_out.json(indent=2)
        else:
            self.outgoing_string = self.transaction_out.json()

def generateSchema():
    import json
    print(TransactionSchema.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
