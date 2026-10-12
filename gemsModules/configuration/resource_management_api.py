#!/usr/bin/env python3
##
## This file should contain dictionaries relevant to specific resource manager needs.
## 

try:
    from pydantic.v1 import BaseModel, Field
except ImportError:
    from pydantic import BaseModel, Field

## The current form of this code might not work. Consider it to be pseudo-code

## Regarding the information in this file: 
## It should only contain information needed by BatchCompute when it prepares and submits jobs.
## Examples:
##          - If a user asks for 4 GPUs, the method for reserving GPUs needs to be known.
##          - Some schedulers allow the term 'cpu' to mean either 'core' or 'thread'. The choice is
##            made by the provisioner when the scheduler is configured.
## This sort of information must be provided on a cluster-to-cluster basis.

SupportedManagers = [ 
                     "slurm", 
                     # "torque", # additional schedulers can be added.
                     ]

import os
from typing import Optional


class AAD2_Configuration(BaseModel):
    """
    Configuration for Antibody Docking (AAD2) on a specific host.
    """
    aad2_docker_home: Optional[str] = Field(
        None,
        description="Path to AAD2_Docker on this host."
    )
    aad2_cli_bin_path: Optional[str] = Field(
        None,
        description="Path to AAD2 CLI bin directory on this host. If omitted, defaults to {aad2_docker_home}/image/AAD2/bin."
    )
    aad2_image_file_path: Optional[str] = Field(
        None,
        description="Path to AAD2 image files directory on this host."
    )
    image: Optional[str] = Field(
        None,
        description="Docker/Singularity image name/tag for AAD2 (e.g. antibody-docking:tag)."
    )
    vmd_home: Optional[str] = Field(
        None,
        description="Path to VMD binary directory on this host."
    )
    vmd_lib: Optional[str] = Field(
        None,
        description="Path to VMD library directory on this host."
    )
    ad2cliconfig_example_file: Optional[str] = Field(
        None,
        description="Path to ad2cliconfig.example file on this host. If omitted, defaults to {aad2_docker_home}/image/AAD2/99.cluster_utilities/ad2cliconfig.example."
    )

    def get_cli_bin_path(self) -> Optional[str]:
        if self.aad2_cli_bin_path:
            return self.aad2_cli_bin_path
        if self.aad2_docker_home:
            return os.path.join(self.aad2_docker_home, "image/AAD2/bin")
        return None

    def get_ad2cliconfig_example_file(self) -> Optional[str]:
        if self.ad2cliconfig_example_file:
            return self.ad2cliconfig_example_file
        if self.aad2_docker_home:
            return os.path.join(self.aad2_docker_home, "image/AAD2/99.cluster_utilities/ad2cliconfig.example")
        return None

    def get_submit_docking_script(self) -> Optional[str]:
        cli_bin = self.get_cli_bin_path()
        if cli_bin:
            return os.path.join(cli_bin, "submit_docking_to_slurm_with_docker.bash")
        return None

    def get_image(self) -> Optional[str]:
        if self.image:
            return self.image
        if self.aad2_docker_home:
            settings_file = os.path.join(self.aad2_docker_home, "settings.bash")
            if os.path.exists(settings_file):
                image_name, tag_name = None, None
                try:
                    with open(settings_file, "r") as f:
                        for line in f:
                            if "AAD2_IMAGE_NAME" in line and "=" in line:
                                image_name = line.split("=")[1].strip().strip('"\'')
                            if "AAD2_TAG_NAME" in line and "=" in line:
                                tag_name = line.split("=")[1].strip().strip('"\'')
                    if image_name and tag_name:
                        return f"{image_name}:{tag_name}"
                    elif image_name:
                        return image_name
                except Exception:
                    pass
        return None


class Slurm_Specific_Information(BaseModel):
    use_gres_for_gpus: str = Field(
        "True",
        description="Should GPUs be reserved as --gpus or --gres in this installation?"
        )
    cpu_hardware_equivalent: str = Field(
        "core",
        description="Is a CPU considered to be a core or a thread in this installation?"
        )


class ResourceSpecificInformation(Slurm_Specific_Information):
    """
    Information needed for request fulfillment that is specific to resources on the host.
    Includes scheduler information (e.g. Slurm) and entity/tool configuration (e.g. AAD2).
    """
    slurm: Optional[Slurm_Specific_Information] = None
    aad2_configuration: Optional[AAD2_Configuration] = None

    class Config:
        extra = "allow"


## This class is an example for future expansion
## There is currently no support for Torque
##
# class Torqe_Specific_Information(BaseModel):
#     pass

Resource_Specific_Information_Registry = {
#        "torque" : Torqe_Specific_Information,
        "slurm"  : ResourceSpecificInformation,
        }

