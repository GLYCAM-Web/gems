#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='Graph'

##Status Report
status = "In development."
moduleStatusDetail = "Module framework in place. Currently working to install required dependencies and develop services."

servicesStatus = [
    {
        "service" : "DrawGlycan",
        "status" : "In development.",
        "statusDetail" : "Can recognize that requests were made. Doesn't do anything else yet."
    }
]


## Module names for services that this entity/module can perform.
serviceModules = {
    'DrawGlycan' : 'drawGlycan',
}

