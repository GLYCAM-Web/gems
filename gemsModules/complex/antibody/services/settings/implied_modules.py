from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "Error": ModuleData('gemsModules.common.services.error.implied_translator', 'error_Implied_Translator'),
    "ListServices": ModuleData('gemsModules.complex.antibody.services.list_services.implied_translator', 'list_services_Implied_Translator'),
    "Marco": ModuleData('Modules.common.services.marco.implied_translator', 'marco_Implied_Translator'),
    "Status": ModuleData('Modules.complex.antibody.services.Status.implied_translator', 'Status_Implied_Translator'),
    # Main services, currently ordered by the order they are called in the workflow.
    "ProjectManagement": ModuleData('Modules.complex.antibody.services.ProjectManagement.implied_translator', 'ProjectManagement_Implied_Translator'),
    # The PM service is mostly implied by the other services.
    "Analyze": ModuleData('Modules.complex.antibody.services.Analyze.implied_translator', 'Analyze_Implied_Translator'),
    "Build": ModuleData('Modules.complex.antibody.services.Build.implied_translator', 'Build_Implied_Translator'),
    "Evaluate": ModuleData('Modules.complex.antibody.services.Evaluate.implied_translator', 'Evaluate_Implied_Translator'),
}


module_loader = ModuleLoader(REGISTRY)

