#!/usr/bin/env python3
from pathlib import Path
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.mmservice.mdaas.tasks import calculate_days_per_ns
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

    # TODO:Grayson Hack to fix ASAP (we have a fix!)
    # This also ends up duplicating work that was done by other services. 
    # The fix we have would allow us to add the unmin gas as a resource to avoid specifically iterating
    # the resources to find it.
    ug_resource_parent = None  # Part of hack below, TODO: REMOVE
    for resource in inputs.resources:
        # Hack to resolve the unminimized-gas.parm7 file from the parent sequence project.
        if (
            resource.locationType == "filesystem-path-unix"
            and resource.resourceFormat == "AMBER-7-prmtop" or resource.resourceFormat == "AMBER-7-restart"
            and ug_resource_parent is None
        ):
            log.debug(f"resource.payload: {resource.payload}")
            ug_resource_parent = Path(resource.payload).parent

    log.debug(f"ug_resource_parent: {ug_resource_parent}")
    if ug_resource_parent:
            ug_path = ug_resource_parent / "unminimized-gas.parm7"
            # this file isn't actually necessary for MDaaS, but tasks/set_up_run_md_directory used by the RunMD service
            # will symlink it if it exists in the MD Project.
            if ug_path.exists():
                time_est_hours, num_particles = calculate_days_per_ns.execute(ug_path, float(inputs.sim_length))
                r = Resource(
                        payload=time_est_hours,
                        resourceFormat="float",
                        type="timeEstimateHours", # resourceRole="timeEstimateHours",
                        locationType="Payload",
                    )
                r.notices.addSimpleInfoNotice(
                    f"Estimated time to run: {time_est_hours} days for ({num_particles}) particles"
                )
                service_outputs.resources.add_resource(
                    r
                )
    return service_outputs
