#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair
from gemsModules.common.main_api import Transaction
from gemsModules.common.project_manager import Project_Manager
from gemsModules.common.services.request_manager import Request_Manager
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

    def process(self):
        self.manage_requests()
        self.generate_workflow()
        self.invoke_servicer()
        self.manage_responses()
        self.manage_project()
        self.update_transaction()
        return self.transaction
    
    @abstractmethod
    def manage_requests(self):
        request_manager =  Request_Manager(entity=self.incoming_entity, project=self.incoming_project)
        self.aaop_request_list : List[AAOP] = request_manager.process()

    @abstractmethod
    def generate_aaop_tree_pair(self):
        aaop_tree_pair_manager = AAOP_Tree_Pair_Manager(aaop_request_list=self.aaop_request_list)
        self.aaop_tree_pair : AAOP_Tree_Pair = aaop_tree_pair_manager.process()

    @abstractmethod
    def invoke_servicer(self): 
        this_servicer = Servicer(aaop_tree_pair=self.aaop_tree_pair)
        self.aaop_tree_pair = this_servicer.serve()

    @abstractmethod
    def manage_responses(self):
        response_manager = Response_Manager(aaop_tree_pair=self.aaop_tree_pair)
        self.response_entity = response_manager.process()

    @abstractmethod
    def manage_project(self):
        project_manager = Project_Manager(project=self.incoming_project, entity=self.response_entity)
        self.response_project = project_manager.process()
        
    def update_transaction(self):
        self.transaction.outputs.entity = self.response_entity
        self.transaction.outputs.project = self.response_project
