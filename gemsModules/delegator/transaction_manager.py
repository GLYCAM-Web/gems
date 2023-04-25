#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.delegator.project_manager import delegator_Project_Manager
from gemsModules.delegator.services.request_manager import delegator_Request_Manager
from gemsModules.delegator.services.response_manager import delegator_Response_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.common.services.servicer import Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class delegator_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  delegator_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = Servicer
        self.response_manager_type = delegator_Response_Manager
        self.project_manager_type = delegator_Project_Manager
   


