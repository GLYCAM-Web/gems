#!/usr/bin/env python3
from pydantic import BaseModel

class inputs (BaseModel):
    B1_int : int = 3
    B1_string : str = "B"

class outputs (BaseModel):
    B1_bool : bool = False


