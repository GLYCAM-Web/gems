#!/usr/bin/env python3
from ..common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

WhoIAm = 'Delegator'
