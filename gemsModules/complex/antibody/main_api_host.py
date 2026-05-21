#!/usr/bin/env python3
import os

from pydantic import BaseModel, Field

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


##
## TODO
## Move the common parts to the Common entity.
## Make this a child of 'ExecutionHostData' in Common.
##
class AntibodyExecutionHostData(BaseModel):
    """
    Indicate paths and other environmental needs
    """
    max_number_of_nodes : int = Field(
            1,
            description = "The maximum number of nodes available to the AAD2 service."
            )
    max_cpus_per_node : int = Field(
            28,
            description = "The number of CPUs (generally, cores) available to AAD2 on each node."
            )
    max_threads_per_node : int = Field(
            56,
            description = "The number of threads available to AAD2 on each node."
            )
    assigned_queue : str = Field(
            "",
            description = "The queue/partition that AAD2 should use."
            )
    time_limit : str = Field(
            "P0DT2H0M", 
            description = "Computing time limit in ISO 8601 format. Example: 2 days, 16 hours and 30 minutes: P2DT16H30M "
            )
    aad2_stacks_path : str = Field(
            "" ,
            description = "Path to software stacks used by AAD2."
            )
    aad2_docker_version : str = Field(
            "",
            description = "in the external_stacks_path, look for AAD2_Docker_{aad2_docker_version}."
            )
    aad2_docker_home : str = Field(
            "",
            description = "If unset: {external_stacks_path}/AAD2_Docker_{aad2_docker_version}."
            )
    aad2_cli_bin_path : str = Field(
            "",
            description = "if unset: {external_stacks_path}/AAD2_Docker_{aad2_docker_version}/image/AAD2/bin."
            )
    aad2_image_name : str = Field(
            "",
            description = "The name for the AAD2 docker image."
            )
    aad2_image_tag : str = Field(
            "",
            description = "The tag for the AAD2 docker image."
            )
    aad2_image_file_path : str = Field(
            "",
            description = "The full path to the AAD2 docker image files."
            )
    binary_dependencies_path : str = Field(
            "",
            description = "Path to standard binary dependencies, e.g., VMD."
            )
    vmd_home : str = Field(
            "",
            description = "The full path to the VMD binary."
            )
    vmd_lib : str = Field(
            "",
            description = "The full path to the VMD library directory."
            )

