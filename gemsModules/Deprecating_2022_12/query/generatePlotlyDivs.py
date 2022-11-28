#!/usr/bin/env python3

import os
import subprocess
import sys
import json
import gemsModules
from inspect import currentframe, getframeinfo
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.common.loggingConfig import *
from gemsModules.query import plotlyChiEnergy

if loggers.get(__name__):
    pass
else:
  log = createLogger(__name__)

exitMessages = {
        'GmmlNotFound':'Cannot load the GMML module',
        }
exitCodes = {
        'GmmlNotFound':'12345',
        }

# import gems/gmml stuff
import gmml
if gmml is None:
    log.error(exitMessages["GmmlNotFound"])
    sys.exit(exitCodes["GmmlNotFound"])
    
if len(sys.argv) < 3:
  log.error("You need to provide the oligo and the linkageID to run this script")
  print("Usage: python3 generatePlotlyDivs.py <oligo> <linkageID>")
  sys.exit(54321)

try:
    virtLocation = os.getenv('VIRTUOSO_DB') + ":" + str(8890) + "/sparql"
except Exception as error:
    log.error("Unable to find the Virtuoso Database.  Quitting. " + str(error))
    log.error(traceback.format_exc())
    raise error
try:
    GemsPath = os.environ.get('GEMSHOME')
except Exception as error:
    log.error("Unable to find GEMSHOME " + str(error))
    log.error(traceback.format_exc())
    raise error
  
# Now I'll actually make the graphs
oligo = sys.argv[1]
linkageID = sys.argv[2]

queryString = plotlyChiEnergy.createPlotlyQuery(oligo, linkageID)

log.debug(queryString)
proc = subprocess.Popen(queryString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(out, err) = proc.communicate()
out = str(out.decode('utf-8'))
log.debug(out)
linkageJson = json.loads(out)

plotlyChiEnergy.generatePlotlyHTML(linkageJson, linkageID, writeToFile=True)