#!/usr/bin/env python3
from pydantic import BaseModel, ValidationError
from pydantic.schema import schema
from typing import Any

class Foo(BaseModel):

    A : str = 'Hello'
    B : str = None
    C : bool = False

    def __init__(self, **data: Any):
        print("dumClass was called")
        super().__init__(**data)
        print("dumClass was initialized")
        if self.A is "Hello" : 
            self.B = "Goodbye"

    def saySomething(self):
        if self.C is False :
            print("Shhhhhh......")
        else :
            print("A is " + self.A + "; B is " + self.B)

class Bar(Foo):
    A : int = 3
    B : str = "three"
    C : str = "Yep"

class Bumble():
    Baz : Bar

def troubleshoot() :

    print("Testing the dumClass!")
    thisJSON={"A":5,"B":"Haha","C":"well"}
    #thisJSON={"A":"Hello","C":True}
    thisBumble=Bumble()
    try :
        thisproject = thisBumble.Baz(**thisJSON)
        #thisproject = Bar(**thisJSON)
        #thisproject = Foo(**thisJSON)
    except ValidationError as e :
        print(e)

    #thisproject.saySomething()

    print("The project is: ")
    print(thisproject)

def generateSchema():
    import json
    print(Bar.schema_json(indent=2))

if __name__ == "__main__":
#  generateSchema()
  troubleshoot()

