#!/usr/bin/env python3
from pydantic import BaseModel
from pydantic.schema import schema
from typing import Any

class dumClass(BaseModel):

    A : str = 'Hello'
    B : str = None
    C: bool = False

    def __init__(self, **data: Any):
        print("dumClass was called")
        super().__init__(**data)
        print("dumClass was initialized")
        if self.A == "Hello" : 
            self.B = "Goodbye"

    def saySomething(self):
        if self.C is False :
            print("Shhhhhh......")
        else :
            print("A is " + self.A + "; B is " + self.B)

def troubleshoot() :

    print("Testing the dumClass!")
    thisJSON={"A":"Hello","C":True}
    try :
        thisproject = dumClass(**thisJSON)
    except ValidationError as e :
        print(e)

    thisproject.saySomething()

def generateSchema():
    import json
    print(dumClass.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
  troubleshoot()

