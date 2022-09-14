#!/usr/bin/env python3
from pydantic import BaseModel

class inputs (BaseModel):
    C_int : int = 42
    C_string : str = "EVERYTHING"

class outputs (BaseModel):
    C_string = "Uncertainty"



if __name__ == "__main__" :
    print(inputs.schema_json(indent=2))
    print(outputs.schema_json(indent=2))
