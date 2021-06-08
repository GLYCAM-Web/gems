#!/usr/bin/env python3

### These import statements can probably go
#import json, sys, os, re, importlib.util, shutil, uuid
#import gemsModules
#import gmml
#import gemsModules.common.utils
#from gemsModules.project import projectUtilPydantic as projectUtils
#from gemsModules.project import settings as projectSettings
#from gemsModules.project import io as projectio
#from gemsModules.common import io as commonio
#from gemsModules.common import logic as commonlogic
#from gemsModules.sequence import projects as sequenceProjects
#from gemsModules.sequence import settings as sequenceSettings
#from gemsModules.sequence.structureInfo import *

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

