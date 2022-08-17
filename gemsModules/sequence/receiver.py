#!/usr/bin/env python3
from . import settings
from .entity_api import SequenceAPI, SequenceTransaction
from .servicer import Sequence_Servicer
from gemsModules.common.receiver import Receiver as CommonReceiver
from pydantic import ValidationError

class Receiver(CommonReceiver):

    entity_type : str = settings.WhoIAm

    def get_transaction_child_type(self):
        return SequenceTransaction

    def get_transaction_child_type(self):
        return SequenceTransaction

    def get_api_child_type(self):
        return SequenceAPI

    def get_entity_child_type(self):
        return 

    def get_servicer_child_type(self):
        return Sequence_Servicer


def __main__(in_string : str) -> str:
    receiver = Receiver(in_string)
    return receiver.receive()