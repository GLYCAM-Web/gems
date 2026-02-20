from typing import Dict, Callable

from gemsModules.common.services.error.implied_translator import error_Implied_Translator 
from gemsModules.common.services.marco.implied_translator import marco_Implied_Translator 

from gemsModules.conjugate.glycoprotein.services.list_services.implied_translator import list_services_Implied_Translator 
from gemsModules.conjugate.glycoprotein.services.Build.implied_translator import Build_Implied_Translator
from gemsModules.conjugate.glycoprotein.services.ProjectManagement.implied_translator import ProjectManagement_Implied_Translator
from gemsModules.conjugate.glycoprotein.services.Evaluate.implied_translator import Evaluate_Implied_Translator
from gemsModules.conjugate.glycoprotein.services.Status.implied_translator import Status_Implied_Translator

from gemsModules.conjugate.glycoprotein.services.ProjectManagement.api import ProjectManagement_Request
from gemsModules.conjugate.glycoprotein.services.Evaluate.api import EvaluateService_Request
from gemsModules.conjugate.glycoprotein.services.Build.api import BuildService_Request
from gemsModules.conjugate.glycoprotein.services.Status.api import StatusService_Request

from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import Serve as serve_list_services
from gemsModules.common.services.marco.server import Serve as serve_marco

from gemsModules.conjugate.glycoprotein.services.ProjectManagement.server import Serve as serve_pm
from gemsModules.conjugate.glycoprotein.services.Build.server  import Serve as serve_Build
from gemsModules.conjugate.glycoprotein.services.Evaluate.server import Serve as serve_evaluate
from gemsModules.conjugate.glycoprotein.services.Status.server import Serve as serve_status

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


implied_modules : Dict[str, Callable] = {
    'Error': error_Implied_Translator,
    'ListServices': list_services_Implied_Translator, 
    'Marco': marco_Implied_Translator, 
    "ProjectManagement": ProjectManagement_Implied_Translator,
    "Evaluate": Evaluate_Implied_Translator,
    'Build': Build_Implied_Translator,
    'Status': Status_Implied_Translator,
#    "ProjectManagement": serve_pm,
#    "Evaluate": serve_evaluate,
#    "Build": serve_Build,
#    "Status": serve_status,
}
