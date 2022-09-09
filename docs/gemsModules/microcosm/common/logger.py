### This is an attempt to not have to put these lines at the top
### of every file.  It works, but it ain't pretty.
from typing import Callable

def Set_Up_Logging(name) -> Callable :
    from gemsModules.docs.microcosm.common import loggingConfig 
    if loggingConfig.loggers.get(name):
        pass
    else:
        log = loggingConfig.createLogger(name)
    
    return log
