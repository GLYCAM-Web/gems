#!/usr/bin/env python3
from typing import  Literal
from pydantic import BaseModel, Field, typing
from gemsModules.common.main_api_services import Service, Response
from gemsModules.delegator.redirector_settings import Known_Entities

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class known_entity_Outputs(BaseModel) :
    knownEntities : list[str]  = Field(
        None,
        description="The response to the Marco request.")

class known_entity_Service(Service) :
    typename : Literal["KnownEntities"] = Field(...)
    inputs : typing.Any = None

class known_entity_Response(Response) :
    typename : str  = "KnownEntities"
    outputs : known_entity_Outputs =  Known_Entities.get_value_list()


#the_response=known_entity_Response()

#print(the_response.json(indent=2))

#print(known_entity_Response.schema_json(indent=2))
