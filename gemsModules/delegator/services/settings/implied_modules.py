from typing import Dict, Callable

from gemsModules.common.services.error.implied_translator import (
    error_Implied_Translator,
)
from gemsModules.common.services.marco.implied_translator import (
    marco_Implied_Translator,
)
from gemsModules.common.services.status.implied_translator import (
    status_Implied_Translator,
)

from gemsModules.delegator.services.known_entities.implied_translator import (
    known_entities_Implied_Translator,
)
from gemsModules.delegator.services.list_services.implied_translator import (
    list_services_Implied_Translator,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

implied_modules: Dict[str, Callable] = {
    "Error": error_Implied_Translator,
    "KnownEntities": known_entities_Implied_Translator,
    "listEntities": known_entities_Implied_Translator,  # json contract compatibility
    "ListEntities": known_entities_Implied_Translator,  # json contract compatibility
    "ListServices": list_services_Implied_Translator,
    "Marco": marco_Implied_Translator,
    "Status": status_Implied_Translator,
}
