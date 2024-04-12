#!/usr/bin/env python3
from abc import ABC
from pydantic import BaseModel, Field
from typing import Dict, Union, Optional

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.main_api_procedural_options import Procedural_Options
from gemsModules.common.main_api_services import Service_Requests, Service_Responses
from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Entity(ABC, BaseModel):
    """Holds information about the main object responsible for a service."""

    entityType: str = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    inputs: Union[Dict, Resources] = Field(
        None,
        title="Inputs",
        description="User-friendly, top-level inputs to the services.",
    )
    outputs: Union[Dict, Resources] = Field(
        None,
        title="Inputs",
        description="User-friendly, top-level outputs from the services.",
    )
    services: Service_Requests = Service_Requests()
    responses: Service_Responses = Service_Responses()
    notices: Optional[Notices] = Notices()
    procedural_options: Procedural_Options = Procedural_Options()
    options: Dict[str, str] = Field(
        None,
        description="Key-value pairs that are specific to each entity, service, etc",
    )


def generateSchema():
    print(Entity.schema_json(indent=2))
