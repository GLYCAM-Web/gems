#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.default_requests import Default_Service_Request_Manager

from gemsModules.common.services.marco.api import marco_Request

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class mdaas_Default_Service_Request_Manager(Default_Service_Request_Manager):
    def get_default_services_aaops(self) -> List[AAOP]:
        this_service = marco_Request()
        this_aaop = AAOP(
            AAO_Type="Marco",
            The_AAO=this_service,
            ID_String=uuid.uuid4(),
            Dictionary_Name="Default_Marco",
        )
        return [this_aaop]
