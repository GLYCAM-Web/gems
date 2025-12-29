from ..ProjectManagement.api import ProjectManagement_Request

from ..Evaluate.api import EvaluateService_Request
from ..Build.api import BuildService_Request
from ..Status.api import StatusService_Request

explicit_modules = {
    "ProjectManagement": ProjectManagement_Request,
    "Evaluate": EvaluateService_Request,
    "Build": BuildService_Request,
    "Status": StatusService_Request,
}