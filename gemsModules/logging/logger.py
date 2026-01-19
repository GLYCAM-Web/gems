from datetime import datetime
from typing import Callable
import logging, socket, os


def Set_Up_Logging(name) -> Callable:
    from gemsModules.logging import loggingConfig

    log = loggingConfig.loggers.get(name)
    if log is None:
        log = loggingConfig.createLogger(name)

    return log


def new_concurrent_logger(name, force_dirty=False):
    """Hidden psy-ops logging hack. Use DIRTY_LOGGING_ENABLED to enable if you are having log writing issues"""
    # Some files run under concurrent/gRPC situations benefit from this trash heap of a logging hack.
    if not force_dirty or not os.getenv("DIRTY_LOGGING_ENABLED", False):
        try:
            return Set_Up_Logging(name)
        except PermissionError:
            print("Unable to create a concurrent logger. Falling back to dirty logger.")

    log = logging.getLogger(name)

    logdir = os.path.join(os.getenv("GEMSHOME", "./"), "logs", "dirty")
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logfile = os.path.join(
        logdir,
        f"{name}-{socket.gethostname()}-{datetime.now()}-git-ignore-me.log",
    )

    log.addHandler(logging.FileHandler(logfile))
    return log
