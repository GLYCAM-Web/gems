#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair
from gemsModules.common.main_api import Transaction
from gemsModules.common.project_manager import common_Project_Manager
from gemsModules.common.services.request_manager import common_Request_Manager
from gemsModules.common.services.response_manager import Response_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Manager
from gemsModules.common.services.servicer import Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class Transaction_Manager(ABC):
    def __init__(self, transaction : Transaction):
        self.transaction = transaction
        self.incoming_entity = transaction.inputs.entity
        self.incoming_project = transaction.inputs.project
        self.response_entity = None
        self.aaop_tree_pair = None
        self.set_local_modules()

    def process(self):
        log.debug('Processing transaction')
        log.debug("about to manage requests")
        self.manage_requests()
        log.debug("about to generate aaop tree pair")
        self.generate_aaop_tree_pair()
        log.debug("about to invoke servicer")
        self.invoke_servicer()
        log.debug("about to manage responses")
        self.manage_responses()
        log.debug("about to manage project")
        self.manage_project()
        log.debug("about to update transaction")
        self.update_transaction()
        log.debug("about to return transaction")
        return self.transaction
    
    @abstractmethod
    def set_local_modules(self):
        self.request_manager =  common_Request_Manager(entity=self.incoming_entity, project=self.incoming_project)
        self.aaop_tree_pair_manager = AAOP_Tree_Pair_Manager()
        self.this_servicer = Servicer(tree_pair=self.aaop_tree_pair)
        self.response_manager = Response_Manager(aaop_tree_pair=self.aaop_tree_pair)
        self.project_manager = common_Project_Manager(project=self.incoming_project, entity=self.response_entity)
    
    def manage_requests(self):
        self.aaop_request_list : List[AAOP] = self.request_manager.process()

    def generate_aaop_tree_pair(self):
        self.aaop_tree_pair : AAOP_Tree_Pair = self.aaop_tree_pair_manager.process()

    def invoke_servicer(self): 
        self.aaop_tree_pair = self.this_servicer.serve()

    def manage_responses(self):
        self.response_entity = self.response_manager.process()

    def manage_project(self):
        self.response_project = self.project_manager.process()
        
    def update_transaction(self):
        self.transaction.outputs.entity = self.response_entity
        self.transaction.outputs.project = self.response_project
