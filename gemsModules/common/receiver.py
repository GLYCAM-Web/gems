#!/usr/bin/env python3
from pydantic import ValidationError
from abc import ABC, abstractmethod

from gemsModules.common.main_api import Transaction
from gemsModules.common import settings_main

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Receiver(ABC):

    @abstractmethod
    def get_local_entity_type(self) -> str:
        return settings_main.WhoIAm

    @abstractmethod
    def get_transaction_child_type(self):
        return Transaction

    def receive(self, incoming_string: str):
        try: 
            self.transaction = self.get_transaction_child_type()
            self.entityType=self.get_local_entity_type()
            return_value=self.transaction.process_incoming_string(self.transaction, in_string=incoming_string, initialize_out=False)
        except ValueError as e:
            self.transaction.generate_error_response(self.transaction, EntityType=self.entityType, Brief='EntityNotKnown', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string(self.transaction)
        except ValidationError as e:
            self.transaction.generate_error_response(self.transaction, EntityType=self.entityType, Brief='InvalidInput', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string(self.transaction)
        except Exception as e:
            self.transaction.generate_error_response(self.transaction, EntityType=self.entityType, Brief='UnknownError', AdditionalInfo={'error': str(e)})
            return self.transaction.get_outgoing_string(self.transaction)
        if return_value is not None and return_value != 0:
            return self.transaction.get_outgoing_string(self.transaction)


    def get_incoming_entity_type(self):
        return self.transaction.inputs.entity.entityType

    def get_incoming_services_types(self):
        pass

    def get_transaction(self):
        return self.transaction
