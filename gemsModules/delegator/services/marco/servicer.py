#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request,  Service_Response

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : Service_Request) -> Service_Response:
   log.info("The marco servicer was called.")
   response = Service_Response()
   if service.typename != 'Marco' :
       response.typename = service.typename
       response.outputs = { 'message' : 'Incorrect typename sent to Marco Servicer.' }
       from .main_api_notices import Notices
       response.notices = Notices()
       response.notices.addDefaultNotice(Brief='InvalidInput', Messenger='Marco Sevicer')
   else :
       from .marco import marco
       response.typename = 'Marco'
       response.outputs = marco(service.inputs)
   return response


