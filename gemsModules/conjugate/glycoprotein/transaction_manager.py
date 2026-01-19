#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.conjugate.glycoprotein.project_manager import GlycoProtein_Project_Manager
from gemsModules.conjugate.glycoprotein.services.request_manager import GlycoProtein_Request_Manager
from gemsModules.conjugate.glycoprotein.services.response_manager import GlycoProtein_Response_Manager
from gemsModules.conjugate.glycoprotein.services.servicer import GlycoProtein_Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class GlycoProtein_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  GlycoProtein_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = GlycoProtein_Servicer
        self.response_manager_type = GlycoProtein_Response_Manager
        self.project_manager_type = GlycoProtein_Project_Manager
   


