#!/usr/bin/env python3
import sys
import os
import gmml
from gemsModules.common.loggingConfig import *

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.DEBUG

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)


def getPrepFileName():
    log.info("getPrepFileName() was called.\n")
    try:
        prepFileName = sys.argv[1]
        return prepFileName
    except Exception as error:
        log.error("There was a problem getting the prepfile.")
        log.error("Error type: " + str(type(error)))
        log.error("Error details: " + str(error))
        return error

#buildThis(theSequence,  prepFile, offFile, pdbFile)
# TODO: fix this. It breaks everything.
def buildThis(sequence, prepFile, offFile, pdbFile):
    log.info("buildThis() was called.\n")
    log.debug("sequence: " + sequence)
    log.debug("prepFile: " + prepFile)
    log.debug("offFile: " + offFile)
    log.debug("pdbFile: " + pdbFile)

    prep = gmml.PrepFile(prepFile)
    assembly = gmml.Assembly()
    assembly.SetName("CONDENSEDSEQUENCE")
    assembly.BuildAssemblyFromCondensedSequence(sequence, prep)
    assembly.CreateOffFileFromAssembly(offFile, 0)
    content = assembly.BuildPdbFileStructureFromAssembly()

    content.Write(pdbFile)


def logHello():
    log.info("Hello")

def main():
    log.info("buildFromSequence.py was called.")
    thisFileName = sys.argv[0]

    prepFileName = sys.argv[1]

    sequence = sys.argv[2]

    outOffFileName = sys.argv[3]

    outPdbFileName = sys.argv[4]

    log.debug("thisFile: " + thisFileName)
    log.debug("prepFile: " + prepFileName)
    log.debug("sequence: " + sequence)
    log.debug("outOff: " + outOffFileName)
    log.debug("outPdb: " + outPdbFileName)

    prep = gmml.PrepFile(prepFileName)
    assembly = gmml.Assembly()
    assembly.SetName("CONDENSEDSEQUENCE")
    assembly.BuildAssemblyFromCondensedSequence(sequence, prep)
    assembly.CreateOffFileFromAssembly(outOffFileName, 0)
    content = assembly.BuildPdbFileStructureFromAssembly()

    content.Write(outPdbFileName)


if __name__ == "__main__":
    main()
