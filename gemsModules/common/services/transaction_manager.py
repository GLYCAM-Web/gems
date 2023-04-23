#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.main_api import Transaction


class Transaction_Manager(ABC):
    def __init__(self, transaction : Transaction):
        self.transaction = transaction

    def process(self):
        self.manage_requests()
        self.generate_workflow()
        self.invoke_servicer()
        self.manage_responses()
        self.manage_project()
        return self.transaction.build_outgoing_string()
    
    @abstractmethod
    def manage_requests(self):
        pass

    @abstractmethod
    def generate_workflow(self):
        pass

    @abstractmethod
    def invoke_servicer(self): 
        pass

    @abstractmethod
    def manage_responses(self):
        pass

    @abstractmethod
    def manage_project(self):
        pass

