#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common import io as commonio
from gemsModules.project import io as projectio
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.conjugate.glycoprotein import settings
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class GlycosylationSitesMetadata(BaseModel):
    app : str = "gp"
    page : str = "addGlycans"
    pages : [str]  = [ "addGlycans", "reviewGlycosylation" ]
    label : str = "Glycosylation Site"
    tableKey : str = "glycosylationSites"
    interactionRequirement : str = "optional"
    urgency : str = "info"
    count : int = 0
    description : str = "Add, Remove or Change Glycosylation"
    descriptions : [str] = [ "Add, Remove or Change Glycosylation" , "Review Glycosylation" ] 

class GlycosylationSiteInfo(BaseModel):
    chain : str = "?"
    residueNumber : str = "?"
    insertionCode : str = "?"
    sequenceContext : str = ""
    occupied : bool = False
    attachedGlycanSpecifier : str = None ## 'Sequence' or 'Library'
    attachedGlycan : str = None
    tags : [str] = []

    def __init__(self, **data : Any):
        super().__init__(**data)
        log.info("Initializing Glycosylation Site Info.")
        log.debug("the data " + repr(self))
        if occupied == True:
            if attachedGlycan is None :
                except AttributeError:
                    log.error("Site set as occupied but has no glycan.")
        if attachedGlycan is not None :
            if attachedGlycanSpecifier is None :
                except AttributeError:
                    log.error("attachedGlycanSpecifier must not be None.")
            if occupied == False:
                log.debug("Found attached glycan but occupied=False; fixing.")
                self.occupied=True

class GlycoproteinInputs(BaseModel):
    sites : [GlycosylationSiteInfo] = []


class glycoproteinModuleIO(commonio.TransactionSchema):
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
class Transaction: ## base off of commonio.Transaction???
    """Holds information relevant to a delegated transaction"""
    incoming_string :str = None
    inputs : glycoproteinModuleIO
    outputs: glycoproteinModuleIO
    outgoing_string : str = None


    def __init__(self, in_string):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        import json
        # ## I think it is wrong to have Transaction call something from
        # ## some other place to modify itself, but I don't have time to
        # ## refactor this all to make it right.  Lachele 2021-04-02
        from gemsModules.common import services as commonServices
        from gemsModules.common import settings as commonSettings
        from gemsModules.common import io as commonio

        ##The following debug line is sometimes useful, but normally redundant.
        #log.debug("The in_string is: " + in_string)
        self.incoming_string = in_string
        ##The following debug lines are also sometimes useful, but normally redundant.
        # log.debug("The incoming_string is: " )
        # log.debug(self.incoming_string)
        if self.incoming_string is None :
            commonSettings.generateCommonParserNotice(noticeBrief='InvalidInput', messagingEntity=commonSettings.WhoIAm)
            return
        else :
            self.request_dict = json.loads(self.incoming_string)
            ##The following debug lines are also sometimes useful, but normally redundant.
            # log.debug("The request_dict is: " )
            # log.debug(self.request_dict)

        if self.incoming_string is None :
            commonSettings.generateCommonParserNotice(noticeBrief='InvalidInput', messagingEntity=commonSettings.WhoIAm)
            return


    def generateCommonParserNotice(self, *args, **kwargs) :
        if self.transaction_out is None :
            self.transaction_out = TransactionSchema()
        self.transaction_out.generateCommonParserNotice(*args, **kwargs)

    def populate_transaction_in(self):

        self.transaction_in = TransactionSchema(**self.request_dict)
        log.debug("The transaction_in is: " )
        log.debug(self.transaction_in.json(indent=2))

    def getProjectIn(self):
        log.info("getProjectFromTransactionIn() was called.\n")
        try :
            if all(v is not None for v in [
                self.transaction_in ,
                self.transaction_in.project ]) :
                log.debug("Found a non-None project in transaction_in of type : " + str(type(self.transaction_in.project)))
                return self.transaction_in.project
            else:
                return None
        except Exception as error :
            log.error("There was a problem getting the project from transaction_in :  " + str(error))
            raise error
    def getProjectOut(self):
        log.info("getProjectFromTransactionOut() was called.\n")
        try :
            if all(v is not None for v in [
                self.transaction_out ,
                self.transaction_out.project ]) :
                log.debug("Found a non-None project in transaction_out of type : " + str(type(self.transaction_out.project)))
                return self.transaction_out.project
            else:
                return None
        except Exception as error :
            log.error("There was a problem getting the project from transaction_out :  " + str(error))
            raise error

    def getSchemaLocation() :
        thisProject=self.getProjectOut()
        return thisProject.getFilesystemPath()


    ######
    ######  This needs to change to look like the method in sequence.io
    ######
    def build_outgoing_string(self):
        if self.transaction_out.prettyPrint is True :
            self.outgoing_string = self.transaction_out.json(indent=2)
        else :
            self.outgoing_string = self.transaction_out.json

        

    


## OG Never tested code, just showing what it might look like:
 class TheGlycosylationSiteInput(BaseModel):
     proteinResidueId : str = None  # E.g. ?_20 if no chain ID and residue number is 20. C_20 if chain id is C.
     glycanInputType : str = None # "Library" if pre-build as a pdb file (not implemented for website) or "Sequence" if glycam condensed nomenclature.
     glycanInput :  str = None # E.g. E.g. DGlcpNAcb1-4DGlcpNAcb1-OH if "Sequence".

 class GlycoproteinBuilderInputs(BaseModel): 
     workingDirectory : str = None
         workingDirectory = "Default"
     prepFileLocation : str = None
         prepFileLocation = "Default"
     substrateFileName : str = None
         substrateFileName = "Undefined"
     number3DStructures : str = None
         number3DStructures = "1"
     maxThreads : str = None
         maxThreads = "1" 
     presistCycles : str = None 
         presistCycles = "5"
     overlapTolerance : str = None
         overlapTolerance = "0.1"
     isDeterministic : str = None
         isDeterministic = "false"
     glycositesInputVector : List[TheGlycosylationSiteInput] = [] 

    gpbInStruct.isDeterministic_ = "true" # Only good for testing, so you get the same 3D structure each time. Don't do this in live site, overlap algo is better with rng.
    gpbInStruct.prepFileLocation_ = "gmml/dat/prep/GLYCAM_06j-1_GAGS.prep" # "Default" doesn't work at gems level.
    glycositeInputA = gmml.GlycositeInput("F_24", "Sequence", "DManpa1-6[DManpa1-2DManpa1-2DManpa1-3]DManpb1-4DGlcpNAcb1-4DGlcpNAcb1-OH")
    glycositeInputB = gmml.GlycositeInput("A_40", "Sequence", "DGalpNAca1-OH")
    gpbInStruct.glycositesInputVector_.append(glycositeInputA)
    gpbInStruct.glycositesInputVector_.append(glycositeInputB)

    gpBuilder = gmml.GlycoproteinBuilder(gpbInStruct)
    gpBuilder.ResolveOverlaps()
    gpBuilder.WriteOutputFiles()
    




def generateSchema():
    import json
    #print(Service.schema_json(indent=2))
    print(TransactionSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()

