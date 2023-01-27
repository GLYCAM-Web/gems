#!/usr/bin/env python3
from gemsModules.common.main_api import Transaction
from gemsModules.common.action_associated_objects import AAOP_Tree
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Transaction_Input_Translator:

    def __init__(self, transaction : Transaction):
        self.transaction = transaction
        self.incoming_tree = AAOP_Tree()

    def translate(self):
        self.translate_top_level_inputs_into_implicit_service_packages(self)
        self.add_explicit_service_packages(self)  # Logic should live in service management
        self.fill_transaction_level_data(self) 

    def fill_transaction_service_requests(self):
        pass

    def get_incoming_tree(self):
        return self.incoming_tree



class Transaction_Output_Translator:

        def build_transaction_outputs(self)

        def add_top_level_outputs(self)
