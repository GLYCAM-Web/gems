#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.TEMPLATE.project_manager import template_Project_Manager
from gemsModules.TEMPLATE.services.request_manager import template_Request_Manager
from gemsModules.TEMPLATE.services.response_manager import template_Response_Manager
from gemsModules.TEMPLATE.services.servicer import template_Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class template_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  template_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = template_Servicer
        self.response_manager_type = template_Response_Manager
        self.project_manager_type = template_Project_Manager
   


