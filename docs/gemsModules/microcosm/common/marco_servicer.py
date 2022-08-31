#!/usr/bin/env python3
from gemsModules.docs.microcosm.common.main_api import Transaction

from gemsModules.docs.microcosm.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

############################################################################
##  Needs to become, once data manager is implemented:   
############################################################################
##from gemsModules.docs.microcosm.common.main_api_services import Service, Response
##def Serve(service : Service) -> Response:
##    log.info("The marco servicer was called.")
##    response = Response()
##    if service.typename != 'Marco' :
##        response.typename = service.typename
##        response.outputs = { 'message' : 'Incorrect typename sent to Marco Servicer.' }
##        from gemsModules.docs.microcosm.common.main_api_notices import Notices
##        response.notices = Notices()
##        response.notices.addDefaultNotice(Brief='InvalidInput', Messenger='Marco Sevicer')
##    else :
##        response.typename = 'Marco',
##        response.outputs  = {'message': 'Polo.'},
##        response.notices  = None
##    return transaction
############################################################################

## For now, this works for testing
def Serve(transaction : Transaction):
    log.info("The marco servicer was called.")
    transaction.entity.responses.add_response(
        typename = 'Marco',
        outputs  = {'message': 'Polo.'},
        notices  = None
        )
    return transaction

