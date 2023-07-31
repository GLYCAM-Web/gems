from collections import namedtuple
from typing import List, Literal

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.code_utils import Annotated_List, resolve_dependency_list
from gemsModules.common.services.workflow_manager import Workflow_Manager

from gemsModules.structurefile.PDBFile.services.AmberMDPrep.api import AmberMDPrep_AAOP
from gemsModules.structurefile.PDBFile.services.ProjectManagement.api import (
    ProjectManagement_AAOP,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


Service_Dependencies = {
    "AmberMDPrep": Annotated_List(["ProjectManagement"], ordered=False)
}


Service_Work_Flow_Order_template = namedtuple(
    "Service_Work_Flow_Order", "Service_Type Operations_Order_List"
)
Service_Work_Flows_template: List[Service_Work_Flow_Order_template] = []


class PDBFile_Workflow_Manager(Workflow_Manager):
    def get_linear_workflow_list(self) -> List[str]:
        return ["ProjectManagement", "AmberMDPrep"]

    def process(self, aaop_list):
        log.debug("\tthe service dependencies are: %s", Service_Dependencies)

        ordered = Annotated_List(ordered=True)
        unordered = aaop_list.copy()
        log.debug("\tthe unordered aaop request list is: %s", unordered)

        # Use AAO_type and service_deps dict to determine order.
        while len(unordered) > 0:
            # Get the next aaop
            current_aaop = unordered.pop(0)

            # Add this aaops deps before this aaop
            these_deps = resolve_dependency_list(
                current_aaop.AAO_Type, Service_Dependencies
            )
            log.debug(
                "\tthe ordered dependencies for %s are: %s",
                current_aaop.AAO_Type,
                these_deps,
            )

            for new_dep in these_deps:
                log.debug(
                    "Adding dependency %s to aaop list before %s",
                    new_dep,
                    current_aaop.AAO_Type,
                )
                if new_dep == "ProjectManagement":
                    ordered.append(ProjectManagement_AAOP())
                # Nothing depends on AmberMDPrep atm.
                elif new_dep == "AmberMDPrep":
                    ordered.append(AmberMDPrep_AAOP())

            # Add this aaop after its deps
            ordered.append(current_aaop)

        # TODO: Prune dependency services that only need to be run once, regardless of requester.
        return ordered
