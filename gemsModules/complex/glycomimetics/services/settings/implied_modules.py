from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "Error": ModuleData('gemsModules.common.services.error.implied_translator', 'error_Implied_Translator'),
    "ListServices": ModuleData('gemsModules.complex.glycomimetics.services.list_services.implied_translator', 'list_services_Implied_Translator'),
    "Marco": ModuleData('gemsModules.common.services.marco.implied_translator', 'marco_Implied_Translator'),
    "Status": ModuleData('gemsModules.complex.glycomimetics.services.Status.implied_translator', 'Status_Implied_Translator'),
    # Main services, currently ordered by the order they are called in the workflow.
    "Evaluate": ModuleData('gemsModules.complex.glycomimetics.services.Evaluate.implied_translator', 'Evaluate_Implied_Translator'),
    "Validate": ModuleData('gemsModules.complex.glycomimetics.services.Validate.implied_translator', 'Validate_Implied_Translator'),
    # The PM service is mostly implied by the other services.
    "ProjectManagement": ModuleData('gemsModules.complex.glycomimetics.services.ProjectManagement.implied_translator', 'ProjectManagement_Implied_Translator'),
    "Build_Selected_Positions": ModuleData('gemsModules.complex.glycomimetics.services.Build_Selected_Positions.implied_translator', 'Build_Implied_Translator'),
    "Analyze": ModuleData('gemsModules.complex.glycomimetics.services.Analyze.implied_translator', 'Analyze_Implied_Translator'),
}

module_loader = ModuleLoader(REGISTRY)

