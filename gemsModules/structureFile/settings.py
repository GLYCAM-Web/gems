#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='StructureFile'

##Status Report
status = "Dev"
moduleStatusDetail = "PDB Pre-processing for Amber currently in development."

servicesStatus = [
    {
        "service" : "PreprocessPdbForAmber",
        "status" : "In queue for development.",
        "statusDetail" : "Queued for after Evaluate service."
    },
    {
        "service" : "Evaluate",
        "status" : "In development.",
        "statusDetail" : "In development."
    }
]

serviceModules = {
    'PreprocessPdbForAmber' : 'preprocessPdbForAmber',
    'Evaluate' : 'evaluate'
}
