#!/usr/bin/env python3
from typing import Protocol

from docs.gemsModules.microcosm.common.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


####  Figure out how to make this easy to change for each entity
from docs.gemsModules.microcosm.common.main_settings import WhoIAm
####

## These are a little redundant in this simple example.
class serviceInputs (Protocol):
    entity : str

class serviceOutputs (Protocol):
    message : str


def marco (inputs : serviceInputs) -> serviceOutputs:
    log.debug(f"serviceInputs: {serviceInputs}")
    service_outputs = {}
    if inputs.entity == WhoIAm :
        service_outputs["message"]="Polo"
    else : 
        service_outputs["message"]="Marco request sent to wrong entity."
    return service_outputs
