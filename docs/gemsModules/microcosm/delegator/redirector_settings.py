#!/usr/bin/env python3
from ..common.code_utils import GemsStrEnum

from ..common import loggingConfig
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Known_Entities(GemsStrEnum):
    """
    The entities that Delegator knows about.
    """
    module = 'Module'
    meta_module = 'Meta_Module'
