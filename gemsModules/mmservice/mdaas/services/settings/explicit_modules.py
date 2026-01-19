from ..Evaluate.api import Evaluate_Request
from ..ProjectManagement.api import ProjectManagement_Request
from ..run_md.run_md_api import run_md_Request

explicit_modules = {
    "Evaluate": Evaluate_Request,
    "ProjectManagement": ProjectManagement_Request,
    "RunMD": run_md_Request,
}