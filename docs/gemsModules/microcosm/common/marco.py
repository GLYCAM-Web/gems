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


def marco (serviceInputs) -> serviceOutputs:
    log.debug(f"serviceInputs: {serviceInputs}")
    service_outputs = {}
    if serviceInputs.entity == WhoIAm :
        service_outputs["message"]="Polo"
    else : 
        service_outputs["message"]="Marco request sent to wrong entity."
    return service_outputs


class test_inputs :
    entity : str = 'CommonServicer'
    random_other_thing: str = 'This is irrelevant input.'

if __name__== "__main__":
    service_outputs = marco(test_inputs)
    print(f"service_outputs: {service_outputs}")
