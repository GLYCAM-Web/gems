#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.structurefile.PDB.project_manager import PDB_Project_Manager
from gemsModules.structurefile.PDB.services.request_manager import (
    AmberMDPrep_Request_Manager,
)
from gemsModules.structurefile.PDB.services.response_manager import (
    PDB_Response_Manager,
)
from gemsModules.structurefile.PDB.services.servicer import PDB_Servicer

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Transaction_Manager(Transaction_Manager):
    def set_local_modules(self):
        self.request_manager_type = AmberMDPrep_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = PDB_Servicer
        self.response_manager_type = PDB_Response_Manager
        self.project_manager_type = PDB_Project_Manager
