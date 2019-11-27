#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Schema
from pydantic.schema import schema

#from gemsModules.common import transaction
from gemsModules.common.transaction import Tags

# ##
# ## Enums 
# ##
class SchedulerTypeEnum(str, Enum):
    slurm='Slurm'
    localhost='None' # for running jobs on the local machine

class QueuePartitionEnum(str, Enum):
    amber='Amber'
    grafting='Grafting'
    node='Node'

class SubmissionStatusEnum(str, Enum):
    new='New'  # has not yet been submitted
    submitted='Submitted'  # has been submitted, but no other info is known yet
    failed='Failed'   # submission was attempted, but the job could not be submitted
    waiting='Waiting'   # has been submitted and is waiting in queue
    running='Running'  # the job is running
    finishing='Finishing'  # the job is no longer running, but is still tracked by the scheduler
    complete='Complete'  # the job has run and is no longer being monitored by the scheduler

class JobSubmissionInfo(BaseModel):
    schedulerType: SchedulerTypeEnum = Schema(
            'Slurm',
            title='Scheduler Type',
            description='The type of scheduling software used in the compute cluster.'
            )
    queuePartition: QueuePartitionEnum = Schema(
            None,
            title='Queue / Partition',
            description='The queue/partition (term depends on software) to use..'
            )
    submissionStatus: SubmissionStatusEnum = Schema(
            None,
            alias='status',
            title='Queue / Partition',
            description='The queue/partition (term depends on software) to use..'
            )
    name: str = Schema(
            None,
            title='Job name',
            description='Ensure that name format conforms to scheduler requirements.'
            )
    workingDirectory: str = Schema(
            None,
            title='Working Directory',
            description='Path must be appropriate to the scheduler file system.'
            )
    schedulerGrpcHost: str = Schema(
            None,
            title='Scheduler gRPC server',
            description='The server to contact via gRPC for submitting the job.  Normally not required.'
            )
    schedulerGrpcPort: int = Schema(
            None,
            title='Scheduler gRPC port',
            description='The port to contact via gRPC for submitting the job.  Normally not required.'
            )
    options : Tags = None
##
##  Others to add one day:
##      time limit
##      memory limit
##      priority
##  

def generateSchema():
    import json
    print(JobSubmissionInfo.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
