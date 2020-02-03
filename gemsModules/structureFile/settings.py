#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='StructureFile'

##Status Report
status = "In development"
moduleStatusDetail = "Module framework exists. Building logic for PDB Preprocessing for Amber."

servicesStatus = [
    {
        "service" : "Preprocess",
        "status" : "In development",
        "statusDetail" : "Creating the logic used to preprocess PDB files."
    }
]

serviceModules = {
    'Preprocess' : 'preprocess'
}
