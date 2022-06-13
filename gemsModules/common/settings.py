#!/usr/bin/env python3
from enum import Enum, auto
#from typing import Dict, List #, Optional, Sequence, Set, Tuple, Union, Any

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


WhoIAm = 'CommonServicer'

class AvailableServices(Enum):
    marco = 'Marco'
    status = 'Status'

    @classmethod
    def get_list(self):
        theList = []
        for item in self :
            theList.append(item.name)
        return theList



