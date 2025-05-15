from ..ProjectManagement.api import ProjectManagement_Request
from ..Build.api import BuildService_Request

explicit_modules = {
    "ProjectManagement": ProjectManagement_Request,
    "Build": BuildService_Request,
}