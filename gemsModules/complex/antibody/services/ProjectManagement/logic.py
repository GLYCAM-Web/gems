#!/usr/bin/env python3
import os
import subprocess
import shutil
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.systemoperations.filesystem_ops import replace_bash_variable_in_file
from gemsModules.systemoperations.environment_ops import get_site_version

# from gemsModules.complex.antibody.tasks import batchcompute
from gemsModules.common.main_api_notices import Notices
from gemsModules.configuration.resource_management_api import AAD2_Configuration
from gemsModules.complex.antibody.services.ProjectManagement.api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource
from gemsModules.complex.antibody.tasks.create_configs import create_ad2config, create_gwconfig, create_vcconfig
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def resolve_aad2_configuration(target_host: Optional[str] = None) -> Optional[AAD2_Configuration]:
    """
    Resolve AAD2_Configuration using InstanceConfig and environment variable overrides.
    """
    cfg = None
    try:
        from gemsModules.configuration.main_api import session_instance_config
        cfg = session_instance_config.get_aad2_configuration(target_host=target_host)
    except Exception as e:
        log.warning(f"Could not load AAD2 configuration from IC: {e}")

    env_docker_home = os.environ.get("AAD2_DOCKER_HOME")
    if env_docker_home:
        if cfg:
            cfg = cfg.copy(deep=True)
            cfg.aad2_docker_home = env_docker_home
        else:
            cfg = AAD2_Configuration(aad2_docker_home=env_docker_home)

    return cfg


def execute(inputs: ProjectManagement_Inputs, service_notices: Optional[Notices] = None) -> ProjectManagement_Outputs:
    """Executes the ProjectManagement service."""
    log.debug(f"serviceInputs: {inputs}")

    service_outputs = ProjectManagement_Outputs()
    if service_notices is None:
        service_notices = Notices()

    service_outputs.resources.add_resource(
        PM_Resource(
            payload=inputs.projectDir,
            resourceFormat="string",
            resourceRole="ProjectDirectory",
        )
    )

    # Resolve AAD2 configuration dynamically
    aad2_config = resolve_aad2_configuration()
    if not aad2_config or not aad2_config.aad2_docker_home:
        msg = "Path to AAD2_Docker is not configured in the Instance Configuration or AAD2_DOCKER_HOME environment variable."
        log.error(msg)
        service_notices.addNotice(
            Brief="PathNotConfigured",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Error",
            Code="404",
            Message=msg,
        )
        if hasattr(service_outputs, "notices"):
            service_outputs.notices.extend(service_notices)
        return service_outputs

    # Setup project directory
    log.debug(f"AD/ProjectManagement: about to create project directory: {inputs.projectDir}")
    os.makedirs(inputs.projectDir, exist_ok=True)

    log.debug("AD/ProjectManagement: about to copy resources to project dir")
    log.debug(f"AD/ProjectManagement: resources: {inputs.resources}")
    antibody_name, ligand_name = None, None
    for resource in inputs.resources:
        file_resource = resource.copy_to(inputs.projectDir)

        if resource.resourceRole == "Antibody":
            antibody_name = os.path.relpath(file_resource.payload, inputs.projectDir)
        elif resource.resourceRole == "Ligand":
            ligand_name = os.path.relpath(file_resource.payload, inputs.projectDir)
        service_outputs.resources.add_resource(file_resource)

    # Create config files
    create_vcconfig(inputs.projectDir + "/vcconfig")
    create_gwconfig(inputs.projectDir + "/gwconfig", inputs.pUUID)
    create_ad2config(
        inputs.projectDir + "/ad2config",
        antibody_name,
        ligand_name,
        aad2_config=aad2_config,
    )

    aad2_docker_home = aad2_config.aad2_docker_home
    cli_bin_path = aad2_config.get_cli_bin_path()
    image_tag = aad2_config.get_image()

    replacements = {
        "AAD2_DOCKER_HOME": aad2_docker_home,
        "AAD2_CLI_BIN_PATH": cli_bin_path or "",
    }
    if image_tag:
        replacements["Image"] = image_tag
    replace_bash_variable_in_file(f"{inputs.projectDir}/ad2config", replacements)
    log.debug(f"The AD2 image is: '{image_tag}'")

    slurm_submit_docking = aad2_config.get_submit_docking_script()
    if slurm_submit_docking and os.path.exists(slurm_submit_docking):
        actual_submit_docking = shutil.copy(slurm_submit_docking, inputs.projectDir)
        if not os.path.exists(actual_submit_docking):
            log.warning(f"AD/ProjectManagement: Error copying {slurm_submit_docking} to {inputs.projectDir}")
    else:
        log.debug(f"slurm_submit_docking file not present on this host: {slurm_submit_docking}")

    if hasattr(service_outputs, "notices"):
        service_outputs.notices.extend(service_notices)

    return service_outputs
