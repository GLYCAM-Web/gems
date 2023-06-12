#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.ambermdprep.main_settings import WhoIAm
from gemsModules.ambermdprep.main_api import AmberMDPrep_Transaction
from gemsModules.ambermdprep.transaction_manager import AmberMDPrep_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Json_String_Manager(Json_String_Manager):
    def get_local_components(self):
        self.transaction = AmberMDPrep_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = AmberMDPrep_Transaction_Manager
