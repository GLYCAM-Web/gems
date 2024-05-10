#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.systemoperations.instance_config import InstanceConfig

from .api import Validate_Inputs, Validate_Outputs

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Validate_Inputs) -> Validate_Outputs:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Validate_Outputs()

    ic = InstanceConfig()

    has_cocomplex_input = False
    has_moiety_metadata = False
    has_execution_parameters = False
    for resource in inputs.resources:
        if resource.resourceRole == "cocomplex-input":
            has_cocomplex_input = True
        elif resource.resourceRole == "moiety-metadata":
            has_moiety_metadata = True
        elif resource.resourceRole == "execution-parameters":
            has_execution_parameters = True
        else:
            log.warning(f"Unknown resource role: {resource.resourceRole}")

    if not (has_cocomplex_input and has_moiety_metadata and has_execution_parameters):
        service_outputs.isValid = False
        service_outputs.outputDirPath = None
    else:
        service_outputs.isValid = True
        # For validate, there is no pUUID input / output dir at the moment,
        # but the sooner we create a project, the better.
        # service_outputs.outputDirPath = ic.get_output_dir() / inputs.pUUID
    return service_outputs
