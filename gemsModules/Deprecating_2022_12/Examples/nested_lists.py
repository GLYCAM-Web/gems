#!/usr/bin/env python3
from pydantic import BaseModel, ValidationError, Field, validator
from pydantic.schema import schema
from typing import Any, List, Dict

class dumClass(BaseModel):
    A : str = Field(
            'Special',
            alias='type',
            )
    B : int = None
    C : bool = None

class containerClass(BaseModel) :
    myname : str = Field(
        'Evaluate', 
        alias = 'name', 
        title = 'Requested Service', 
        description = 'The service requested of the Sequence Entity'
        )
    myDummies : List[Dict[str,dumClass]] = []

def troubleshoot() :
    import json
    #thisJSON={"name":"Fumble","myDummies":[{"numberOne":{"A":"Hello","C":True}}]}
    thisRawJSON='{"name":"Fumble","myDummies":[{"numberOne":{"Z":"ouch","type":"Hello","C":true}}]}'
    thisJSON=json.loads(thisRawJSON)
    try :
        thisproject = containerClass(**thisJSON)
    except ValidationError as e :
        print(e)

    print(thisproject)


def generateSchema():
    import json
    #print(dumClass.schema_json(indent=2))
    print(containerClass.schema_json(indent=2))

if __name__ == "__main__":
#  generateSchema()
  troubleshoot()

