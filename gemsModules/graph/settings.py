#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## Who I am
WhoIAm='Graph'

##Status Report
status = "Down"
moduleStatusDetail = "In queue for development. Gems/JSON interface needed."

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

