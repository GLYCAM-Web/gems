#!/usr/bin/env python3
from gemsModules.common.receiver import Receiver
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.main_api import Redirector_Transaction

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Redirector_Receiver(Receiver):
    
    def get_local_entity_type(self) -> str:
        return WhoIAm

    def get_transaction_child_type(self):
        return Redirector_Transaction


class Delegator_Receiver(Receiver):
    
    def get_local_entity_type(self) -> str:
        return WhoIAm

    def get_transaction_child_type(self):
        return Delegator_Transaction
