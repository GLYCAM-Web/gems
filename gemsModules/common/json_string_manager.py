#!/usr/bin/env python3
import traceback

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
        brief = None
        try:
            return_value = self.transaction.process_incoming_string(
                in_string=incoming_string, initialize_out=False
            )
            if return_value is None or return_value == 0:
                self.transaction_manager = self.transaction_manager_type(
                    self.transaction
                )
                self.transaction = self.transaction_manager.process()
                # Should this return a good response here?
                # return self.transaction.get_outgoing_string()
        except (ValueError, ValidationError, Exception) as e:
            # Could use use a NamedTuple here.
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
