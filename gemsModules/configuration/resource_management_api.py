#!/usr/bin/env python3
##
## This file should contain dictionaries relevant to specific resource manager needs.
## 

from pydantic import BaseModel

## The current form of this code might not work. Consider it to be pseudo-code

SupportedManagers = [ "slurm", "torque" ]

class Slurm_Specific_Information(BaseModel):
    use_gres_for_gpus: str = "True"

class Torqe_Specific_Information(BaseModel):
    pass

Resource_Specific_Information_Registry = {
        "slurm"  : Slurm_Specific_Information,
        "torque" : Torqe_Specific_Information
        }

