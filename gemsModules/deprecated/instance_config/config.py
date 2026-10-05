import json

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Union

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class ConfigManager(ABC):
    """ConfigManager manages a 'config' dict and associated json file at a particular GEMS path.

    This class is a singleton, so it can be instantiated once and then used throughout the
    lifetime of a request. One feature of this is that the instance configuration cannot be changed
    out from under the feet of a request because the real configuration file is read only once.

    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton pattern
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(
        self,
        config: Dict = None,
        config_path: Union[Path, str] = None,
        reinitialize: bool = False,
        **kwargs
    ):
        # Singleton pattern - only initialize once, overridable.
        if not reinitialize and self.__initialized:
            return
        self.__initialized = True

        self._config = None
        if config is not None:
            self.set_config_data(config)
        elif config_path is not None:
            self.set_active_config(config_path)
        else:
            self.set_active_config(self.get_default_path())

    @property
    def config(self):
        return self._config

    @property
    def is_configured(self) -> bool:
        """Returns True if the $GEMSHOME/instance_config.json exists and is valid."""
        return self.get_default_path().exists()

    def set_active_config(self, config_path: Path):
        if config_path is None:
            config_path = self.get_default_path()

        if not config_path.exists():
            config_path = self.get_default_path(template=True)

        self._config = self.load(config_path=config_path)

    def set_config_data(self, config: Dict):
        if isinstance(config, dict) and isinstance(config.get("hosts"), list):
            hosts_dict = {}
            for i, h in enumerate(config["hosts"]):
                if isinstance(h, dict):
                    name = h.get("name") or h.get("host") or str(i)
                    h_copy = h.copy()
                    if "host" not in h_copy and "address" in h_copy:
                        h_copy["host"] = h_copy["address"]
                    if "contexts" not in h_copy and "entities_available" in h_copy:
                        h_copy["contexts"] = [e.value if hasattr(e, "value") else str(e) for e in h_copy["entities_available"]]
                    hosts_dict[name] = h_copy
            config = config.copy()
            config["hosts"] = hosts_dict
        self._config = config

    @abstractmethod
    def get_default_path(template=False) -> Path:
        """Must be overridden to return the default path for the instance config file."""
        raise NotImplementedError("Must be overridden to return the default path.")

    @classmethod
    def from_dict(cls, config_dict):
        return cls(config=config_dict)

    @staticmethod
    def load(config_path) -> Dict:
        """Load a json instance config file."""
        with open(config_path, "r") as f:
            instance_config = json.load(f)

        if isinstance(instance_config, dict) and isinstance(instance_config.get("hosts"), list):
            hosts_dict = {}
            for i, h in enumerate(instance_config["hosts"]):
                if isinstance(h, dict):
                    name = h.get("name") or h.get("host") or str(i)
                    h_copy = h.copy()
                    if "host" not in h_copy and "address" in h_copy:
                        h_copy["host"] = h_copy["address"]
                    if "contexts" not in h_copy and "entities_available" in h_copy:
                        h_copy["contexts"] = [e.value if hasattr(e, "value") else str(e) for e in h_copy["entities_available"]]
                    hosts_dict[name] = h_copy
            instance_config["hosts"] = hosts_dict

        return instance_config

    def save(self, config_path):
        """Save a json instance config file."""
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
