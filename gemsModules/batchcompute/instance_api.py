#!/usr/bin/env python3
##
## This file should contain dictionaries relevant to specific scheduler needs.
## 

from pydantic import BaseModel

class Slurm_Specific_Information(BaseModel):
    use_gres_for_gpus: str = "True"
