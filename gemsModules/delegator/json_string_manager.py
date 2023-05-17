#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.main_api import Redirector_Transaction
from gemsModules.delegator.transaction_manager import delegator_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Redirector_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = Redirector_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = None

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

    def get_incoming_entity_type(self):
        return self.transaction.inputs.entity.entityType

class Delegator_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = Delegator_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = delegator_Transaction_Manager
