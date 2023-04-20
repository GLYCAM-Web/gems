#!/usr/bin/env python3
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator, Json
from typing import Any, Dict, List, Union

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)



class Procedural_Options(ABC, BaseModel):
    context : str = Field(
            "unset",
            description="Is the user a normal user (default) or a website?  Is set automatically but can be overridden in some contextx."
            )
    force_serial_execution : bool = Field(
            False,
            description="Should GEMS execute serially (no daemons, no parallel)?  Note that this only affects GEMS, not any programs called by GEMS."
            )

    @validator('context', pre=True, always=True)
    def enforce_website_context(cls, v, values, **kwargs):
        from gemsModules.deprecated.common.logic import getGemsExecutionContext
        apparent_context : str = getGemsExecutionContext()
        if 'context' not in values :
            return apparent_context
        if apparent_context == 'website':
            if values['context'] != apparent_context :
                log.debug("Incoming context does not match environment.  Setting to 'website'.")
                return apparent_context
        return v

    @validator('force_serial_execution', pre=True, always=True)
    def enforce_environment_serial_execution_flag(cls, v, values, **kwargs):
        from gemsModules.deprecated.common.logic import getGemsEnvironmentForceSerialExecution
        the_flag : str =getGemsEnvironmentForceSerialExecution()
        if the_flag == 'unset':
            return v
        if the_flag.lower() == 'true':
            return True
        elif the_flag.lower() == 'false':
            return False
        raise ValueError ("Cannot interpret value set for GEMS_FORCE_SERIAL_EXECUTION from the environment.")


