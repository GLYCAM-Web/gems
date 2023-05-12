#!/usr/bin/env python3
from pydantic import BaseModel

class Module_User_Friendliness_Inputs(BaseModel) :
    string_A : str = None
    int_A : int = None
    string_B1 : str = None
    int_B1 : int = None
    string_B2 : str = None
    int_B2 : int = None
    string_C : str = None
    int_C : int = None
    

class Module_User_Friendliness_Outputs(BaseModel) :
    bool_A : bool = None
    bool_B1 : bool = None
    bool_B2 : bool = None
    string_C : str = None

