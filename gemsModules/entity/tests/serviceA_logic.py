#!/usr/bin/env python3
from typing import Protocol
from gemsModules.docs.microcosm.entity import serviceA_logic as logicA

class input_here (logicA.Inputs):
    def __init__(self, A_int = int, A_string = str):
        self.A_int = A_int
        self.A_string = A_string

input_Good = input_here ( A_int = 3, A_string = "abc" )
the_output = logicA.do_service_A(input_Good)
print(str(the_output.A_bool))

input_Bad = input_here ( A_int = 3, A_string = "abcd" )
the_output = logicA.do_service_A(input_Bad)
print(str(the_output.A_bool))
