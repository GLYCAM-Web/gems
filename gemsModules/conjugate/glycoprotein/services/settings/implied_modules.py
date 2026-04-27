from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'Error': ModuleData('gemsModules.common.services.error.implied_translator', 'error_Implied_Translator'),
    'Marco': ModuleData('gemsModules.common.services.marco.implied_translator', 'marco_Implied_Translator'),
    'ListServices': ModuleData('gemsModules.conjugate.glycoprotein.services.list_services.implied_translator', 'list_services_Implied_Translator'),
    "ProjectManagement": ModuleData('gemsModules.conjugate.glycoprotein.services.ProjectManagement.implied_translator', 'ProjectManagement_Implied_Translator'),
    "Evaluate": ModuleData('gemsModules.conjugate.glycoprotein.services.Evaluate.implied_translator', 'Evaluate_Implied_Translator'),
    'Build': ModuleData('gemsModules.conjugate.glycoprotein.services.Build.implied_translator', 'Build_Implied_Translator'),
    'Status': ModuleData('gemsModules.conjugate.glycoprotein.services.Status.implied_translator', 'Status_Implied_Translator'),
}


module_loader = ModuleLoader(REGISTRY)



##### The following were in this file, and I'm not sure why. 
##### If this code works long enough that the person reading this is surprised, please remove them.
#    "ProjectManagement": serve_pm,
#    "Evaluate": serve_evaluate,
#    "Build": serve_Build,
#    "Status": serve_status,
#from gemsModules.common.services.error.server import Serve as serve_error
#from gemsModules.common.services.list_services.server import Serve as serve_list_services
#from gemsModules.common.services.marco.server import Serve as serve_marco
#
#from gemsModules.conjugate.glycoprotein.services.ProjectManagement.server import Serve as serve_pm
#from gemsModules.conjugate.glycoprotein.services.Build.server  import Serve as serve_Build
#from gemsModules.conjugate.glycoprotein.services.Evaluate.server import Serve as serve_evaluate
#from gemsModules.conjugate.glycoprotein.services.Status.server import Serve as serve_status
#
#from gemsModules.conjugate.glycoprotein.services.ProjectManagement.api import ProjectManagement_Request
#from gemsModules.conjugate.glycoprotein.services.Evaluate.api import EvaluateService_Request
#from gemsModules.conjugate.glycoprotein.services.Build.api import BuildService_Request
#from gemsModules.conjugate.glycoprotein.services.Status.api import StatusService_Request
