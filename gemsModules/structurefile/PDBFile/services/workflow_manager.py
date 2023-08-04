import uuid
from gemsModules.common.main_api_resources import Resource
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.workflow_manager import Workflow_Manager
from gemsModules.common.code_utils import Annotated_List, resolve_dependency_list

from gemsModules.structurefile.PDBFile.services.AmberMDPrep.api import (
    AmberMDPrep_Request,
)
from gemsModules.structurefile.PDBFile.services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Inputs,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: To settings.service_dependencies?
Service_Dependencies = {
    "AmberMDPrep": Annotated_List(["ProjectManagement"], ordered=False)
}


class PDBFile_Workflow_Manager(Workflow_Manager):
    def get_linear_workflow_list(self) -> list[str]:
        return ["ProjectManagement", "AmberMDPrep"]

    def process(self, aaop_list):
        """This function takes a list of AAOPs and returns a list of AAOPs in the order they should be executed."""
        log.debug("\tthe service dependencies are: %s", Service_Dependencies)

        ordered = Annotated_List(ordered=True)
        unordered = aaop_list.copy()
        log.debug("\tthe unordered aaop request list is: %s", unordered)

        # Use AAO_type and Service_Dependencies  dict to determine order.
        while len(unordered) > 0:
            # Get the next aaop
            current_aaop = unordered.pop(0)

            # Add this aaops deps before this aaop, TODO: resolve/unify these_deps against prior deps
            these_deps = resolve_dependency_list(
                current_aaop.AAO_Type, Service_Dependencies
            )
            log.debug(
                "\tthe ordered dependencies for %s are: %s",
                current_aaop.AAO_Type,
                these_deps,
            )

            for new_dep in these_deps:
                new_aaop = None
                if new_dep == "ProjectManagement":
                    # TODO: We need AmberMDPrep inputs to be added to new_aaop in data_request_filler where we can get a project.
                    # However, then it's not as easy to get AmberMDPrep inputs for the ProjectManagement request.
                    if current_aaop.AAO_Type == "AmberMDPrep":
                        pass

                    new_aaop = AAOP(
                        AAO_Type="ProjectManagement",
                        The_AAO=ProjectManagement_Request(),
                        ID_String=uuid.uuid4(),
                        Dictionary_Name="ProjectManagement_Dep_Request",
                    )
                # Nothing depends on AmberMDPrep, but we'll include it's arm for now.
                elif new_dep == "AmberMDPrep":
                    new_aaop = AAOP(
                        AAO_Type="AmberMDPrep",
                        The_AAO=AmberMDPrep_Request(),
                        ID_String=uuid.uuid4(),
                        Dictionary_Name="AmberMDPrep_Dep_Request",
                    )

                if new_aaop:
                    log.debug(
                        "Adding dependency %s to aaop list before %s",
                        new_aaop,
                        current_aaop,
                    )

                    # Update the current AAOP's dependencies and set it as the requester AAOP.
                    #   TODO: this seems like a common pattern we could lift out
                    if current_aaop.Dependencies is None:
                        current_aaop.Dependencies = []
                    current_aaop.Dependencies.append(new_aaop.ID_String)
                    new_aaop.Requester = current_aaop.ID_String

                    # Append the new AAOP before the current AAOP.
                    ordered.append(new_aaop)

            # Add this aaop after we're finished with its deps
            ordered.append(current_aaop)

        # TODO: Prune dependency services that only need to be run once, regardless of requester.

        return ordered
