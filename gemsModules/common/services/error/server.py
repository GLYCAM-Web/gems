#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response
from gemsModules.common.main_api_notices import Notices
#from gemsModules.common.services.error.logic import error

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(request : Service_Request) -> Service_Response:
    log.info("The error server was called.")
    response = Service_Response()
    response.typename = 'Error'
    response.typename = request.typename
    response.outputs = { 'message' : 'The error service is not quite written yet, but something went wrong.' }
    response.notices = Notices()
    response.notices.addDefaultNotice(Brief='InvalidInput', Messenger='Common Sevicer')
    return response


