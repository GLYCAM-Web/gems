#!/usr/bin/env python3
from typing import Dict
from pydantic import Field
from gemsModules.common.loggingConfig import *
import gemsModules.common.resources as common_resources
from gemsModules.sequence import settings
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class SequenceResource(common_resources.Resource):
    locationType: settings.Locations = Field(
        'internal',
        description='Supported input locations for the Service Entity.'
    )
    resourceFormat: settings.Formats = Field(
        'GlycamCondensed',
        description='Supported input formats for the Service Entity.'
    )

class Resources(common_resources.Resources):
    __root__ : Dict[str, SequenceResource] = {}

def generateSchema():
    print(Resources.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
