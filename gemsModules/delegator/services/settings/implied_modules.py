from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "Error": ModuleData('gemsModules.common.services.error.implied_translator', 'error_Implied_Translator'),
    "KnownEntities": ModuleData('gemsModules.delegator.services.known_entities.implied_translator', 'known_entities_Implied_Translator'),
    "listEntities": ModuleData('gemsModules.delegator.services.known_entities.implied_translator', 'known_entities_Implied_Translator'),
    # json contract compatibility
    "ListEntities": ModuleData('gemsModules.delegator.services.known_entities.implied_translator', 'known_entities_Implied_Translator'),
    # json contract compatibility
    "ListServices": ModuleData('gemsModules.delegator.services.list_services.implied_translator', 'list_services_Implied_Translator'),
    "Marco": ModuleData('gemsModules.common.services.marco.implied_translator', 'marco_Implied_Translator'),
    "Status": ModuleData('gemsModules.common.services.status.implied_translator', 'status_Implied_Translator'),
}

module_loader = ModuleLoader(REGISTRY)

