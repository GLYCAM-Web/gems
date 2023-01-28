from gemsModules.common.main_api import Transaction
from gemsModules.common.main_api_services import Services
from gemsModules.common.main_api_notices import Notices
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
        self.incoming_list : Services = self.input_translator.get_incoming_list()

    def invoke_servicer(self):
        self.servicer = Servicer(self.incoming_list)
        self.servicer.serve()
        self.transaction.outputs.entity.services : Services = self.servicer.get_services_request_list()
        self.transaction.outputs.entity.responses : Services = self.servicer.get_services_response_list()
        self.temp_notices : Notices = self.servicer.get_services_notices()
        self.transaction.outputs.entity.notices.append(self.temp_notices)

    def manage_outputs(self):
        self.output_translator = Transaction_Output_Translator(
            transaction : Transaction = self.transaction)
        self.output_translator.process()
        self.transaction : Transaction = self.output_translator.get_transaction()

    def get_transaction(self):
        return self.transaction
