#!/usr/bin/env python3
from typing import  Any , Dict 
from pydantic import  Field
from gemsModules.common.loggingConfig import *
import gemsModules.common.services_responses as common_services_responses
from gemsModules.sequence import settings as sequencesettings
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class Sequence_Service(common_services_responses.Service) :
    typename: sequencesettings.AvailableServices = Field(
        'Evaluate',
        alias='type',
        title='Service',
        description='Evaluate a sequence.'
    )

class Sequence_Services(common_services_responses.Services) :
    __root__ : Dict[str, Sequence_Service] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Initializing Services for Sequence.")
        log.debug("the data " + repr(self))
        log.debug("Init for the Services in sequence was called.")


def generateSchema():
    print(Sequence_Services.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
