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

## Information about error messages this entity/module might return.
ExitTypes = {
    'NoEntityDefined':'error',
    'EntityNotKnown':'error',
    'NoTypeForEntity':'error',
    'JsonParseEror':'error',
    'ServiceNotKnownToEntity':'error',
    'RequestedEntityNotFindable':'error',
    'EmptyPayload':'error',
    'InvalidInput':'error',
    'GmmlError':'error'
}

ExitBlockIDs = {
    'NoEntityDefined':'Transaction',
    'EntityNotKnown':'Entity',
    'NoTypeForEntity':'Entity',
    'JsonParseEror':'Transaction',
    'ServiceNotKnownToEntity':'Service',
    'RequestedEntityNotFindable':'SystemError',
    'EmptyPayload':'Transaction',
    'InvalidInput':'Transaction',
    'GmmlError':'SyatemError',
    'InvalidInputPayload':'Transaction',
    'NoInputPayloadDefined':'Transaction'
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
    'InvalidInput':'400'
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
    'GmmlError':'An interaction with GMML failed.'
}

## TODO Make this sort of thing ultimately part of transaction.py (eg Notice class).
def appendCommonParserNotice(thisTransaction: Transaction,  noticeBrief: str, blockID: str = None):
    log.info("appendCommonParserNotice() was called.\n")
    # Build the notice
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
        thisTransaction.response_dict['entity']={}

    if thisTransaction.response_dict['entity'] is None:
        thisTransaction.response_dict['entity']={}

    if not 'type' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['type'] = 'CommonServicer'


    if not 'responses' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['responses']=[]

    if blockID is None:
        if noticeBrief in ExitBlockIDs:
            blockID = ExitBlockIDs[noticeBrief]
        else:
            blockID = 'unknown'

    thisTransaction.response_dict['entity']['responses'].append({
            'CommonServicerNotice' : {
            'type' : ExitTypes[noticeBrief],
            'notice' : {
                'code' : ExitCodes[noticeBrief],
                'brief' : noticeBrief,
                'blockID' : blockID,
                'message' : ExitMessages[noticeBrief],
                }
            }})

