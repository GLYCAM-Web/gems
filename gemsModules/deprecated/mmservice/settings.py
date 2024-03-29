#!/usr/bin/env python3
from gemsModules.deprecated import common

from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## Who I am
WhoIAm='mmservice'

##Status Report
status = "In development"
moduleStatusDetail = "Module framework exists. Building logic for Amber submissions."

servicesStatus = [
    {
        "service" : "Amber",
        "status" : "In development",
        "statusDetail" : "Creating the logic used to submit requests to Slurm."
    }
]

serviceModules = {
    'Amber' : 'amber'
}
