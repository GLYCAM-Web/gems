from typing import Callable
import logging, socket


def Set_Up_Logging(name) -> Callable:
    from gemsModules.logging import loggingConfig

    log = loggingConfig.loggers.get(name)
    if log is None:
        log = loggingConfig.createLogger(name)

    return log
