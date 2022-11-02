import gemsModules
#from shutil import copyfile
from gemsModules.project import settings as projectSettings
from gemsModules.common import logic as commonlogic
#from gemsModules.project import io as projectio
#from gemsModules.common import io as commonio
#from gemsModules.common import services as commonservices
#from gemsModules.common import utils as commonutils
from gemsModules.common.loggingConfig import *
import traceback
#from datetime import datetime

#import json, os, sys, uuid

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  Set up a new project's contents.  The contents can be 
#   based on defaults or on the content in a reference project.
#   By default, existing contents of the project will be protected.
#   Allow them to be overwritten by setting noClobber to False.
#   @param Project
#
#   Generally, an outgoing Project should have been generated by
#   being  coped from an incoming one, if it exists.  For that
#   reason, noClobber is set to True by default.  This will keep
#   the script from overwriting any existing data.
def defaultInitializeProject(self, noClobber : bool = True):
    log.info("defaultInitializeProject() was called.\n")

    #  The format for the output paths is"
    #    /filesystem_path/entity_ID/service_ID/service_organizational_unit(s)
    self.setFilesystemPath()
    self.setServiceDir()
    self.setProjectDir()

