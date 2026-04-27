from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'Error': ModuleData('gemsModules.common.services.error.manage_multiples', 'error_Multiples_Manager'),
    'Marco': ModuleData('gemsModules.common.services.marco.manage_multiples', 'marco_Multiples_Manager'),
    'ListServices': ModuleData('gemsModules.conjugate.glycoprotein.services.list_services.manage_multiples', 'list_services_Multiples_Manager'),
    'Evaluate': ModuleData('gemsModules.conjugate.glycoprotein.services.Evaluate.manage_multiples', 'Evaluate_Multiples_Manager'),
    'ProjectManagement': ModuleData('gemsModules.conjugate.glycoprotein.services.ProjectManagement.manage_multiples', 'ProjectManagement_Multiples_Manager'),
    'Build': ModuleData('gemsModules.conjugate.glycoprotein.services.Build.manage_multiples', 'Build_Multiples_Manager'),
    'Status': ModuleData('gemsModules.conjugate.glycoprotein.services.Status.manage_multiples', 'Status_Multiples_Manager'),
}


module_loader = ModuleLoader(REGISTRY)

