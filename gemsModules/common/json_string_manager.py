#!/usr/bin/env python3
import traceback

from pydantic import ValidationError
from abc import ABC, abstractmethod

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.main_api import common_Transaction
from gemsModules.common.settings import WhoIAm

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
        self.entityType = WhoIAm
        self.transaction_manager_type = common_Transaction_Manager
        self.initialize_out = True

    def process(self, incoming_string: str):
        log.info("process for Common's Json_String_Manager is called")
        brief = None
        try:
            return_value = self.transaction.process_incoming_string(
                in_string=incoming_string, initialize_out=self.initialize_out
            )
            if return_value is None or return_value == 0:
                self.transaction_manager = self.transaction_manager_type(
                    self.transaction
                )
                self.transaction = self.transaction_manager.process()
        except (ValueError, ValidationError, Exception) as e:
            if isinstance(e, ValueError):
                brief = "InvalidInput", e
            elif isinstance(e, ValidationError):
                brief = "ValidationError", e
            else:
                brief = "UnknownError", e
            log.error("Exception in Json_String_Manager: %s", traceback.format_exc())
        finally:
            if brief is not None:
                self.transaction.generate_error_response(
                    EntityType=self.entityType,
                    Brief=brief[0],
                    AdditionalInfo={"error": str(brief[1])},
                )
                return self.transaction.get_outgoing_string()
