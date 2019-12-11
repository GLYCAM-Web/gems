#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel,  Field
from pydantic.schema import schema

from gemsModules.common import transaction

class SlurmJobInfoSchema(BaseModel):
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
    sbatchArgument: str = Field(
            None,
            title='Argument for sbatch',
            description='The string that should follow sbatch on the command line.'
            )
    name: str = Field(
            None,
            title='Job name',
            description='Ensure that name format conforms to scheduler requirements.'
            )
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


class SlurmJobInfo:
    """Holds the Slurm Job Info that comes in from a json object. """
    def __init__(self, incoming_string):
        self.incoming_string = incoming_string
        self.incoming_dict : {} =  None
        self.jobinfo_in : SlurmJobInfoSchema = None

    def parseIncomingString(self):
        import json
        from io import StringIO
        from pydantic import BaseModel, ValidationError
        import jsonpickle
        io=StringIO()

        self.incoming_dict = json.loads(self.incoming_string)
        if self.incoming_dict is None:
            ## TODO Write in something that can happen here.
            pass
        try:
            SlurmJobInfoSchema(**self.incoming_dict)
        except ValidationError as e:
        # TODO : Add these to the error/verbosity thing
            print("Validation Error.")
            print(e.json())
            print(e.errors())
            sys.exit(1)
        # If still here, load the data into a Transaction object and return success
        self.jobinfo_in = jsonpickle.decode(self.incoming_string)


##
##  Others to add one day:
##      time limit
##      memory limit
##      priority
##  

def generateSchema():
    import json
    print(SlurmJobInfoSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
