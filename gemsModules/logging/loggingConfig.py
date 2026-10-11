import logging, os, sys
import socket

# logging cannot import complex dependencies from gemsModules, but user_config has 0 internal dependencies
try:
    from gemsModules.configuration.user_config import (
        get_effective_logs_dir,
        get_effective_logging_level,
    )
except Exception:
    get_effective_logs_dir = None
    get_effective_logging_level = None

##TODO Create custom logging levels for critical errors to be able to specify
##  email recipient.


def is_stderr_suppressed() -> bool:
    """Check if stderr must remain completely clean (e.g. website or gRPC delegation)."""
    if "GW_LIVE_SWARM" in os.environ or "GW_DOMAIN" in os.environ:
        return True
    if os.environ.get("GEMS_NO_STDERR") in ("1", "true", "True"):
        return True
    return False


## Set the verbosity via the GEMS_LOGGING_LEVEL environment var or .gemsrc.
def getGemsLoggingLevel():
    try:
        loggingLevel = os.environ.get("GEMS_LOGGING_LEVEL")
        if loggingLevel is None and get_effective_logging_level is not None:
            loggingLevel = get_effective_logging_level()

        if loggingLevel is None:
            loggingLevel = logging.ERROR
        elif str(loggingLevel).lower() == "error":
            loggingLevel = logging.ERROR
        elif str(loggingLevel).lower() == "info":
            loggingLevel = logging.INFO
        elif str(loggingLevel).lower() == "debug":
            loggingLevel = logging.DEBUG
        else:
            if not is_stderr_suppressed() and sys.stderr.isatty():
                print(
                    "The only valid values for GEMS_LOGGING_LEVEL are: error, info, or debug: "
                    + str(loggingLevel),
                    file=sys.stderr,
                )
            loggingLevel = logging.ERROR
        return loggingLevel
    except Exception:
        return logging.ERROR


LOGGING_LEVEL = getGemsLoggingLevel()
loggers = {}

"""
Creates a logging solution for writing to the console. Can add handlers if
we want to write logs to file, send emails, etc...
"""


class HostnameFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True


def createLogger(name):
    if loggers.get(name):
        log.debug("logger already exists with name: " + name)
    else:
        log = logging.getLogger(name)
        log.setLevel(LOGGING_LEVEL)

        hostnameFilter = HostnameFilter()
        formatter = logging.Formatter(
            "%(hostname)s %(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p",
        )

        handlers_added = False
        try:
            logsDir = getLogsDir()
            if logsDir and os.path.exists(logsDir):
                errorFileHandler = logging.FileHandler(
                    os.path.join(logsDir, "git-ignore-me_gemsError.log")
                )
                errorFileHandler.setLevel(logging.ERROR)
                errorFileHandler.addFilter(hostnameFilter)
                errorFileHandler.setFormatter(formatter)
                log.addHandler(errorFileHandler)
                handlers_added = True

                if LOGGING_LEVEL == logging.INFO or LOGGING_LEVEL == logging.DEBUG:
                    infoFileHandler = logging.FileHandler(
                        os.path.join(logsDir, "git-ignore-me_gemsInfo.log")
                    )
                    infoFileHandler.setLevel(logging.INFO)
                    infoFileHandler.addFilter(hostnameFilter)
                    infoFileHandler.setFormatter(formatter)
                    log.addHandler(infoFileHandler)

                if LOGGING_LEVEL == logging.DEBUG:
                    debugFileHandler = logging.FileHandler(
                        os.path.join(logsDir, "git-ignore-me_gemsDebug.log")
                    )
                    debugFileHandler.setLevel(logging.DEBUG)
                    debugFileHandler.addFilter(hostnameFilter)
                    debugFileHandler.setFormatter(formatter)
                    log.addHandler(debugFileHandler)
        except (PermissionError, OSError) as e:
            # If writing to log files fails due to permission denied or unwritable filesystem,
            # gracefully fall back to a stderr handler so the program does not crash.
            pass

        if not handlers_added:
            if is_stderr_suppressed():
                log.addHandler(logging.NullHandler())
            else:
                streamHandler = logging.StreamHandler(sys.stderr)
                streamHandler.setLevel(LOGGING_LEVEL)
                streamHandler.addFilter(hostnameFilter)
                streamHandler.setFormatter(formatter)
                log.addHandler(streamHandler)

        loggers[name] = log
        log.debug("Created a new logger with level: " + str(LOGGING_LEVEL))
    return log


def getLogsDir():
    if get_effective_logs_dir is not None:
        try:
            return get_effective_logs_dir()
        except Exception:
            pass

    GEMSHOME = os.environ.get("GEMSHOME")
    if GEMSHOME:
        logsDir = os.path.join(GEMSHOME, "logs")
        try:
            if not os.path.exists(logsDir):
                os.makedirs(logsDir, exist_ok=True)
            return logsDir
        except (PermissionError, OSError):
            pass

    # Fallback to user home or temp directory
    user_dir = os.path.expanduser("~/.gems/logs")
    try:
        os.makedirs(user_dir, exist_ok=True)
        return user_dir
    except (PermissionError, OSError):
        return "/tmp"

