from typing import Callable

def Set_Up_Logging(name) -> Callable :
    from gemsModules.status import loggingConfig 
    log = loggingConfig.loggers.get(name)
    if log :
        return log
    else:
        return loggingConfig.createLogger(name)
    
