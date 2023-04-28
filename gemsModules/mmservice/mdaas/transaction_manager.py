#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.mmservice.mdaas.project_manager import mdaas_Project_Manager
from gemsModules.mmservice.mdaas.services.request_manager import mdaas_Request_Manager
from gemsModules.mmservice.mdaas.services.response_manager import mdaas_Response_Manager
from gemsModules.mmservice.mdaas.services.servicer import mdaas_Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class mdaas_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  mdaas_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = mdaas_Servicer
        self.response_manager_type = mdaas_Response_Manager
        self.project_manager_type = mdaas_Project_Manager
   


