from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "Error": ModuleData('gemsModules.common.services.error.manage_multiples', 'error_Multiples_Manager'),
    "ListServices": ModuleData('gemsModules.complex.glycomimetics.services.list_services.manage_multiples', 'list_services_Multiples_Manager'),
    "Marco": ModuleData('gemsModules.common.services.marco.manage_multiples', 'marco_Multiples_Manager'),
    "Status": ModuleData('gemsModules.complex.glycomimetics.services.Status.manage_multiples', 'Status_Multiples_Manager'),
    "Build_Selected_Positions": ModuleData('gemsModules.complex.glycomimetics.services.Build_Selected_Positions.manage_multiples', 'Build_Multiples_Manager'),
}


module_loader = ModuleLoader(REGISTRY)

