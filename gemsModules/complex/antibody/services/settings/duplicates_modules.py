from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "Error": ModuleData('gemsModules.common.services.error.manage_multiples', 'error_Multiples_Manager'),
    "ListServices": ModuleData('gemsModules.complex.antibody.services.list_services.manage_multiples', 'list_services_Multiples_Manager'),
    "Marco": ModuleData('gemsModules.common.services.marco.manage_multiples', 'marco_Multiples_Manager'),
    "Status": ModuleData('gemsModules.complex.antibody.services.Status.manage_multiples', 'Status_Multiples_Manager'),
}


module_loader = ModuleLoader(REGISTRY)



#def get_the_module(choice):
#    module_path, module_attr = DUPLICATES_MODULE_REGISTRY.get(choice)
#    if not module_path or not module_attr:
#        raise ValueError(f"No module found for choice: {choice}")
#
#    try:
#        module = importlib.import_module(module_path)
#        # Extract the 'receive' function from the loaded module and return that
#        return getattr(module, module_attr)
#    except ImportError as e:
#        log.error(f"Failed to load {module_attr} for {choice} at {module_path}: {e}")
#        raise


# Gemini said this:
#from registry_utils import ModuleData, ModuleLoader
#
## 1. Define your specific data
#DUPLICATES_REGISTRY = {
#    "Error": ModuleData('gemsModules.common.services.error.manage_multiples', 'error_Multiples_Manager'),
#    "Marco": ModuleData('gemsModules.common.services.marco.manage_multiples', 'marco_Multiples_Manager'),
#}
#
## 2. Create an instance of the loader for this registry
#duplicates_manager = ModuleLoader(DUPLICATES_REGISTRY)
#
## 3. Use it anywhere in this file
#try:
#    manager_func = duplicates_manager.get_module_attr("Error")
#    manager_func() # Executes the retrieved function
#except ValueError as e:
#    print(e)

