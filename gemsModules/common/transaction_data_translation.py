#!/usr/bin/env python3
from abc import ABC
from typing import List
from gemsModules.common.main_api import Transaction
from gemsModules.common.main_api_services import Services
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Transaction_Input_Translator(ABC):

    def __init__(self, transaction : Transaction):
        self.transaction = transaction
        self.incoming_list : List[Services] = []

    def translate(self):
        self.translate_top_level_inputs_into_implicit_service_packages(self)
        self.add_explicit_service_packages(self)  # Logic should live in service management
        self.fill_transaction_level_data(self) 

    def fill_transaction_service_requests(self):
        pass

    def get_incoming_list(self):
        return self.incoming_list



class Transaction_Output_Translator(ABC):

    def __init__(self, transaction : Transaction):
        self.transaction = transaction

    def translate(self):
        self.build_transaction_outputs(self)
        self.add_top_level_outputs(self)

    def build_transaction_outputs(self):
        pass

    def add_top_level_outputs(self):
        pass
