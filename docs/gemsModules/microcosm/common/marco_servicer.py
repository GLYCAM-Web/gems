#!/usr/bin/env python3
from typing import Protocol
from docs.gemsModules.microcosm.common.main_api_services import Service,  Response

from docs.gemsModules.microcosm.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


def Serve(service : Service) -> Response:
   log.info("The marco servicer was called.")
   response = Response()
   if service.typename != 'Marco' :
       response.typename = service.typename
       response.outputs = { 'message' : 'Incorrect typename sent to Marco Servicer.' }
       from gemsModules.docs.microcosm.common.main_api_notices import Notices
       response.notices = Notices()
       response.notices.addDefaultNotice(Brief='InvalidInput', Messenger='Marco Sevicer')
   else :
       from docs.gemsModules.microcosm.common.marco import marco
       response.typename = 'Marco'
       response.outputs = marco(service.inputs)
   return response


