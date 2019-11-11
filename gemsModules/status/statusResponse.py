#!/usr/bin/env python3
from typing import Dict, List
from pydantic import BaseModel, Schema
from pydantic.schema import schema

class ServiceReport(BaseModel):
    service : str
    status : str
    statusDetail : str


class StatusResponse(BaseModel):
    status : 'Down'
    moduleStatusDetail : str
    services : List[ServiceReport]

if__name__ == "__main__":
    ##TODO: write this.
    generateStatusResponse()
