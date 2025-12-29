#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.complex.GpBuilder.project_manager import Gpbuilder_Project_Manager
from gemsModules.complex.GpBuilder.services.request_manager import Gpbuilder_Request_Manager
from gemsModules.complex.GpBuilder.services.response_manager import Gpbuilder_Response_Manager
from gemsModules.complex.GpBuilder.services.servicer import Gpbuilder_Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class Gpbuilder_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  Gpbuilder_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = Gpbuilder_Servicer
        self.response_manager_type = Gpbuilder_Response_Manager
        self.project_manager_type = Gpbuilder_Project_Manager
   


