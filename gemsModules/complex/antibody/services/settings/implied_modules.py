from typing import Dict, Callable

from gemsModules.common.services.error.implied_translator import (
    error_Implied_Translator,
)
from gemsModules.common.services.marco.implied_translator import (
    marco_Implied_Translator,
)

from gemsModules.complex.antibody.services.Status.implied_translator import (
    Status_Implied_Translator,
)
from gemsModules.complex.antibody.services.list_services.implied_translator import (
    list_services_Implied_Translator,
)

from gemsModules.complex.antibody.services.ProjectManagement.implied_translator import (
    ProjectManagement_Implied_Translator,
)
from gemsModules.complex.antibody.services.Evaluate.implied_translator import (
    Evaluate_Implied_Translator,
)
from gemsModules.complex.antibody.services.Validate.implied_translator import (
    Validate_Implied_Translator,
)

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


implied_modules: Dict[str, Callable] = {
    "Error": error_Implied_Translator,
    "ListServices": list_services_Implied_Translator,
    "Marco": marco_Implied_Translator,
    "Status": Status_Implied_Translator,
    # Main services, currently ordered by the order they are called in the workflow.
    "Evaluate": Evaluate_Implied_Translator,
    "Validate": Validate_Implied_Translator,
    "ProjectManagement": ProjectManagement_Implied_Translator,  # The PM service is mostly implied by the other services.
}
