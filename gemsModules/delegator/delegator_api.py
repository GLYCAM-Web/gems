#!/usr/bin/env python3
import gemsModules.common.services as commonservices
from  gemsModules.common.entity import Entity as commonEntity
import gemsModules.common.common_api as commonio
import gemsModules.delegator.settings as delegatorsettings
from pydantic import Field
from typing import Dict, Optional
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class Delegator_Service(commonservices.Service) :
    typename: delegatorsettings.AvailableServices = Field(
        'Marco',
        alias='type',
        title='Service',
        description='A connectivity assurance service.'
    )

class Delegator_Services(commonservices.Services) :
    __root__ : Dict[str, Delegator_Service] = None

class Delegator_Entity(commonEntity) :
    services : Delegator_Services  = Field(
        Delegator_Services(),
        description='Services available from Delegator')

class Delegator_API(commonio.CommonAPI) :
    entity  : Delegator_Entity 
    class Config:
        title = 'gemsModulesDelegatorAPI'

class Delegator_Transaction(commonio.Transaction):
    transaction_in: Delegator_API = None
    transaction_out: Delegator_API = None

    def get_API_type(self):
        log.info("get_API_type was called from Delegator_Transaction")
        return Delegator_API

    def getEntityModuleName(self):
        return delegatorsettings.subEntities[self.transaction_in.entity.entityType].value

class Redirector_Entity(Delegator_Entity) :
    services : Optional[Dict] = None

class Redirector_API(Delegator_API):
    entity  : Redirector_Entity 
    project : Optional[Dict] = None
    class Config:
        title = 'gemsModulesDelegatorRedirectionAPI'

class Redirector_Transaction(Delegator_Transaction):
    transaction_in: Redirector_API = None
    transaction_out: Redirector_API = None

    def get_API_type(self):
        log.info("get_API_type was called from Redirector_Transaction")
        log.debug("the type of Redirector_API is: " + str(Redirector_API))
        return Redirector_API

def generateSchema():
    import json
    print(Delegator_Transaction.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()

