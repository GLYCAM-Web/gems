#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.structurefile.PDBFile.project_manager import PDBFile_Project_Manager
from gemsModules.structurefile.PDBFile.services.request_manager import (
    PDBFile_Request_Manager,
)
from gemsModules.structurefile.PDBFile.services.response_manager import (
    PDBFile_Response_Manager,
)
from gemsModules.structurefile.PDBFile.services.workflow_manager import (
    PDBFile_Workflow_Manager,
)
from gemsModules.structurefile.PDBFile.services.servicer import PDBFile_Servicer

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Transaction_Manager(Transaction_Manager):
    def set_local_modules(self):
        self.request_manager_type = PDBFile_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = PDBFile_Servicer
        self.response_manager_type = PDBFile_Response_Manager
        self.project_manager_type = PDBFile_Project_Manager
        self.workflow_manager_type = PDBFile_Workflow_Manager
