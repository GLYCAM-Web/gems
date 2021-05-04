#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from gemsModules.common.loggingConfig import *

from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## TODO: put some of this data into an in-memory sqlite db

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


## Who I am
WhoIAm='CommonServicer'

status = "Stable"
moduleStatusDetail = "Can provide Marco, ReturnHelp, ReturnUsage, ReturnVerboseHelp, and ReturnSchema services."

servicesStatus = [
    {
        "service" : "Marco",
        "status" : "Stable.",
        "statusDetail" : "Returns Polo if all is well."
    },
    {
        "service" : "ReturnHelp",
        "status" : "Stable.",
        "statusDetail" : "Returns brief help message if provided in gemsModule."
    },
    {
        "service" : "ReturnUsage",
        "status" : "Stable.",
        "statusDetail" : "Returns usage help message if provided in gemsModule."
    },
    {
        "service" : "ReturnVerboseHelp",
        "status" : "Stable",
        "statusDetail" : "Returns more detailed help message if provided in gemsModule."
    },
    {
        "service" : "ReturnSchema",
        "status" : "Stable",
        "statusDetail" : "Returns a schema upon request."
    }
]

schemaLocation = "/website/userdata/"

## Module names for entities that this entity/module knows.
subEntities = {
    'BatchCompute' : 'batchcompute',
    'CommonServices' : 'common',
    'Conjugate' : 'conjugate',
    'Delegator' : 'delegator',
    'Graph' : 'graph',
    'Query' : 'query',
    'MmService' : 'mmservice',
    'Project' : 'project',
    'Sequence' : 'sequence',
    'Status' : 'status',
    'StructureFile' : 'structureFile'

}

## Module names for services that this entity/module can perform.
serviceModules = {
    'Marco' : 'marco',
    'ReturnHelp' : 'returnHelp',
    'ReturnUsage' : 'returnHelp',
    'ReturnVerboseHelp' : 'returnHelp',
    'ReturnSchema' : 'returnHelp'
}
## The name of the text to return for various types of help
helpDict = {
    'ReturnUsage'       : 'usageText',
    'ReturnHelp'        : 'basicHelpText',
    'ReturnVerboseHelp' : 'moreHelpText',
    'ReturnSchema'      : 'schemaLocation'
}

##
##
## Notices Generator Data
##
## The key in the following dictionaries is called noticeBrief 
##
## These dictionaries contain information about error messages 
## an entity/module might return.
ExitTypes = {
    'NoEntityDefined':'error',
    'EntityNotKnown':'error',
    'NoTypeForEntity':'error',
    'JsonParseEror':'error',
    'ServiceNotKnownToEntity':'error',
    'RequestedEntityNotFindable':'error',
    'EmptyPayload':'error',
    'InvalidInput':'error',
    'GmmlError':'error',
    'GemsError':'error',
    'InvalidInputPayload':'error',
    'NoInputPayloadDefined':'error',
    'UnknownError':'error'
}
ExitScopes = {
    'NoEntityDefined':'Transaction',
    'EntityNotKnown':'Entity',
    'NoTypeForEntity':'Entity',
    'JsonParseEror':'Transaction',
    'ServiceNotKnownToEntity':'Service',
    'RequestedEntityNotFindable':'SystemError',
    'EmptyPayload':'Transaction',
    'InvalidInput':'Transaction',
    'GmmlError':'SyatemError',
    'GemsError':'SystemError',
    'InvalidInputPayload':'Transaction',
    'NoInputPayloadDefined':'Transaction',
    'UnknownError':'Unknown'
}
ExitCodes = {
    'NoEntityDefined':'301',
    'EntityNotKnown':'302',
    'NoTypeForEntity':'303',
    'JsonParseEror':'304',
    'ServiceNotKnownToEntity':'305',
    'RequestedEntityNotFindable':'310',
    'GmmlError':'315',
    'EmptyPayload':'400',
    'InvalidInput':'400',
    'GemsError':'315',
    'InvalidInputPayload':'400',
    'NoInputPayloadDefined':'400',
    'UnknownError':'500'
}
ExitMessages = {
    'NoEntityDefined':'The JSON object does not contain an Entity.',
    'EntityNotKnown':'The entity in this JSON Onject is not known to the commonServicer.',
    'NoTypeForEntity':'The Entity does not contain a type.',
    'JsonParseEror':'There was an unknown error parsing the JSON Object.',
    'ServiceNotKnownToEntity':'The requested Entity does not offer this Service.',
    'RequestedEntityNotFindable':'The requested Entity is known, but does not respond.',
    'EmptyPayload':'Missing or empty input payload.',
    'InvalidInput':'error',
    'GmmlError':'An interaction with GMML failed.',
    'GemsError':'There was an error in GEMS',
    'InvalidInputPayload':'An invalid payload was detected.',
    'NoInputPayloadDefined':'No payload could be found.',
    'UnknownError':'We really have no idea what went wrong.'
}

##
## This can probably go very soon
##
#def appendCommonParserNotice(theTransaction )  :
#    # Build the notice for older code
#        if theTransaction.response_dict is None:
#            theTransaction.response_dict={}
#            theTransaction.response_dict['entity']={}
#    
#        if theTransaction.response_dict['entity'] is None:
#            theTransaction.response_dict['entity']={}
#    
#        if not 'type' in theTransaction.response_dict['entity']:
#            theTransaction.response_dict['entity']['type'] = 'CommonServicer'
#    
#    
#        if not 'responses' in theTransaction.response_dict['entity']:
#            theTransaction.response_dict['entity']['responses']=[]
#    
#        theTransaction.response_dict['entity']['responses'].append({
#                'CommonServicerNotice' : {
#                'type' : ExitTypes[noticeBrief],
#                'notice' : {
#                    'code' : ExitCodes[noticeBrief],
#                    'brief' : noticeBrief,
#                    'blockID' : scope,
#                    'message' : ExitMessages[noticeBrief],
#                    }
#                }})
#    

# ## See above for definition of noticeBrief
def generateCommonParserNotice(
        noticeBrief     : str  = 'UnknownError' ,  # Lookup keyword for the error
        scope           : str  = None,             # Is this from entity? service? transaction?
        messagingEntity : str  = None,             # Which entity sends this message?
        exitType        : str  = None,             # Error, Warning, Info
        exitCode        : str  = None,             # Numeric code because those can be useful
        exitMessage     : str  = None,             # Human-readable brief description
        additionalInfo  : Dict = None              # Free-form dictionary of data to return 
        ):
    log.info("generateCommonParserNotice() was called.\n")

    if ExitTypes[noticeBrief] is None :
        log.info("Unknown noticeBrief, '" + noticeBrief + "', sent to generateCommonParserNotice() \n")
        noticeBrief = 'UnknownError'

    if messagingEntity is None :
        messagingEntity='CommonServicer'

    if scope is None :
        scope : str = ExitScopes[noticeBrief]
    if exitType is None :
        exitType = ExitTypes[noticeBrief],
    if exitCode is None :
        exitCode = ExitCodes[noticeBrief],
    if exitMessage is None :
        exitMessage = ExitMessages[noticeBrief],

    # Build the notice for newer code
    thisNotice = common.io.Notice()
    thisNotice.noticeType=exitType
    thisNotice.noticeCode=exitCode
    thisNotice.noticeBrief=noticeBrief
    thisNotice.noticeScope=scope
    thisNotice.noticeMessage=exitMessage
    thisNotice.messagingEntity=messagingEntity
    if additionalInfo is not None : 
        thisNotice.additionalInfo=additionalInfo

    return thisNotice
