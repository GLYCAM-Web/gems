#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response
#from gemsModules.common.main_api_notices import Notices
#from gemsModules.common.services.error.logic import error

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(request : Service_Request) -> Service_Response:
    pass
#   log.info("The marco server was called.")
#   response = Service_Response()
#   if request.typename != 'Marco' :
#       response.typename = request.typename
#       response.outputs = { 'message' : 'Incorrect typename sent to Marco Servicer.' }
#       response.notices = Notices()
#       response.notices.addDefaultNotice(Brief='InvalidInput', Messenger='Marco Sevicer')
#   else :
#       response.typename = 'Marco'
#       response.outputs = marco(request)
#   return response


