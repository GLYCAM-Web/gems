#!/usr/bin/env python3
from gemsModules.common.utils import GemsStrEnum
#from typing import Dict, List #, Optional, Sequence, Set, Tuple, Union, Any

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


WhoIAm = 'CommonServicer'

class AvailableServices(GemsStrEnum):
    marco = 'Marco'
    status = 'Status'


