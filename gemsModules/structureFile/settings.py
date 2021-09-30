#!/usr/bin/env python3
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel
## Who I am
WhoIAm='StructureFile'

##Status Report
status = "Dev"
moduleStatusDetail = "PDB Pre-processing for Amber currently in development. Writing evaluate service."

servicesStatus = [
    {
        "service" : "Evaluate",
        "status" : "In development.",
        "statusDetail" : "In development. Currently fails to return a valid response. Queued for after Schema service."
    },
    {
        "service" : "PreprocessPdbForAmber",
        "status" : "In development.",
        "statusDetail" : "In development."
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



