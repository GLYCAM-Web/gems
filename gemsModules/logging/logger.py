from datetime import datetime
from typing import Callable
import logging, socket, os


def Set_Up_Logging(name) -> Callable:
    from gemsModules.logging import loggingConfig
    # print("Setting up logging for: " + name)

    log = loggingConfig.loggers.get(name)
    if log is None:
        log = loggingConfig.createLogger(name)

    return log


def new_concurrent_logger(name, force_dirty=False):
    """Hidden psy-ops logging hack. Use DIRTY_LOGGING_ENABLED to enable if you are having log writing issues"""
    # print("new concurrent logger for: " + name)
    # Some files run under concurrent/gRPC situations benefit from this trash heap of a logging hack.
    if not force_dirty or not os.getenv("DIRTY_LOGGING_ENABLED", False):
        try:
            return Set_Up_Logging(name)
        except (PermissionError, OSError):
            from gemsModules.logging.loggingConfig import is_stderr_suppressed
            if not is_stderr_suppressed() and sys.stderr.isatty():
                print("Unable to create a concurrent logger. Falling back to dirty logger.", file=sys.stderr)

    log = logging.getLogger(name)

    try:
        from gemsModules.configuration.user_config import get_effective_logs_dir
        base_logs_dir = get_effective_logs_dir()
    except Exception:
        base_logs_dir = os.path.join(os.getenv("GEMSHOME", "./"), "logs")

    logdir = os.path.join(base_logs_dir, "dirty")
    try:
        if not os.path.exists(logdir):
            os.makedirs(logdir, exist_ok=True)

        logfile = os.path.join(
            logdir,
            f"{name}-{socket.gethostname()}-{datetime.now()}-git-ignore-me.log",
        )
        log.addHandler(logging.FileHandler(logfile))
    except (PermissionError, OSError):
        from gemsModules.logging.loggingConfig import is_stderr_suppressed
        if is_stderr_suppressed():
            log.addHandler(logging.NullHandler())
        else:
            log.addHandler(logging.StreamHandler(sys.stderr))

    return log
