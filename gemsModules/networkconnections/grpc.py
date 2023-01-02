#!/usr/bin/env python3
from pydantic import BaseModel, Field
from gemsModules.common.main_api_services import Service, Response


from gemsModules. import loggingConfig 
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




#schedulerGrpcHost: str = Field(
#    None,
#    title='Scheduler gRPC server',
#    description='The server to contact via gRPC for submitting the job.  Normally not required.'
#    )
#schedulerGrpcPort: int = Field(
#    None,
#    title='Scheduler gRPC port',
#    description='The port to contact via gRPC for submitting the job.  Normally not required.'
#    )


