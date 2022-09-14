#!/usr/bin/env python3
from pydantic import BaseModel

class inputs (BaseModel):
    A_int : int = 0
    A_string : str = ""

class outputs (BaseModel):
    A_bool : bool = False



if __name__ == "__main__" :
    print(inputs.schema_json(indent=2))
    print(outputs.schema_json(indent=2))
