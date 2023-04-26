#!/usr/bin/env python3
from typing import Protocol, Dict, Optional

from gemsModules.common.tasks import cake

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

## These are a little redundant in this simple example.
class requestInputs:  
    """Defines the inputs to the service."""
    entity : str
    who_I_am : str 

class responseOutputs:
    """Defines the outputs from the service."""
    message : str
    info : Optional[str] = None

class serviceInputs (Protocol):
    """Allows a Service_Request to be used as input"""
    inputs : requestInputs
    options : Dict[str,str]

class serviceOutputs:
    outputs : responseOutputs

class cakeInputs:
    cake : bool = False
    color : str = None

# Make this an ABC so that the WhoIAm can be set by a made-concrete abstract method?
def execute(inputs : serviceInputs) -> serviceOutputs:
    log.debug(f"serviceInputs: {serviceInputs}")
    service_outputs = serviceOutputs()
    # The who_I_am must be set in the options.
    if inputs.entity == inputs.who_I_am :  # trivial here, but could be more complex (search a dictionary, etc.).
        service_outputs.outputs["message"]="Polo"
    else : 
        service_outputs.outputs["message"]="Marco request sent to wrong entity. See who_I_am in info."
    if inputs.options is not None :
        cake_inputs = cakeInputs()
        docake=False
        if 'cake' in inputs.options.keys() :
            docake=True
            cake_inputs.cake = inputs.options['cake']
        if 'color' in inputs.options.keys() :
            docake=True
            cake_inputs.color = inputs.options['color']
        if docake == True :
            service_outputs.outputs.info = cake.execute(cake_inputs)
    return service_outputs
