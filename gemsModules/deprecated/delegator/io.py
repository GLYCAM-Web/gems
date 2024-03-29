#!/usr/bin/env python3
#
# ###############################################################
# ##
# ##  The gemsModules.deprecated are being refactored.
# ##  
# ##  This file:
# ##
# ##      -  Will eventually hold the Transaction class
# ##      -  Might not be in full use by all modules
# ##
# ##  The modules/Entities that are partially or wholly 
# ##  changed so that they use this file are:
# ##
# ##      None yet.
# ##
# ##  Go see that module for examples, etc.
# ##
# ##  Please add your module to the list when you change 
# ##  it, just to help reduce chaos.
# ##
# ##  Got a better accounting method?  Let's hear it!
# ##
# ###############################################################
import traceback
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from typing import ForwardRef
from pydantic import BaseModel, Field, Json
from pydantic.schema import schema
from gemsModules.deprecated.common import io as commonio
from gemsModules.deprecated.project import dataio as projectio
from gemsModules.deprecated.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class Entities(str, Enum):
    commonServices = 'CommonServices'
    delegator = 'Delegator'
    project = 'Project'
    sequence = 'Sequence'


