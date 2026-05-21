#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.batchcompute.main_settings import WhoIAm
from gemsModules.batchcompute.main_api import Batchcompute_Transaction
from gemsModules.batchcompute.transaction_manager import Batchcompute_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Batchcompute_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = Batchcompute_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = Batchcompute_Transaction_Manager
        self.initialize_out = True
