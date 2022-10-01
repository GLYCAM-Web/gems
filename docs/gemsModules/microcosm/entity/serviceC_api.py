#!/usr/bin/env python3
from pydantic import BaseModel

class inputs (BaseModel):
    C_int : int = 42
    C_string : str = "EVERYTHING"

class outputs (BaseModel):
    C_string = "Uncertainty"


