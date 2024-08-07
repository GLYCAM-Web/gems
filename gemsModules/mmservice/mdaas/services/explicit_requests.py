
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.logging.logger import Set_Up_Logging

from .settings.explicit_modules import explicit_modules


log = Set_Up_Logging(__name__)


class mdaas_Explicit_Request_Manager(Explicit_Service_Request_Manager):
    pass
    # def validate_service_request(self, service_request):
    #     # TODO/FIX: this is inefficient, we should be validating the service_request appropriately by more internal GEMS structure.
    #     validated = explicit_modules[service_request.typename].parse_obj(service_request)
    #     log.debug("validated mdaas service request:")
    #     log.debug(validated)
    #     return validated