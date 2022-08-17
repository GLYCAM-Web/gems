#!/usr/bin/env python3
from collections import namedtuple
from typing import List

from gemsModules.docs.microcosm.common.loggingConfig import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


NoticeDatum = namedtuple(
        "NoticeDatum",
            "Brief Scope Messenger Type Code Message")
NoticeData : List[NoticeDatum] = []

NoticeData.append(NoticeDatum(
    'NoEntityDefined', 
    'Transaction', 
    'Common Servicer', 
    'error', 
    '301', 
    'The JSON object does not contain an Entity.'))
NoticeData.append(NoticeDatum(
    'EntityNotKnown', 
    'Entity', 
    'Common Servicer', 
    'error', 
    '302', 
    'The entity in this JSON Onject is not known to the commonServicer.'))
NoticeData.append(NoticeDatum(
    'NoTypeForEntity', 
    'Entity', 
    'Common Servicer', 
    'error', 
    '303', 
    'The Entity does not contain a type.'))
NoticeData.append(NoticeDatum(
    'JsonParseEror', 
    'Transaction', 
    'Common Servicer', 
    'error', 
    '304', 
    'There was an unknown error parsing the JSON Object.'))
NoticeData.append(NoticeDatum(
    'ServiceNotKnownToEntity', 
    'Service', 
    'Common Servicer', 
    'error', 
    '305', 
    'The requested Entity does not offer this Service.'))
NoticeData.append(NoticeDatum(
    'RequestedEntityNotFindable', 
    'SystemError', 
    'Common Servicer', 
    'error', 
    '310', 
    'The requested Entity is known, but does not respond.'))
NoticeData.append(NoticeDatum(
    'EmptyPayload', 
    'Transaction', 
    'Common Servicer', 
    'error', 
    '400', 
    'Missing or empty input payload.'))
NoticeData.append(NoticeDatum(
    'InvalidInput', 
    'Transaction', 
    'Common Servicer', 
    'error', 
    '400', 
    "Invalid input"))
NoticeData.append(NoticeDatum(
    'GmmlError', 
    'SyatemError', 
    'Common Servicer', 
    'error', 
    '315', 
    'An interaction with GMML failed.'))
NoticeData.append(NoticeDatum(
    'GemsError', 
    'SystemError', 
    'Common Servicer', 
    'error', 
    '315', 
    'There was an error in GEMS'))
NoticeData.append(NoticeDatum(
    'InvalidInputPayload', 
    'Transaction', 
    'Common Servicer', 
    'error', 
    '400', 
    'An invalid payload was detected.'))
NoticeData.append(NoticeDatum(
    'NoInputPayloadDefined', 
    'Transaction', 
    'Common Servicer', 
    'error', 
    '400', 
    'No payload could be found.'))
NoticeData.append(NoticeDatum(
    'UnknownError', 
    'Unknown', 
    'Common Servicer', 
    'error', 
    '500', 
    'We really have no idea what went wrong.'))

#from pprint import pprint
##pprint(NoticeData)
#for noticedatum in NoticeData :
#    pprint(noticedatum._asdict())
