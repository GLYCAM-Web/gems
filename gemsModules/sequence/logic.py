#!/usr/bin/env python3
import traceback
from multiprocessing import Process
from gemsModules.common.loggingConfig import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)
#
class EverLastingProcess(Process):
    def join(self, *args, **kwargs):
        pass # Overwrites join so that it doesn't block. Otherwise parent waits.
    def __del__(self):
        pass

def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

