#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Callable

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.common.services.servicer import Servicer

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class GlycoProtein_Servicer(Servicer):

    def get_module_for_this_request(self, this_request_aaop: AAOP) -> Callable:
        from gemsModules.conjugate.glycoprotein.services.settings.service_modules import service_modules
        log.info("GlycoProtein_Servicer get_module_for_this_request is called.")
        log.debug(f"Getting module for current request: {this_request_aaop}")
        module = service_modules[this_request_aaop.AAO_Type]
        log.debug(f"Got module we will use to serve: {module} for {this_request_aaop.AAO_Type}")       
        return module
