#!/usr/bin/env python3
from gemsModules.common.entity import Entity
from .common_api import CommonAPI, Transaction
from .servicer import Servicer
from . import settings
from pydantic import ValidationError
from abc import ABC, abstractmethod

class Receiver(ABC):

    @abstractmethod
    def get_local_entity_type(self) -> str:
        return settings.WhoIAm

    @abstractmethod
    def get_transaction_child_type(self):
        return Transaction

    @abstractmethod
    def get_api_child_type(self):
        return CommonAPI

    @abstractmethod
    def get_entity_child_type(self):
        return Entity

    @abstractmethod
    def get_servicer_child_type(self):
        return Servicer

    def __init__(self, incoming_string: str):
        try: 
            self.transaction = self.get_transaction_child_type()
            self.transaction.process_incoming_string(incoming_string, initialize_out=False)
        except ValidationError as e:
            self.transaction.generate_error_response(Brief='InvalidInput', AdditionalInfo={'error': str(e)})
            return self.transaction.outgoing_string
        except Exception as e:
            self.transaction.generate_error_response(Brief='UnknownError', AdditionalInfo={'error': str(e)})
            return self.transaction.outgoing_string

    def receive(self) -> str:
        self.check_entity()
        self.hand_off_to_servicer()
        return self.transaction.outgoing_string

    def check_entity(self):   #  Override this function in delgator
        this_api : self.get_api_child_type = self.transaction.inputs
        this_entity : self.get_entity_child_type = this_api.entity
        if this_entity.entity_type != self.get_local_entity_type():
            self.transaction.generate_error_response(Brief='InvalidEntity', AdditionalInfo={'error': 'Entity type was not valid'})

    def hand_off_to_servicer(self):  #  Override this function in delgator
        servicer = self.get_servicer_child_type(self.transaction)
        servicer.delegate_services()
