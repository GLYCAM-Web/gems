#!/usr/bin/env python3
from pydantic import ValidationError
from abc import ABC, abstractmethod

from gemsModules.common import settings_main
from gemsModules.common.main_api import Transaction
from gemsModules.common.transaction_manager import Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Receiver(ABC):

    @abstractmethod
    def get_local_entity_type(self) -> str:
        return settings_main.WhoIAm

    @abstractmethod
    def get_transaction_child_type(self):
        return Transaction

    def __init__(self):
        self.transaction = self.get_transaction_child_type()()
        self.entityType=self.get_local_entity_type()

    def receive(self, incoming_string: str):
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

        transaction_manager = Transaction_Manager(self.transaction)
        try:
            self.transaction = transaction_manager.process()
            return self.transaction.get_outgoing_string()
        except Exception as e:
            self.transaction.generate_error_response(EntityType=self.entityType, Brief='UnknownError', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string()

