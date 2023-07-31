from collections import namedtuple
from typing import List
from abc import ABC, abstractmethod

from gemsModules.common.services.orders_dependencies import Workflow_Manager
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


Service_Work_Flow_Order_template = namedtuple(
    "Service_Work_Flow_Order", "Service_Type Operations_Order_List"
)
Service_Work_Flows_template: List[Service_Work_Flow_Order_template] = []


class PDBFile_Workflow_Manager(Workflow_Manager):
    def get_linear_workflow_list(self) -> List[str]:
        return ["ProjectManagement", "AmberMDPrep"]
