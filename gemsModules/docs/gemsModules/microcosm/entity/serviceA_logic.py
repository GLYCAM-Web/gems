#!/usr/bin/env python3
from typing import Protocol

class Inputs(Protocol):
    A_int : int 
    A_string : str

class Outputs(Protocol):  
    A_bool : bool

def do_service_A(inputs : Inputs) -> Outputs:
    class outputs (Outputs):
        def __init__(self, A_bool : bool = True):
            self.A_bool = A_bool

    this_output = outputs()
    
    if len(inputs.A_string) != inputs.A_int :
        this_output.A_bool = False
    
    return this_output


