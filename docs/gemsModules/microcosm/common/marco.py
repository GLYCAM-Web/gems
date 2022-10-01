#!/usr/bin/env python3
from typing import Protocol

from .logger import Set_Up_Logging
log = Set_Up_Logging(__name__)  ## will this break?

## These are a little redundant in this simple example.
class serviceInputs (Protocol):
    entity : str
    who_I_am : str 

class serviceOutputs (Protocol):
    message : str


# Make this an ABC so that the WhoIAm can be set by a made-concrete abstract method?
def marco (inputs : serviceInputs) -> serviceOutputs:
    log.debug(f"serviceInputs: {serviceInputs}")
    service_outputs = {}
    # The who_I_am must be set in the options.
    if inputs.entity == inputs.who_I_am :  # trivial here, but could be more complex (search a dictionary, etc.).
        service_outputs["message"]="Polo"
    else : 
        service_outputs["message"]="Marco request sent to wrong entity. See who_I_am in options."
    return service_outputs
