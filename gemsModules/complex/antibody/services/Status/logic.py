#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments
from pathlib import Path

from gemsModules.common.main_api_notices import Notices
from gemsModules.deprecated.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

from .api import Status_Inputs, Status_Outputs


log = Set_Up_Logging(__name__)

GLYCOMIMETICS_PROJECTS_ROOT = InstanceConfig().get_filesystem_path("AntibodyDocking")

# TODO: Determine project type, and return status of that project type
def execute(inputs: Status_Inputs) -> Status_Outputs:
    log.debug(f"Status resources at servicing: {inputs}")
    service_outputs = Status_Outputs()
    service_notices = Notices()

    return service_outputs, service_notices
    # DEPRECATED:
    
    # check for errors during evaluation
    evaluate_err = project_path / "evaluate.err"
    evaluation_log = project_path / "evaluation.log"
    
    non_empty_evaluate_err = evaluate_err.exists() and evaluate_err.stat().st_size > 0
    contains_success_str = False
    with open(evaluation_log, "r") as f:
        for line in f:
            if "Pdb2glycam matching successful." in line:
                contains_success_str = True
                break

    if non_empty_evaluate_err or not contains_success_str:
        service_outputs.status = "Failure"
        service_outputs.details = "Project failed during evaluation"
    else:
        service_outputs.status = "Success"
        service_outputs.details = "Project successfully evaluated"
            
    if main_status_txt.exists() and service_outputs.status != "Failure":
        with open(main_status_txt, "r") as f:
            for line in f:
                if "Simulations completed." in line:
                    service_outputs.status = "Success"
                    service_outputs.details = line
                    break
                elif "error" in line.lower():
                    service_outputs.status = "Failure"
                    service_outputs.details = line
                    break
                else:
                    service_outputs.status = "Pending"
                    service_outputs.details = line


    return service_outputs, service_notices
