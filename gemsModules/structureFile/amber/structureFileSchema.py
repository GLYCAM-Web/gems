#!/usr/bin/env python3
import os, sys, json, importlib.util
import pathlib
import traceback
import gemsModules.structureFile.amber.io as amberIO
from gemsModules.common.loggingConfig import *
from gemsModules.common.logic import getGemsHome

# from gemsModules.common.logic import updateResponse, getGemsHome


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

# 1) Define one structure for each type of record.
## UnrecognizedAtom ##
## UnrecognizedMolecule ##
## MissingResidue ##
## HistidineProtonation ##
## DisulfideBond ##
## ChainTermination ##
## ReplacedHydrogen ##

# 2) Provide table metadata for things like labels.

##  @brief Build the data needed for the pdb options tables.
##  @detail Use classes in io.py to generate schema that will be used to build models.py. 
##          Primarily for use by the pdb app in the website.
def generateStructureFileSchemaForWeb():
    log.info("generateStructureFileSchemaForWeb() was called.")
    try:
        amberIO.generateSchemaForWeb()
    except Exception as error:
        log.error("There was a problem generating the schema for the structureFile gemsModule: " + str(error))
        log.error(traceback.format_exc())
        raise error


if __name__ == "__main__":
    generateStructureFileSchemaForWeb()
