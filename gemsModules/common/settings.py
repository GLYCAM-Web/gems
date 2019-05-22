#!/usr/bin/env python3
from gemsModules import common 
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## TODO: put some of this data into an in-memory sqlite db

## Who I am
WhoIAm='CommonServicer'

## Module names for entities that this entity/module knows.
EntityModules = {
        'Delegator' = 'delegator'
        'Sequence' = 'sequence'
        'Glycoprotein' = 'glycoprotein'
        }
## Module names for services that this entity/module can perform.
ServiceModules = {
        'Marco' : 'marco',
        'ListEntities' : 'listEntities',
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
        'RequestedEntityNotFindable':'error'
        }
ExitCodes = {
        'NoEntityDefined':'301',
        'EntityNotKnown':'302',
        'NoTypeForEntity':'303',
        'JsonParseEror':'304',
        'RequestedEntityNotFindable':'310'
        }
ExitMessages = {
        'NoEntityDefined':'The JSON object does not contain an Entity.',
        'EntityNotKnown':'The entity in this JSON Onject is not known to the commonServicer.',
        'NoTypeForEntity':'The Entity does not contain a type.',
        'JsonParseEror':'There was an unknown error parsing the JSON Object.',
        'RequestedEntityNotFindable':'The requested Entity is known, but does not respond.'
        }

## TODO Make this sort of thing ultimately part of the Notice class.
def appendCommonParserNotice(thisTransaction: Transaction,  noticeBrief: str):
    # Build the notice
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
        thisTransaction.response_dict['entity']={}
    if thisTransaction.response_dict['entity'] is None:
        thisTransaction.response_dict['entity']={}
    if not 'responses' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['responses']=[]
    thisTransaction.response_dict['entity']['responses'].append({
            'type':'errorNotice',
            'notice' : {
                'type' : commonServicesExitTypes[noticeBrief],
                'code' : commonServicesExitCodes[noticeBrief],
                'brief' : noticeBrief,
                'message' : commonServicesExitMessages[noticeBrief],
                }
            })


