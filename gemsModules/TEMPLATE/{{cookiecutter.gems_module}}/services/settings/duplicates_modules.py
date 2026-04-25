from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'Error': ModuleData('gemsModules.common.services.error.manage_multiples', 'error_Multiples_Manager'),
    'ListServices': ModuleData('gemsModules.{{cookiecutter.gems_module}}.services.list_services.manage_multiples', 'list_services_Multiples_Manager'),
    'Marco': ModuleData('gemsModules.common.services.marco.manage_multiples', 'marco_Multiples_Manager'),
    'Status': ModuleData('gemsModules.common.services.status.manage_multiples', 'status_Multiples_Manager'),
    '{{cookiecutter.service_name}}': ModuleData('gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}}.manage_multiples', '{{cookiecutter.service_name}}_Multiples_Manager'),
    }


module_loader = ModuleLoader(REGISTRY)

