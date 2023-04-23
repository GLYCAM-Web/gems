from typing import Dict, Callable

from gemsModules.delegator.services.list_services.implied_translator import list_services_Implied_Translator 
from gemsModules.delegator.services.known_entities.implied_translator import known_entities_Implied_Translator 
from gemsModules.delegator.services.marco.implied_translator import marco_Implied_Translator 
from gemsModules.delegator.services.status.implied_translator import status_Implied_Translator

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

implied_modules : Dict[str, Callable] = {
    'KnownEntities': known_entities_Implied_Translator,
    'ListServices': list_services_Implied_Translator, 
    'Marco': marco_Implied_Translator, 
    'Status': status_Implied_Translator
    }
