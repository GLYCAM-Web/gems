import datetime
import json, os, glob, shutil, socket
from pathlib import Path
from typing import Dict, List, Optional, Union
from abc import ABC, abstractmethod

from gemsModules.systemoperations.instance_config.versions import DateReversioner
from gemsModules.systemoperations.environment_ops import (
    is_GEMS_test_workflow,
    is_GEMS_live_swarm,
)

from gemsModules.logging.logger import Set_Up_Logging

from . import *


log = Set_Up_Logging(__name__)


class FileSystemPathsMixin:
    """A mixin for the InstanceConfig class to handle filesystem paths.

    - Honestly should have a generic filesystems_paths dict in the instance config..This just avoids breaking people's DevEnv. TODO: Fix this.

    This functionality mostly lives in gemsModules/project. Arguably, instance config should be part of that. (BLF 2026-01-22)
    """

    def get_filesystem_path(self, app) -> str:
        """Returns the filesystem path for the given name defined in the instance config's filesystem_paths dict.
        """

        if app in self.config["filesystem_paths"]:
            return self.config["filesystem_paths"][app]
        else:
            # This used to log and raise an error (commented out), but it should not.
            # The project module contains safeguards against bad paths being in the instance config.
            # The project module also has functionality for setting paths internally. And, paths can 
            #     be set in the JSON objects, etc.
            log.debug(
                f"Filesystem path not set for {app} in instance_config.json. If problems occur later, this might be why."
            )
            return None
#            log.error(
#                f"Access attempted but {app} filesystem path not set in instance_config.json."
#            )
#            raise KeyError(
#                f"{app} not found in instance_config.json, available: {self.config['filesystem_paths']}"
#            )

    def set_filesystem_path(self, app: str, path: str):
        """Sets the filesystem path for the given app in the instance config's filesystem_paths dict."""
        if "filesystem_paths" not in self.config:
            self.config["filesystem_paths"] = {}
        elif app in self.config["filesystem_paths"]:
            log.warning(
                f"Overwriting existing filesystem path for {app} in instance_config.json. Old path: {self.config['filesystem_paths'][app]}"
            )
            
        self.config["filesystem_paths"][app] = path


class UploadsPathsMixin:
    """A mixin for the InstanceConfig class to handle uploads paths.
    This is brazen copy-pasta for the object above. All of the instance config functionality should probably move to the project module and 
    should definitely be recast using Pydantic. (BLF 2026-01-22)
    """

    def get_uploads_path(self, app) -> str:
        """Returns the uploads path for the given app defined in the instance config's filesystem_paths dict.
        """

        if app in self.config["filesystem_paths"]:
            return self.config["filesystem_paths"][app]
        else:
            log.debug(
                f"Uploads path not set for {app} in instance_config.json. If problems occur later, this might be why."
            )
            return None


class InstanceConfig(KeyedArgManager, FileSystemPathsMixin, UploadsPathsMixin):
    """The main GEMS class for parsing it's active instance configuration file.

    This class only has active GEMS instance specific methods and configuration.
    It inherits all it's configuration functionality.

    A class for parsing and using the instance_config.yml of the active GEMS installation.

    This class is deeply coupled with the active state of your GEMS environment.
    It has properties and methods which convey active environmental information.

    >>> instance_config = InstanceConfig()
    >>> instance_config.get_available_contexts('gw-grpc-delegator')
    """

    # Not an enum so we can extend here, in the InstanceConfig class, where the most specific GEMS instance configuration is defined.
    Contexts = ["DevEnv", "Swarm"]

    def __init__(
        self,
        config: Dict = None,
        config_path: Union[Path, str] = None,
        reinitialize: bool = False,
        **kwargs,
    ):
        super().__init__(config, config_path, reinitialize, **kwargs)
        if len(self.config) and "date" not in self.config:
            self.set_active_config(self.get_default_path(template=True))

        # compare the active config to the example config
        self.reversioner = DateReversioner(
            self.get_default_path(), self.get_default_path(template=True)
        )

        if self.reversioner.is_outdated:
            log.warning("Detected old configuration template, if you have any issues, try regenerating your instance config.")
            
        log.debug(f"Active config: {self.config}")

    def save(self, force_update=False) -> bool:
        """save the instance config using a DateReversioner."""
        self.reversioner.set_new_config_data(self.config)
        return self.reversioner.update(force_update=force_update)

    @staticmethod
    def get_default_path(template=False) -> Path:
        """The default path is the active GEMS instance configuration.

        TODO: change to active_path property.
        """
        name = "instance_config"
        if template:
            name += ".template"
        name += ".json"

        return Path(os.getenv("GEMSHOME", "")) / name

    # TODO: Context needs an enum.
    # TODO: Now that there are two competing uses of 'context' in the codebase, it doesn't just need an enum.
    #       It needs a disambiguating name. Search for getGemsExecutionContext to find other uses.
    #       The two uses are similar, but probably both can happen at once. (BLF 2026-01-22)
    def get_keyed_arguments(
        self,
        key: KeyedArgManager.ConfigurationKeys,
        host: str = None,
        context: Optional[str] = None,
    ):
        if context not in self.Contexts:
            log.warning(f"Context {context} not found in {self.Contexts}.")

        if context is None:
            # TODO: Is this sensible? We also need to generalize it to a systemoperation or combine with one already in use.
            # I think that the DevEnv and the website should be expected to always declare themselves fully. If they have 
            # not done so, I think execution should stop. 
            # But, I will leave the current logic in place and only add an option for STANDALONE
            # In a standalone user environment, we should grant some leeway. (BLF 2026-01-22)
            if is_GEMS_test_workflow():
                context = self.Contexts.DEV_ENV
            elif host is not None and self.Context.SWARM in self.get_available_contexts(
                host
            ):
                context = self.Contexts.SWARM
            else:  
                context = self.Contexts.STANDALONE

        return super().get_keyed_arguments(key, host, context)
