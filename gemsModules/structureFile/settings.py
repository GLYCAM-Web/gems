#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='StructureFile'

##Status Report
status = "Stable"
moduleStatusDetail = "PDB Pre-processing for Amber."

servicesStatus = [
    {
        "service" : "PreprocessPdbForAmber",
        "status" : "Stable",
        "statusDetail" : "Can receive a PDB file and generate a new one that has been preprared for use with Amber."
    }
]

serviceModules = {
    'PreprocessPdbForAmber' : 'preprocessPdbForAmber'
}
