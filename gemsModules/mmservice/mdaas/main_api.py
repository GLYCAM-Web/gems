#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.mmservice.mdaas.main_settings import WhoIAm

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class MDaaS_Entity(main_api_entity.Entity) :

    entityType : Literal['MDaaS'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.mdaas
class MDaaS_API(main_api.Common_API):
    entity : MDaaS_Entity


class MDaaS_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return MDaaS_API


