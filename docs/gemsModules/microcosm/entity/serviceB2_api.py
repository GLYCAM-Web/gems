#!/usr/bin/env python3
from pydantic import BaseModel

class inputs (BaseModel):
    B2_int : int = 8
    B2_string : str = "B2"

class outputs (BaseModel):
    B2_bool : bool = True


