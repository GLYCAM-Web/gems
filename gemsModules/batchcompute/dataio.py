#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Schema
from pydantic.schema import schema


##
##  Job options....
##  
##  name
##  working directory
##  queue/partition
##  time limit
##  memory limit
##  priority
##  

##  Scheduler Info....
##
##  type of scheduler (slurm, torque, ll, NONE, etc.) - NONE means use localhost and just run the job
##  location of scheduler (host name , port)
##  

class SubmissionSchema(BaseModel):
    schedulerInfo : 
    jobOptions : None
    options : Tags = None


def generateSchema():
    import json
    print(SubmissionSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
