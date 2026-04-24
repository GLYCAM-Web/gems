import importlib
import logging
from typing import NamedTuple, Optional, Any

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class ModuleData(NamedTuple):
    from_this: str
    import_this: str

class ModuleLoader:
    def __init__(self, registry: dict[str, ModuleData]):
        """Initialize with a specific registry dictionary."""
        self._registry = registry

    def get_module_attr(self, choice: str) -> Any:
        """Retrieves the attribute from the module defined in the registry."""
        data: Optional[ModuleData] = self._registry.get(choice)
        
        if not data:
            raise ValueError(f"No module configuration found for choice: {choice}")
        
        try:
            module = importlib.import_module(data.from_this)
            # Returns the specific function/class (e.g., 'error_Multiples_Manager')
            return getattr(module, data.import_this)
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load '{data.import_this}' from '{data.from_this}': {e}")
            raise



