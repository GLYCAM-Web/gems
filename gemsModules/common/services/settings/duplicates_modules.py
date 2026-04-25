from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'KnownEntities': ModuleData('gemsModules.delegator.services.known_entities.manage_multiples', 'known_entities_Multiples_Manager'),
    'ListServices': ModuleData('gemsModules.delegator.services.list_services.manage_multiples', 'list_services_Multiples_Manager '),
    'Marco': ModuleData('gemsModules.delegator.services.marco.manage_multiples', 'marco_Multiples_Manager'),
    'Status': ModuleData('gemsModules.delegator.services.status.manage_multiples', 'status_Multiples_Manager'),
    }


module_loader = ModuleLoader(REGISTRY)

