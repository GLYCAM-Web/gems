import uuid
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.workflow_manager import Workflow_Manager
from gemsModules.common.code_utils import Annotated_List, resolve_dependency_list
from gemsModules.logging.logger import Set_Up_Logging

from .Build_Selected_Positions.api import Build_Request
from .ProjectManagement.api import ProjectManagement_Request
from .Evaluate.api import Evaluate_Request
from .Validate.api import Validate_Request
from .Analyze.api import Analyze_Request

# from .known_available import Module_Available_Services # for maybe keying...


log = Set_Up_Logging(__name__)


# TODO: To services.settings... ?
# Service_Dependencies = {
#     "Analyze": Annotated_List(
#         ["Evaluate", "Validate", "ProjectManagement", "Build_Selected_Positions"], ordered=True
#     ),
#     "Build_Selected_Positions": Annotated_List(
#         ["Evaluate", "Validate", "ProjectManagement"], ordered=True
#     ),
#     "ProjectManagement": Annotated_List(["Evaluate", "Validate"], ordered=True),
#     "Evaluate": Annotated_List([], ordered=True),
#     "Validate": Annotated_List(["Evaluate"], ordered=True),
# }

EVALUATE_DEPENDENCIES = Annotated_List([], ordered=True)
VALIDATE_DEPENDENCIES = Annotated_List(["Evaluate"], ordered=True)
PROJECTMANAGEMENT_DEPENDENCIES = Annotated_List(
    VALIDATE_DEPENDENCIES + ["Validate"], ordered=True
)
BUILD_DEPENDENCIES = Annotated_List(
    PROJECTMANAGEMENT_DEPENDENCIES + ["ProjectManagement"], ordered=True
)
ANALYZE_DEPENDENCIES = Annotated_List(
    BUILD_DEPENDENCIES + ["Build_Selected_Positions"], ordered=True
)

Service_Dependencies = {
    "Analyze": ANALYZE_DEPENDENCIES,
    "Build_Selected_Positions": BUILD_DEPENDENCIES,
    "ProjectManagement": PROJECTMANAGEMENT_DEPENDENCIES,
    "Evaluate": EVALUATE_DEPENDENCIES,
    "Validate": VALIDATE_DEPENDENCIES,
}


# TODO: work_flows style or workflow_manager style?
class Glycomimetics_Workflow_Manager(Workflow_Manager):
    def get_linear_workflow_list(self) -> list[str]:
        return [
            "Evaluate",
            "Validate",
            "ProjectManagement",
            "Build_Selected_Positions",
            "Analyze",
        ]

    def process(self, aaop_list):
        """This function takes a list of AAOPs and returns a list of AAOPs in the order they should be executed."""
        log.debug("\tthe service dependencies are: %s", Service_Dependencies)

        ordered = Annotated_List(ordered=True)
        unordered = aaop_list.copy()
        log.debug("\tthe unordered aaop request list is: %s", unordered)

        # Use AAO_type and Service_Dependencies dict to determine AAOP execution order.
        while len(unordered) > 0:
            # Get the next aaop
            current_aaop = unordered.pop(0)

            # TODO: resolve/unify these_deps against prior deps
            these_deps = resolve_dependency_list(
                current_aaop.AAO_Type, Service_Dependencies
            )
            log.debug(
                "\tthe ordered dependencies for %s are: %s",
                current_aaop.AAO_Type,
                these_deps,
            )

            # TODO: the dep resolution could be more general (really a lot of this workflow manager)
            for new_dep in these_deps:
                # resolve the cls from the dependency string
                aao_cls = globals()[f"{new_dep}_Request"]
                new_aaop = AAOP(
                    AAO_Type=new_dep,
                    The_AAO=aao_cls(),
                    ID_String=uuid.uuid4(),
                    Dictionary_Name=f"{new_dep}_Dep_Request",
                )

                log.debug(
                    "Adding dependency %s to aaop list before %s",
                    new_aaop,
                    current_aaop,
                )

                new_aaop.set_requester(current_aaop)
                ordered.append(new_aaop)

            # Add this aaop after we're finished with its deps
            ordered.append(current_aaop)

        # TODO: Prune dependency services that only need to be run once, regardless of requester.
        return ordered
