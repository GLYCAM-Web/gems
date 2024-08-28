#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from copy import deepcopy
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api import Transaction
from gemsModules.common.main_api_entity import Entity
from gemsModules.project.main_api import Project

from gemsModules.common.code_utils import find_aaop_by_id

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Request_Data_Filler(ABC):
    def __init__(
        self,
        aaop_list: List[AAOP],
        transaction: Transaction,
        response_project: Project = None,
    ):
        self.aaop_list = aaop_list
        self.transaction = transaction
        self.response_project = response_project

    @abstractmethod
    def process(self) -> List[AAOP]:
        pass

    def fill_resources_from_requester_if_exists(self, aaop, deep_copy=False):
        """ If this aaop has a requester, copy the resources from the requester to this aaop. """
        log.debug(f"About to fill resources from requester for {aaop=}")
        
        # TODO: optional filter by resourceRoles.
        if aaop.Requester is not None:
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester) 
            if requester_aaop is None:
                log.error(f"Requester AAOP not found for {aaop=}")
                return
            
            log.debug(f"resources: {requester_aaop.The_AAO.inputs.resources}")
            for resource in requester_aaop.The_AAO.inputs.resources:
                if deep_copy:
                    log.debug(f"Deep copying resource {resource=}")
                    aaop.The_AAO.inputs.resources.add_resource(deepcopy(resource))
                else:
                    aaop.The_AAO.inputs.resources.add_resource(resource)
        else:
            log.debug(f"No requester for {aaop=}")


class common_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> List[AAOP]:
        log.debug("common_Request_Data_Filler.process() called.")
        return self.aaop_list
