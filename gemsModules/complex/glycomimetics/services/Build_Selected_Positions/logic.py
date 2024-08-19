from gemsModules.logging.logger import Set_Up_Logging

from .api import Build_Inputs, Build_Outputs

log = Set_Up_Logging(__name__)


def execute(inputs: Build_Inputs) -> Build_Outputs:
    service_outputs = Build_Outputs(pUUID=inputs.pUUID)
    
    return service_outputs