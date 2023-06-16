#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.ambermdprep.project_manager import AmberMDPrep_Project_Manager
from gemsModules.ambermdprep.services.request_manager import AmberMDPrep_Request_Manager
from gemsModules.ambermdprep.services.response_manager import (
    AmberMDPrep_Response_Manager,
)
from gemsModules.ambermdprep.services.servicer import AmberMDPrep_Servicer

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Transaction_Manager(Transaction_Manager):
    def set_local_modules(self):
        self.request_manager_type = AmberMDPrep_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = AmberMDPrep_Servicer
        self.response_manager_type = AmberMDPrep_Response_Manager
        self.project_manager_type = AmberMDPrep_Project_Manager
