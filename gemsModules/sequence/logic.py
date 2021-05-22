#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from multiprocessing import Process
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.project import settings as projectSettings
from gemsModules.project import io as projectio
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.common.loggingConfig import *
from . import settings as sequenceSettings
from gemsModules.sequence import projects as sequenceProjects
from .structureInfo import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief convenience method. pass transaction, get options dict.
##  TODO: evaluate for deprecation. Not terribly useful.
#
# This should probably move to transactin in io.py
#
def getOptionsFromTransaction(thisTransaction: sequenceio.Transaction):
    log.info("getOptionsFromTransaction() was called.")
    if "options" in thisTransaction.request_dict.keys():
        log.debug("Found options.")
        return thisTransaction.request_dict['options']
    else:
        log.debug("No options found.")
        return None

class EverLastingProcess(Process):
    def join(self, *args, **kwargs):
        pass # Overwrites join so that it doesn't block. Otherwise parent waits.

    def __del__(self):
        pass


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

