#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='Status'

## Status Report
status = "In development"
moduleStatusDetail = "Can receive requests. Currently working on report generation."

servicesStatus = [
    {
        "service" : "GenerateReport",
        "status" : "In development.",
        "statusDetail" : "Knows when it receives a request. If no entities or services are specified, tries to generate a report for all. Cannot generate specific reports yet."
    }
]

serviceModules = {
    "GenerateReport" :"generateReport"
}
