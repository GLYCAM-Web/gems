#!/usr/bin/env python3
from typing import Protocol

from gemsModules.common.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)  ## will this break?

## These are a little redundant in this simple example.
class serviceInputs (Protocol):
    entity : str
    who_I_am : str 

class serviceOutputs (Protocol):
    message : str


