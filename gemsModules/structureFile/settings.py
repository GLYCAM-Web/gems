#!/usr/bin/env python3
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel
from enum import Enum, auto
## Who I am
WhoIAm='StructureFile'

##Status Report
status = "Dev"
moduleStatusDetail = "PDB Pre-processing for Amber currently in development. Writing evaluate service."

servicesStatus = [
    {
        "service" : "Evaluate",
        "status" : "Alpha.",
        "statusDetail" : "Testing for deployment. In-house testing only so far."
    },
    {
        "service" : "PreprocessPdbForAmber",
        "status" : "In development.",
        "statusDetail" : "Actively in development. Working to preprocess with default settings."
    }
]

serviceModules = {
    'Evaluate' : 'evaluate',
    'PreprocessPdbForAmber' : 'preprocessPdbForAmber'
}

# ## Services
# ##
class Services(str,Enum):
    evaluate = 'Evaluate'
    status = 'Status'
    preprocessPdbForAmber = 'PreprocessPdbForAmber'



