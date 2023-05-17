#!/usr/bin/env python3
from pydantic import ValidationError
from abc import ABC, abstractmethod

from gemsModules.common import settings
from gemsModules.common.main_api import common_Transaction
from gemsModules.common.transaction_manager import Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class common_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        super().set_local_modules()

class Json_String_Manager(ABC):

    def __init__(self):
        self.get_local_components()

    @abstractmethod
    def get_local_components(self):
        self.transaction = common_Transaction()
        self.entityType = settings.WhoIAm
        self.transaction_manager_type = common_Transaction_Manager


    def process(self, incoming_string: str):
        try: 
            return_value=self.transaction.process_incoming_string(in_string=incoming_string, initialize_out=False)
        except ValidationError as e:
            self.transaction.generate_error_response(EntityType=self.entityType, Brief='InvalidInput', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string()
        except ValueError as e:
            self.transaction.generate_error_response(EntityType=self.entityType, Brief='EntityNotKnown', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string()
        except Exception as e:
            self.transaction.generate_error_response(EntityType=self.entityType, Brief='UnknownError', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string()
        if return_value is not None and return_value != 0:
            return self.transaction.get_outgoing_string()

        try:
            self.transaction_manager = self.transaction_manager_type(self.transaction)
            self.transaction = self.transaction_manager.process()
            return self.transaction.get_outgoing_string()
        except Exception as e:
            self.transaction.generate_error_response(EntityType=self.entityType, Brief='UnknownError', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string()

