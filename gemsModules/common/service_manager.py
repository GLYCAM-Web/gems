from gemsModules.common.action_associated_objects import AAOP_Tree
from gemsModules.common.transaction_data_translation import Transaction_Input_Translator
from gemsModules.common.servicer import Servicer
from gemsModules.common.transaction_data_translation import Transaction_Output_Translator

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Service_Manager():

    def __init__(self, transaction: Transaction):
        self.transaction : Transaction = transaction

    def process(self):
        self.manage_inputs()
        self.invoke_servicer()
        self.manage_outputs()
        return self.transaction

    def manage_inputs(self):
        self.input_translator = Transaction_Input_Translator(transaction = self.transaction)
        self.input_translator.translate()
        self.input_translator.fill_transaction_service_requests()
        self.incoming_tree : AAOP_Tree = self.input_translator.get_incoming_tree()

    def invoke_servicer(self):
        self.servicer = Servicer(self.incoming_tree)
        self.servicer.serve()
        self.outgoing_tree : AAOP_Tree = self.servicer.get_outgoing_tree()

    def manage_outputs(self):
        self.output_translator = Transaction_Output_Translator(
                transaction = self.transaction
                outgoing_tree = self.outgoing_tree)
        self.output_translator.build_transaction_outputs()
        self.transaction : Transaction = self.output_translator.get_transaction()

    def get_transaction(self):
        return self.transaction
