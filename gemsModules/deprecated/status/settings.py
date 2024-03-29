#!/usr/bin/env python3
from gemsModules.deprecated import common
from gemsModules.deprecated.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## Who I am
WhoIAm='Status'

## Status Report
status = "Stable"
moduleStatusDetail = "Can receive requests. Currently working on report generation."

servicesStatus = [
    {
        "service" : "GenerateReport",
        "status" : "Stable.",
        "statusDetail" : "Generates a backend report for all entities."
    },
    {
    	"service" : "GetJobStatus",
    	"status" : "In development",
    	"statusDetail" : "Building service infrastructure."
    }
]

serviceModules = {
    "GenerateReport" :"generateReport",
    "GetJobStatus" : "getJobStatus"
}
