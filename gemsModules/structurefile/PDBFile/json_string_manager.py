#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.structurefile.PDBFile.main_settings import WhoIAm
from gemsModules.structurefile.PDBFile.main_api import PDBFile_Transaction
from gemsModules.structurefile.PDBFile.transaction_manager import (
    PDBFile_Transaction_Manager,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Json_String_Manager(Json_String_Manager):
    def get_local_components(self):
        self.transaction = PDBFile_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = PDBFile_Transaction_Manager
