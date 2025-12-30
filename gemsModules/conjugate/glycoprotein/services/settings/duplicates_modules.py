from typing import Dict, Callable

from gemsModules.common.services.error.manage_multiples import error_Multiples_Manager 
from gemsModules.common.services.marco.manage_multiples import marco_Multiples_Manager 

from gemsModules.conjugate.glycoprotein.services.list_services.manage_multiples import list_services_Multiples_Manager
from gemsModules.conjugate.glycoprotein.services.ProjectManagement.manage_multiples import ProjectManagement_Multiples_Manager
from gemsModules.conjugate.glycoprotein.services.Build.manage_multiples import Build_Multiples_Manager 
from gemsModules.conjugate.glycoprotein.services.Evaluate.manage_multiples import Evaluate_Multiples_Manager
from gemsModules.conjugate.glycoprotein.services.Status.manage_multiples import Status_Multiples_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

duplicates_modules : Dict[str, Callable] = {
    'Error': error_Multiples_Manager, 
    'ListServices': list_services_Multiples_Manager, 
    'Marco': marco_Multiples_Manager, 
    'Evaluate': Evaluate_Multiples_Manager,
    'ProjectManagement': ProjectManagement_Multiples_Manager,
    'Build': Build_Multiples_Manager,
    'Status': Status_Multiples_Manager,
}
