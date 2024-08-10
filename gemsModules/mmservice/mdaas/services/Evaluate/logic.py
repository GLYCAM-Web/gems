#!/usr/bin/env python3
from pathlib import Path
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.mmservice.mdaas.tasks import calculate_time_est_from_parm7
from gemsModules.mmservice.mdaas.services.Evaluate.api import (
    Evaluate_Inputs,
    Evaluate_Outputs,
)
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: decouple from run md/implied translation/rdf fill to get the unminimized-gas.parm7 for day calc
#@validate_arguments
def execute(inputs: Evaluate_Inputs) -> Evaluate_Outputs:
    log.debug(f"MDaaS/Evaluate input resources: {inputs.resources}")
    service_outputs = Evaluate_Outputs()

    for resource in inputs.resources:
        if resource.resourceRole == "parameter-topology":
            content = resource.get_payload(decode=True)
            log.debug(f"MDaaS/Evaluate parameter-topology-file content: {type(content)}")
                
            time_est_hours, num_particles = calculate_time_est_from_parm7.execute(content, float(inputs.sim_length))
            r = Resource(
                    payload=time_est_hours,
                    resourceFormat="float",
                    resourceRole="timeEstimateHours", # resourceRole="timeEstimateHours",
                    locationType="Payload",
                )
            r.notices.addSimpleInfoNotice(
                f"Estimated time to run: {time_est_hours} hours to simulate {num_particles} particles for {inputs.sim_length} ns."
            )
            service_outputs.resources.add_resource(r)
    return service_outputs
