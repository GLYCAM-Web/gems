#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.batchcompute.project_manager import Batchcompute_Project_Manager
from gemsModules.batchcompute.services.request_manager import Batchcompute_Request_Manager
from gemsModules.batchcompute.services.response_manager import Batchcompute_Response_Manager
from gemsModules.batchcompute.services.servicer import Batchcompute_Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class Batchcompute_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  Batchcompute_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = Batchcompute_Servicer
        self.response_manager_type = Batchcompute_Response_Manager
        self.project_manager_type = Batchcompute_Project_Manager
   


