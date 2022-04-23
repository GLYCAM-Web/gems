#!/usr/bin/env python3

import traceback
from gemsModules.common.loggingConfig import loggers, createLogger
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def main():
    log.info("main() was called.\n")


if __name__ == "__main__":
    main()
