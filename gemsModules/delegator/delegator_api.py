#!/usr/bin/env python3
import traceback
import gemsModules.common.services as commonservices
from  gemsModules.common.entity import Entity as commonEntity
import gemsModules.common.common_api as commonio
import gemsModules.project.project_api as projectio
import gemsModules.delegator.settings as delegatorsettings
from pydantic import Field
from typing import List
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class DelegatorService(commonservices.Service) :
    typename: delegatorsettings.AvailableServices = Field(
        'Marco',
        alias='type',
        title='Service',
        description='A service available from Delegator'
    )


class DelegatorServices(commonservices.Services) :
    __root__ : List[DelegatorService]

class DelegatorEntity(commonEntity) :
    Services : DelegatorServices


class DelegatorAPI(commonio.TransactionSchema):
    Entity : DelegatorEntity


class Transaction(commonio.Transaction):
    """
    Storage for the input and output (the transaction) relevant to 
    interaction via GEMS API.  Handling of the string prior to first
    initialization of this class is usually the domain of delegator.
    """
    incoming_string: str = None
    transaction_in: DelegatorAPI = None
    transaction_out: DelegatorAPI = None
    outgoing_string: str = None

    def getEntityModuleName(self):
        return delegatorsettings.subEntities[self.transaction_in.entity.entityType].value



def generateSchema():
    import json
    print(Transaction.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()

