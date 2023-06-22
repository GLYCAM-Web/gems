#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.default_requests import Default_Service_Request_Manager

from gemsModules.structurefile.PDB.main_api import AmberMDPrep_Service_Request

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Default_Service_Request_Manager(Default_Service_Request_Manager):
    def get_default_services_aaops(self) -> List[AAOP]:
        this_service = AmberMDPrep_Service_Request()
        this_aaop = AAOP(
            AAO_Type="PDB",
            The_AAO=this_service,
            ID_String=uuid.uuid4(),
            Dictionary_Name="Default_PDB",
        )
        return [this_aaop]
