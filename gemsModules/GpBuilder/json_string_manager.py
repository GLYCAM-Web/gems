#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.GpBuilder.main_settings import WhoIAm
from gemsModules.GpBuilder.main_api import Gpbuilder_Transaction
from gemsModules.GpBuilder.transaction_manager import Gpbuilder_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Gpbuilder_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = Gpbuilder_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = Gpbuilder_Transaction_Manager
