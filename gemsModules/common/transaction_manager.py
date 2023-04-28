#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair
from gemsModules.common.main_api import Transaction
from gemsModules.common.project_manager import common_Project_Manager
from gemsModules.common.services.request_manager import common_Request_Manager
from gemsModules.common.services.response_manager import Response_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.common.services.servicer import commonservices_Servicer

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
        log.debug("about to manage project")
        self.manage_project()
        log.debug("about to manage requests")
        self.manage_requests()
        log.debug("about to generate aaop tree pair")
        self.generate_aaop_tree_pair()
        log.debug("about to invoke servicer")
        self.invoke_servicer()
        log.debug("about to manage responses")
        self.manage_responses()
        log.debug("about to update transaction")
        self.update_transaction()
        log.debug("about to return transaction")
        return self.transaction
    
    @abstractmethod
    def set_local_modules(self):
        self.request_manager_type =  common_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = commonservices_Servicer
        self.response_manager_type = Response_Manager
        self.project_manager_type = common_Project_Manager
    
    def manage_project(self):
        self.project_manager = self.project_manager_type(project=self.incoming_project, entity=self.incoming_entity)
        self.response_project = self.project_manager.process()
        
    def manage_requests(self):
        self.request_manager = self.request_manager_type(entity=self.incoming_entity, project=self.response_project)
        self.aaop_request_list : List[AAOP] = self.request_manager.process()
        log.debug("the aaop request list is: ")
        log.debug(self.aaop_request_list)

    def generate_aaop_tree_pair(self):
        self.aaop_tree_pair_manager=self.aaop_tree_pair_manager_type(aaop_request_list=self.aaop_request_list)
        self.aaop_tree_pair : AAOP_Tree_Pair = self.aaop_tree_pair_manager.process()
        log.debug("the tree pair is: ")
        log.debug(self.aaop_tree_pair)

    def invoke_servicer(self): 
        log.debug("about to invoke the following servicer")
        log.debug(self.this_servicer_type)
        self.this_servicer = self.this_servicer_type(tree_pair=self.aaop_tree_pair)
        log.debug("about to serve")
        self.aaop_tree_pair = self.this_servicer.serve()
        log.debug("after serving, the tree pair is: ")
        log.debug(self.aaop_tree_pair)

    def manage_responses(self):
        self.response_manager = self.response_manager_type(aaop_tree_pair=self.aaop_tree_pair)
        self.response_entity = self.response_manager.process()

    def update_transaction(self):
        this_transaction_type = self.transaction.get_API_type()
        entity_json = self.response_entity.dict(by_alias=True)
        this_json={}
        this_json["entity"] = entity_json
        self.transaction.outputs=this_transaction_type.parse_obj(this_json)
        log.debug("the transaction outputs are: ")
        log.debug(self.transaction.outputs.json(indent=2, by_alias=True))
        if self.response_project is not None:
            self.transaction.outputs.project=self.response_project.copy(deep=True)
