import uuid

from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.logging.logger import Set_Up_Logging

from .settings.explicit_modules import explicit_modules


log = Set_Up_Logging(__name__)


class GlycoProtein_Explicit_Request_Manager(Explicit_Service_Request_Manager):
    def validate_service_request(self, service_request):
        log.info("validate_service_request for GlycoProtein_Explicit_Request_Manager is called.")
        log.debug("validating GpB service request: {}, typename:{}".format(service_request, service_request.typename))
        validated = explicit_modules[service_request.typename].parse_obj(service_request)
        log.debug("validated GpB service request:")
        log.debug(validated)
        return validated
