#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## Who I am
WhoIAm='Sequence'

##Status Report
status = "Stable"
moduleStatusDetail = "Nearing ready for v1 release. Needs tests and documentation."

servicesStatus = [
    {
        "service" : "Validate",
        "status" : "Stable.",
        "statusDetail" : "Rarely used Evaluate includes Validate. Validate mayeventually be deprecated."
    },
    {
        "service" : "Evaluate",
        "status" : "Stable.",
        "statusDetail" : "Works for GLYCAM condensed sequences."
    },
    {
        "service" : "Build3DStructure",
        "status" : "Stable.",
        "statusDetail" : "Ready for tests and documentation."
    }
]

subEntities = [
    {
        "subEntity" : "Graph"
    }
]


#Validate service in focus.
#Evaluate service still needs to be developed.
#Build3DStructure can create a default structure.
#No minimization is applied yet.
#No options can be set yet."

## Module names for services that this entity/module can perform.
serviceModules = {
    'Validate' : 'validate',
    'Evaluate' : 'evaluate',
    'Build3DStructure' : 'build3Dstructure'
}

