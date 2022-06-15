#!/usr/bin/env python3
import traceback
from typing import Dict, List
from pydantic import BaseModel
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class Options(BaseModel):
    __root__ : List[Dict] = None

def generateSchema():
    import json
    print(Options.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
    
