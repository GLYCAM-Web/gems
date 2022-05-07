#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, validator, PositiveFloat, PositiveInt
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import jsoninterface as commonio
from gemsModules.common import settings as commonSettings
from gemsModules.project import jsoninterface as projectio
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.conjugate import settings
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class conjugateService(commonio.Service):
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
        log.info("Initializing Conjugate Service.")
        log.debug("the data " + repr(self))
        log.debug("Init for the Services in conjugate was called.")


class GlycosylationSitesMetadata(BaseModel):
    app : str = "gp"
    pages : List[str]  = [ "addGlycans", "reviewGlycosylation" ]
    label : str = "Glycosylation Site"
    tableKey : str = "glycosylationSites"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    descriptions : List[str] = [ "Add, Remove or Change Glycosylation" , "Review Glycosylation" ] 

class GlycosylationSiteInfo(BaseModel):
    chain : str = "?"
    residueNumber : str = Field(
            ...,
            description="Required Input.  This must be a valid residue number."
            )
    insertionCode : str = "?"
    sequenceContext : str = ""
    occupied : bool = False
    glycanFormat : str = Field(
            ...,
            description="Required Input.  Format in which the glycan is given.  Required if occupied=True. Possible values are 'Sequence' and 'Library'"
            )
    glycan : str = Field(
            ...,
            description="Required Input.  Glycan sequence or other ID.  Required if occupied=True. Format must match glycanFormat"
            )
    tags : List[str] = []

    def __init__(self, **data : Any):
        super().__init__(**data)
        log.info("Initializing Glycosylation Site Info.")
        log.debug("the data " + repr(self))
        if occupied == True:
            if glycan is None :
                error="Site set as occupied but has no glycan."
                log.error(error)
                raise AttributeError(error)
        if glycan is not None :
            if glycanSpecifier is None :
                error="glycanSpecifier must not be None if glycan is present."
                log.error(error)
                raise AttributeError(error)
            if occupied == False:
                log.debug("Found attached glycan but occupied=False.  Hoping that's ok.")


class GlycosylationStatus(str,Enum):
    attached = 'Attached' # glycan was successfully attached
    removed = 'Removed'  # a previously attached glycan was removed
    attachmentFailed = 'Attachment Failed' # the glycan could not be attached
    unknown = 'Unknown' # the glycan attachment status is not known

class glycosylationSiteResults(GlycosylationSiteInfo):
    clashScore : float = 123456789.0 # initialize to an absurd value
    status : GlycosylationStatus = 'Unknown'

class GlycosylationIO(BaseModel):
    sites : List[GlycosylationSiteInfo] = []
    workingDirectory : str = "CWD"
    prepFileLocation : str = "Default" # this needs much expansion
    substrateFileName : str = ...
    substrateType : str = "protein" 
    number3DStructures : int = 1
    maxThreads : int = 1
    persistCycles : int = 5
    overlapTolerance : float = 0.1
    isDeterministic : bool = False

class ConjugateOutputs(BaseModel):
    glycosylationResults : List[glycosylationSiteResults] = []
    workingDirectory : str = "CWD"
    resolvedFileName : str = None
    unresolvedFileName : str = None
    jsonFileName : str = None

class conjugateEntity(commonio.Entity):
    entityType : str = Field(
            settings.WhoIAm,
            title='Type',
            alias='type'
            )
    services : Dict[str,conjugateService] = {}
    inputs : GlycosylationIO = None
    outputs : ConjugateOutputs = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a glycoproteinEntity")
        log.debug("entityType: " + self.entityType)


class conjugateModuleIO(commonio.TransactionSchema):
    """
    Holds info about the Transaction JSON object used in the Sequence entity.
    """
    ##  ... means a value is required in Pydantic.
    entity : conjugateEntity = ...
    project : projectio.GpProject = None

    def __init__(self, **data : Any):
        super().__init__(**data)


# ####
# ####  Container for use in the modules
# ####
class Transaction(commonio.Transaction): ## base off of commonio.Transaction???
    """Holds information relevant to a delegated transaction"""
    incoming_string :str = None
    inputs : conjugateModuleIO = None
    outputs: conjugateModuleIO = None
    outgoing_string : str = None

    def __init__(self, in_string):
        super().__init__(in_string)
        log.debug("The in_string is: " + in_string)
        self.incoming_string = in_string
        if self.incoming_string is None :
            generateCommonParserNotice(noticeBrief='InvalidInput', messagingEntity=settings.WhoIAm)
            return
        try: 
            self.inputs = conjugateModuleIO.parse_raw(self.incoming_string) 
#            self.inputs.parse_raw(self.incoming_string) 
            log.debug("The inputs object is: " ) 
            log.debug(self.inputs.json(indent=2))
            self.outputs = self.inputs.copy(deep=True)
            log.debug("The outputs was initialized from the inputs.  The outputs is:")
            log.debug(self.outputs.json(indent=2))
        except ValidationError as e :
            log.error(e)
            log.error(traceback.format.exc())
            thisTransaction.generateCommonParserNotice(
                noticeBrief='JsonParseEror',
                additionalInfo={'hint' : str(e)})
            self.outgoing_string=self.outputs.json(indent=2)
            raise e
        except Exception as error :
            log.error(error)
            log.error(traceback.format.exc())
            thisTransaction.generateCommonParserNotice(
                noticeBrief='UnknownError',
                additionalInfo={'hint' : str(error)})
            raise error

    def build_outgoing_string(self):
        if self.inputs.prettyPrint is True :
            self.outgoing_string = self.outputs.json(indent=2)
        else :
            self.outgoing_string = self.outputs.json()

        

def generateSchema():
    import json
    print(conjugateModuleIO.schema_json(indent=2))

if __name__ == "__main__":
  #generateSchema()
  print("""This jsoninterface.py does little on its own.  It is the parent for
  jsoninterface.py in the specific conjugates.  Glycoprotein is the first.""")

