import uuid

from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.logging.logger import Set_Up_Logging

from .settings.explicit_modules import explicit_modules


log = Set_Up_Logging(__name__)


class GpBuilder_Explicit_Request_Manager(Explicit_Service_Request_Manager):
    # def validate_service_request(self, service_request):
    #     log.debug("validating GpB service request: {}, typename:{}".format(service_request, service_request.typename))
    #     validated = explicit_modules[service_request.typename].parse_obj(service_request)
    #     log.debug("validated GpB service request:")
    #     log.debug(validated)
    #     return validated
    
    def copy_explicit_services(self):
        the_root = self.entity.services.__root__ 
        log.debug("In Explicit_Service_Request_Manager, copy_explicit_services")
        log.debug("the_root is: ")
        log.debug(the_root)
        for supplied_name in the_root:
            log.debug("the supplied name is: " + supplied_name)
            service_request = self.validate_service_request(the_root[supplied_name].copy(deep=True))
            log.debug("the service request is: ")
            log.debug(service_request)
            this_aaop = AAOP(Dictionary_Name=supplied_name, 
                    ID_String=uuid.uuid4(),
                    The_AAO=service_request,
                    AAO_Type=service_request.typename)
            log.debug("the aaop is: ")
            log.debug(this_aaop)
            log.debug("done printing the aaop")
            self.aaop_list.append(this_aaop)