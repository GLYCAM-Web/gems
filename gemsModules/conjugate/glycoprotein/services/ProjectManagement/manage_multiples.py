#!/usr/bin/env python3
from typing import List

from gemsModules.common.services.each_service.manage_multiples import Multiples_Manager
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class ProjectManagement_Multiples_Manager(Multiples_Manager):
    def process_multiples(self) -> List[AAOP]:
        log.info("process_multiples for the service ProjectManagement_Multiples_Manager in GlycoProtein is called")
        return self.process_multiples_action_First()
