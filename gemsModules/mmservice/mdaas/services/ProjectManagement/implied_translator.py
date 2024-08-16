#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP


from gemsModules.common.services.each_service.implied_translator import (
    Implied_Translator,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class ProjectManagement_Implied_Translator(Implied_Translator):
    """Inspect the Implied_Services_Inputs to figure out if this service needs to be run, and if so, how many times.
    Bundle resulting services into a service request package list (List[AAOP]).
    """

    def process(self, input_object) -> List[AAOP]:
        log.debug("In ProjectManagement_Implied_Translator.process, input_object is type: %s", type(input_object))
        self.aaop_list = []
        return self.get_aaop_list()
