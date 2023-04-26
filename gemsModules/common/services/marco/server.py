#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response
from gemsModules.common.main_api_notices import Notices
from gemsModules.common.services.marco.logic import execute as marco
from gemsModules.common.services.marco.logic import requestInputs as marcoInputs

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(request : Service_Request) -> Service_Response:
    log.info("The marco server was called.")
    response = Service_Response()
    if request.typename != 'Marco' :
        response.typename = request.typename
        response.outputs = { 'message' : 'Incorrect typename sent to Marco Servicer.' }
        response.notices = Notices()
        response.notices.addDefaultNotice(Brief='InvalidInput', Messenger='Marco Sevicer')
    else :
        if request.inputs is None:
            request.inputs = marcoInputs()
            request.inputs.entity = 'FixMe' # data afiller should do this
            request.inputs.who_I_am = 'FixMe'
        response.typename = 'Marco'
        response.outputs = marco(request)
    return response


