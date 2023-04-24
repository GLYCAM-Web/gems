#!/usr/bin/env python3
from typing import List
import uuid
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_services import Service_Request

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Default_Service_Request_Manager(ABC):
    """ This should only happen if there are no services specified after the
        explicit and implicit services have been considered."""
    
    def __init__(self):
        self.aaop_list = self.get_default_services_aaops()

    @abstractmethod
    def get_default_services_aaops(self) -> List[AAOP]:
        pass

    def get_aaop_list(self):
        return self.aaop_list

class common_Default_Service_Request_Manager(Default_Service_Request_Manager):

    def get_default_services_aaops(self) -> List[AAOP]:
        this_service = Service_Request(typename="Status")
        this_service.options = {"error" : "The CommonServicer has no defailt services."}
        this_aaop = AAOP(
            The_AAO=this_service,
            ID_String=uuid.uuid4(),
            Dictionary_Name="Error"
            )
        return [this_aaop]