#!/usr/bin/env python3
from gemsModules.docs.microcosm.common.utils import GemsStrEnumA

from gemsModules.docs.microcosm.common import loggingConfig
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Known_Entities(GemsStrEnumA):
    """
    The entities that Delegator knows about.
    """
    pass