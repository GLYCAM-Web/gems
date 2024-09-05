#!/usr/bin/env python3
import os
from pathlib import Path
import sys
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Evaluate_Inputs, Evaluate_Outputs
from ..common_api import Modification_Position

from ...tasks import evaluate_wrapper

log = Set_Up_Logging(__name__)


# Not working.
@validate_arguments
def execute(inputs: Evaluate_Inputs) -> Evaluate_Outputs:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Evaluate_Outputs()
    service_notices = Notices()

    receptor_pdb_resource = None
    for resource in inputs.resources:
        if resource.resourceRole == "Receptor":
            receptor_pdb_resource = resource
            break

    if not receptor_pdb_resource:
        # Append a notice, we can do nothing else.
        service_notices.addNotice(
            Brief="No Receptor PDB Resource",
            Scope="Service",
            Messenger="Glycomimetics",
            Type="Info",
            Code="600",
            Message="No Receptor PDB was provided to Glycomimetics, nothing to do.",
        )
    else:
        # Evaluation
        result = None
        if receptor_pdb_resource.locationType != "filesystem-path-unix":
            service_notices.addNotice(
                Brief="current Receptor PDB Resource Location type not supported",
                Scope="Service",
                Messenger="Glycomimetics",
                Type="Error",
                Code="601",
                Message="Receptor PDB Resource must be a filesystem path.",
            )
        else:
            pdb_fpath = receptor_pdb_resource.payload

            if Path(pdb_fpath).exists():
                working_dir = str(Path(pdb_fpath).parent)

                log.debug(
                    f"Receptor PDB file found: {pdb_fpath}, working_dir: {working_dir}"
                )
                try:
                    # To ensure various output files are written to the correct directory.
                    parent_dir = str(Path(pdb_fpath).parent)
                    pdb_filename = Path(pdb_fpath).name
                    
                    available_positions = evaluate_wrapper.execute(parent_dir, pdb_filename)

                    for pos in available_positions:
                        service_outputs.Available_Modification_Options.append(pos)
                    log.debug(
                        f"Available_Modification_Options: {service_outputs.Available_Modification_Options}"
                    )
                except Exception as e:
                    service_notices.addNotice(
                        Brief="Error during Evaluation",
                        Scope="Service",
                        Messenger="Glycomimetics",
                        Type="Error",
                        Code="602",
                        Message=f"Error during Evaluation: {e}",
                    )
                    
                # TODO: swig wrap or recover results from evaluation.log
                log.debug(f"Evaluation Result: {None}")
            else:
                log.debug(f"Receptor PDB file not found: {pdb_fpath}")

    log.debug(f"service_outputs: {service_outputs}")
    return service_outputs, service_notices
