#!/usr/bin/env python3
from pydantic import validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.logging.logger import Set_Up_Logging

from .api import Evaluate_Inputs, Evaluate_Outputs
from ...main_api_project import AntibodyProject

from  ...tasks import fix_glycam_glycan, run_detect_sugars, run_ad_evaluate


log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Evaluate_Inputs) -> tuple[Evaluate_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Evaluate_Outputs()
    service_notices = Notices()

    #workdir = AntibodyProject.get_project_dir_from_pUUID(inputs.pUUID) deprecated form
FIX ME
    workdir = ## should already be visible by the time a service is called
    log.debug(f"workdir: {workdir}")
    if not workdir:
        service_notices.addNotice(
            Brief="Project not found",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Error",
            Code="400",
            Message="Project not found",
        )
        return service_outputs, service_notices
    
    # Fix ligand.pdb by adding an END card at the end of file if not present
    needed_fix = fix_glycam_glycan.execute(inputs.ligand_path)
    log.debug(f"Fixed ligand.pdb: {needed_fix=}")
    
    # Call gmml/detect_sugars on ligand.pdb to generate glycan_ring_atoms.txt
    # TODO: Delay until gRPC too? (It's a little slow)
    run_detect_sugars.execute(inputs.ligand_path, workdir) 
    
    # if is_correct_GEMS_instance_for_AAD2(): - should not get to this if it is not
    # TODO: Call AD_Evaluate over gRPC here. - this is ideal, but not a huge priority
    results = run_ad_evaluate.execute(inputs.pUUID, workdir)
    if results.returncode:
        service_notices.addNotice(
            Brief="Evaluation Failed",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Error",
            Code="500",
            Message=f"Evaluation Failed: {results.stderr}",
        )

    if not len(service_notices):
        service_notices.addNotice(
            Brief="Evaluation Successful",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Info",
            Code="600",
            Message="Evaluation Successful",
        )

    log.debug(f"service_outputs: {service_outputs}")
    log.debug(f"service_notices: {service_notices}")
    return service_outputs, service_notices
