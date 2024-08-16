#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Validate_Inputs, Validate_Outputs


log = Set_Up_Logging(__name__)


def execute(inputs: Validate_Inputs) -> Validate_Outputs:
    log.debug(f"Validate resources at servicing: {inputs}")
    service_outputs = Validate_Outputs()
    service_notices = Notices()

    # TODO: Handle pUUID
    # if inputs.pUUID:
    #     pass

    hasReceptorResource = False
    for resource in inputs.resources:
        if resource.resourceRole == "Receptor":
            hasReceptorResource = True

    if not hasReceptorResource:
        service_notices.addNotice(
            Brief="No Receptor PDB Resource",
            Scope="Service",
            Messenger="Glycomimetics",
            Type="Error",
            Code="600",
            Message="No Receptor PDB was provided to Glycomimetics.",
        )
        service_outputs.isValid = False
    else:
        # TODO: We need to check it's an actual PDB now. PDB Preprocessor?
        service_outputs.isValid = True

    log.debug(f"service_outputs: {service_outputs}")
    return service_outputs, service_notices
