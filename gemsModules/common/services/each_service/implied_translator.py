#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.implied_requests import Implied_Services_Inputs

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Implied_Translator(ABC):
    """ Inspect the Implied_Services_Inputs to figure out if this service needs to be run, and if so, how many times.
        Bundle resulting services into a service request package list (List[AAOP]).
    """

    def __init__(self):
        self.aaop_list : List[AAOP] = []

    @abstractmethod
    def process(self, input_object : Implied_Services_Inputs) -> List[AAOP]:
        return self.get_aaop_list()

    def get_aaop_list(self) -> List[AAOP]:
        return self.aaop_list

