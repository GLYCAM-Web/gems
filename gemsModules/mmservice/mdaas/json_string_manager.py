#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.mmservice.mdaas.main_settings import WhoIAm
from gemsModules.mmservice.mdaas.main_api import MDaaS_Transaction
from gemsModules.mmservice.mdaas.transaction_manager import mdaas_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class MDaaS_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = MDaaS_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = mdaas_Transaction_Manager
