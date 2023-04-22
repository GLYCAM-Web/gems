#!/usr/bin/env python3
from typing import List
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Default_Service_Request_Manager(ABC):
    """ This should only happen if there are no services specified after the
        explicit and implicit services have been considered."""

    @abstractmethod
    def add_default_services(self) -> List[AAOP]:
        pass

    def get_aaop_list(self):
        return self.aaop_list

