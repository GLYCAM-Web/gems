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


if __name__ == "__main__" :
    class input_here (Inputs):
        def __init__(self, A_int = int, A_string = str):
            self.A_int = A_int
            self.A_string = A_string

    input_Good = input_here ( A_int = 3, A_string = "abc" )
    the_output = do_service_A(input_Good)
    print(str(the_output.A_bool))

    input_Bad = input_here ( A_int = 3, A_string = "abcd" )
    the_output = do_service_A(input_Bad)
    print(str(the_output.A_bool))