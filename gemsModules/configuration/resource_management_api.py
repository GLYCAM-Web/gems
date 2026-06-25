#!/usr/bin/env python3
##
## This file should contain dictionaries relevant to specific resource manager needs.
## 

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

class Slurm_Specific_Information(BaseModel):
    use_gres_for_gpus: str = Field(
        "True",
        description="Should GPUs be reserved as --gpus or --gres in this installation?"
        )
    cpu_hardware_equivalent: str = Field(
        "core",
        description="Is a CPU considered to be a core or a thread in this installation?"
        )



## This class is an example for future expansion
## There is currently no support for Torque
##
# class Torqe_Specific_Information(BaseModel):
#     pass

Resource_Specific_Information_Registry = {
#        "torque" : Torqe_Specific_Information,
        "slurm"  : Slurm_Specific_Information
        }

