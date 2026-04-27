from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "Error": ModuleData('gemsModules.common.services.error.implied_translator', 'error_Implied_Translator'),
    "Marco": ModuleData('gemsModules.common.services.marco.implied_translator', 'marco_Implied_Translator'),
    "ListServices": ModuleData('gemsModules.mmservice.mdaas.services.list_services.implied_translator', 'list_services_Implied_Translator'),
    "Status": ModuleData('gemsModules.common.services.status.implied_translator', 'status_Implied_Translator'),
    "Evaluate": ModuleData('gemsModules.mmservice.mdaas.services.Evaluate.implied_translator', 'Evaluate_Implied_Translator'),
    "RunMD": ModuleData('gemsModules.mmservice.mdaas.services.run_md.implied_translator', 'run_md_Implied_Translator'),
    "ProjectManagement": ModuleData('gemsModules.mmservice.mdaas.services.ProjectManagement.implied_translator', 'ProjectManagement_Implied_Translator'),
}


module_loader = ModuleLoader(REGISTRY)

