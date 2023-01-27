#!/usr/bin/env python3
from pydantic import BaseModel, Field

from gemsModules.common.main_api_services import Service, Response
from gemsModules.common import loggingConfig 

if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)



#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel,  Field
from pydantic.schema import schema

from gemsModules.deprecated.common import transaction
from gemsModules.deprecated.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class SlurmSubmissionSchema(BaseModel):
    partition: str = Field(
            None,
            title='Sumbmission Partition',
            description='The partition to which the job should be submitted.'
            )
    user: str = Field(
            None,
            title='Run-as User',
            description='The user who should submit the job.'
            )
    workingDirectory: str = Field(
            None,
            title='Working Directory',
            description='Path must be appropriate to the scheduler file system.'
            )
    name: str = Field(
            None,
            title='Job name',
            description='Ensure that name format conforms to scheduler requirements.'
            )


class SlurmJobInfoSchema(BaseModel):
    jobID: str = Field(
            None,
            title='Job ID',
            description='The job identifier, if any, returned by the scheduler.'
            )
    schedulerResponse: str = Field(
            None,
            title='Scheduler response',
            description='The entire text returned by the scheduler upon the (attempted or successful) submission.'
            )
    schedulerGrpcHost: str = Field(
            None,
            title='Scheduler gRPC server',
            description='The server to contact via gRPC for submitting the job.  Normally not required.'
            )
    schedulerGrpcPort: int = Field(
            None,
            title='Scheduler gRPC port',
            description='The port to contact via gRPC for submitting the job.  Normally not required.'
            )
    options : transaction.Tags = None

    def generateSchema():
        return(self.schema_json(indent=2))

class submision_script_Inputs(BaseModel) :
    requesting_entity : str  = Field(
        None,
        description="The entity that initiated the request.")
    
class submission_script_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="The response to the Marco request.")

class submission_script_Service(Service) :
    typename : str  = "BuildSubmissionScript"
    inputs : marco_Inputs = marco_Inputs()

class submission_script_Response(Response) :
    outputs : marco_Outputs



if __name__ == "__main__":
  generateSchema()
