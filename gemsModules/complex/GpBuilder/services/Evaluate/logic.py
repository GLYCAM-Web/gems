#!/usr/bin/env python3
from typing import Optional
from pathlib import Path
from pydantic import validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.main_api_resources import Resource
from gemsModules.logging.logger import Set_Up_Logging

from .api import Evaluate_Inputs, Evaluate_Outputs, Evaluate_Options, Glycosite
from ...main_api_project import GpBuilderProject

from  ...tasks import generate_input_file
from ...tasks.run_gpbuilder import execute_gpbt_wrapper


log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Evaluate_Inputs, options: Optional[Evaluate_Options]) -> tuple[Evaluate_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Evaluate_Outputs()
    service_notices = Notices()

    workdir = GpBuilderProject.get_project_dir_from_pUUID(inputs.pUUID)
    log.debug(f"workdir: {workdir}")
    if not workdir:
        service_notices.addNotice(
            Brief="Project not found",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="400",
            Message="Project not found",
        )
        return service_outputs, service_notices
                
    # This generates the glycosites to choose from for GpBuilder
    output_csv = workdir / "the_glycosites.csv"
    gpbt_failed = execute_gpbt_wrapper(
        # TODO: ensure we're using pdb file from the project directory
        inputs.protein_file,
        output_csv,
    )
    
    # Update the glycosites in the api response from the output CSV
    service_outputs.csv_path = str(output_csv)
    with open(output_csv, 'r') as f:
        for line in f: 
            if any([x in line for x in ["Chain", "ResidueNumber", "InsertionCode", "SequenceContext", "Tags"]]):
                continue # Skip the header line safely. (In case it's not generated)
            if line.startswith("#"):
                continue
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            glycosite = Glycosite(
                Chain=parts[0],
                ResidueNumber=parts[1],
                InsertionCode=parts[2] if len(parts) > 2 else "",
                SequenceContext=parts[3] if len(parts) > 3 else "",
                Tags=parts[4] if len(parts) > 4 else ""
            )
            service_outputs.glycosites.append(glycosite)
    log.debug(f"Found {len(service_outputs.glycosites)} glycosites in the CSV.")

    if gpbt_failed:
        service_notices.addNotice(
            Brief="Evaluation Failed",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="500",
            Message=f"Evaluation Failed: {gpbt_failed.stderr}",
        )

    if not len(service_notices):
        service_notices.addNotice(
            Brief="Evaluation Successful",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Info",
            Code="600",
            Message="Evaluation Successful",
        )

    log.debug(f"service_outputs: {service_outputs}")
    log.debug(f"service_notices: {service_notices}")
    return service_outputs, service_notices
