from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'Error': ModuleData('gemsModules.common.services.error.manage_multiples', 'error_Multiples_Manager'),
    'Marco': ModuleData('gemsModules.common.services.marco.manage_multiples', 'marco_Multiples_Manager'),
    'ListServices': ModuleData('gemsModules.mmservice.mdaas.services.list_services.manage_multiples', 'list_services_Multiples_Manager'),
    'Status': ModuleData('gemsModules.common.services.status.manage_multiples', 'status_Multiples_Manager'),
    'Evaluate': ModuleData('gemsModules.mmservice.mdaas.services.Evaluate.manage_multiples', 'Evaluate_Multiples_Manager'),
    'RunMD': ModuleData('gemsModules.mmservice.mdaas.services.run_md.manage_multiples', 'run_md_Multiples_Manager'),
    }


module_loader = ModuleLoader(REGISTRY)

