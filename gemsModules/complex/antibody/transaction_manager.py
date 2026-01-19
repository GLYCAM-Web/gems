#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.complex.antibody.project_manager import (
    Antibody_Project_Manager,
)
from gemsModules.complex.antibody.services.request_manager import (
    Antibody_Request_Manager,
)
from gemsModules.complex.antibody.services.response_manager import (
    Antibody_Response_Manager,
)
from gemsModules.complex.antibody.services.servicer import Antibody_Servicer

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Antibody_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type = Antibody_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = Antibody_Servicer
        self.response_manager_type = Antibody_Response_Manager
        self.project_manager_type = Antibody_Project_Manager
