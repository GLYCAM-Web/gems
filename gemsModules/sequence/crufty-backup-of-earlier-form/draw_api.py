#!/usr/bin/env python3
from pydantic import BaseModel, Field
from gemsModules.common.loggingConfig import *
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class TheDrawOptions(BaseModel):
    """Options for drawing 2D models"""
    Labeled: bool = True


def generateSchema():
    print(TheDrawOptions.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
