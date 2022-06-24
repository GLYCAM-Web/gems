#!/usr/bin/env python3
from pydantic import BaseModel
from gemsModules.common.loggingConfig import *
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class TheEvaluationOptions(BaseModel):
    """Options for sequence evaluations"""
    validateOnly: bool = False  # Stop after setting sequenceIsValid and return answer
    # Is this an evaluation as part of an explicit build request?
    evaluateForBuild: bool = False
    noBuild: bool = False  # Just do a full evaluation ; don't do the default example build


def generateSchema():
    print(TheEvaluationOptions.schema_json(indent=2))



if __name__ == "__main__":
    generateSchema()
