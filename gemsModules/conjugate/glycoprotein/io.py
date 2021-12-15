#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, validator, PositiveFloat, PositiveInt
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonio
from gemsModules.project import io as projectio
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.conjugate import io as parentio
from gemsModules.conjugate.glycoprotein import settings
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class glycoproteinService(parentio.conjugateService):
    """Holds information about a Service requested of the Conjugate Entity."""
    ##
    ## Eventually...  if the 'entity' is specified as 'Conjugate' and 'Evaluate' is
    ##    the service, then the substrate will be sent to all submodules.  These
    ##    will include, at least, glycoprotein, glycolipid and 'glycopolymer' (or
    ##    whatever name the materials folks want to use for a glycosylated polymer).
    ##
    typename : settings.Services = Field(
        'Evaluate',
        alias = 'type',
        title = 'Requested Service',
        description = 'The service requested of the Conjugate Entity'
        )

    def __init__(self, **data : Any):
        super().__init__(**data)
        log.info("Initializing Glycoprotein Service.")
        log.debug("the data " + repr(self))
        log.debug("Init for the Services in glycoprotein was called.")


class gpGlycosylationSiteInfo(parentio.GlycosylationSiteInfo):

    def gmmlGlycositeInput():
        if residueNumber == "?" :
            raise ValueError ("residueNumber must be specified & cannot be '?'")
        siteID = self.chain + "_" + self.residueNumber + "_" + self.insertionCode
        return gmml.GlycositeInput( siteID, self.glycanSpecifier, self.glycan ) 

class gpGlycosylationIO(parentio.GlycosylationIO):
    sites : List[gpGlycosylationSiteInfo] = []

### Example use in gmml
#	std::string workingDirectory_;						// Default is to figure out current directory.
#	std::string prepFileLocation_;						// Default is to figure out install directory + ../dat/prep/GLYCAM_06j-1_GAGS.prep.
#	std::string substrateFileName_;						// Default is "Undefined", program will throw if left as "Undefined".
#	std::string number3DStructures_;					// Default is 1. //ToDo Implement this.
#	std::string maxThreads_; 							// Default is 1. //ToDo Implement this.
#	std::string persistCycles_;						    // Default is 5.
#	std::string overlapTolerance_;						// Default is 0.1
#	std::string isDeterministic_;						// Default is false
#	std::vector<GlycositeInput> glycositesInputVector_;	// No default, program will throw if uninitialized.

    def gmmlGlycoproteinBuilderInput():
        gpbInput = gmml.GlycoproteinBuilderInputs()
        gpbInput.prepFileLocation_ = self.prepFileLocation
        gpbInput.workingDirectory_ = self.workingDirectory 
        gpbInput.substrateFileName_ = self.substrateFileName 
        gpbInput.number3DStructures_ = str(self.number3DStructures) 
        gpbInput.maxThreads_ = str(self.maxThreads)
        gpbInput.persistCycles_ = str(self.persistCycles)
        gpbInput.overlapTolerance_ = str(self.overlapTolerance)
        gpbInput.isDeterministic_ = str(self.isDeterministic)
 
        for site in self.sites:
            gpbInput.glycositesInputVector_.append(site.gmmlGlycositeInput())
 
        return gpbInput

    def buildGlycoProtein(): 
        gpBuilder = gmml.GlycoproteinBuilder(self.gmmlGlycoproteinBuilderInput()) 
        gpBuilder.ResolveOverlaps() 
        gpBuilder.WriteOutputFiles()
    

class glycoproteinEntity(parentio.conjugateEntity):
    services : Dict[str,glycoproteinService] = {}
    inputs : gpGlycosylationIO = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a glycoproteinEntity")
        log.debug("entityType: " + self.entityType)

class glycoproteinModuleIO(parentio.conjugateModuleIO):
    """
    Holds info about the Transaction JSON object used in the Sequence entity.
    """
    ##  ... means a value is required in Pydantic.
    entity : glycoproteinEntity = ...
    project : projectio.GpProject = None

    def __init__(self, **data : Any):
        super().__init__(**data)


# ####
# ####  Container for use in the modules
# ####
class Transaction(parentio.Transaction): 
    """Holds information relevant to a delegated transaction"""
    inputs : glycoproteinModuleIO
    outputs: glycoproteinModuleIO


def generateSchema():
    import json
    #print(Service.schema_json(indent=2))
    print(glycoproteinModuleIO.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()

