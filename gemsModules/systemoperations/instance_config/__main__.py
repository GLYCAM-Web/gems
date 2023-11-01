import datetime
import json, os, glob, shutil, socket
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal
from abc import ABC, abstractmethod

from gemsModules.systemoperations.environment_ops import (
    is_GEMS_test_workflow,
    is_GEMS_live_swarm,
)

from gemsModules.logging.logger import Set_Up_Logging

from . import *


log = Set_Up_Logging(__name__)


# GEMS note: We should not modify production configuration files automatically. It should only run in a DevEnv.
class DateReversioner:
    """A class to version a json file based on a timestamp."""

    def __init__(self, active_config: Path, example_config: Path):
        self.file_to_version = active_config
        self.example = example_config

    def update(self):
        """Update the file_to_version with the current date."""

        needs_update = False
        if self.file_to_version.exists():
            # could generilize
            j_data = json.load(open(self.file_to_version))
            tj_data = json.load(open(self.example))
            if "date" not in j_data:
                # if no date is found, lets update to a versioned file
                needs_update = True
            else:
                # check the template file for a date
                # if the template is newer, lets update to a versioned file
                if "date" in tj_data:
                    if j_data["date"] < tj_data["date"]:
                        needs_update = True
                else:
                    raise RuntimeError(
                        "Template file does not have a date, cannot update."
                    )

        if needs_update:
            # Backup the file_to_version.
            backup_file = self.file_to_version.with_suffix(
                f".{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            )
            shutil.copyfile(self.file_to_version, backup_file)

            # copy the example file in place of the file_to_version
            shutil.copyfile(self.example, self.file_to_version)
            log.info(f"Updated {self.file_to_version} with new date.")


class InstanceConfig(KeyedArgManager):
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
    Contexts = ContextManager.Contexts + ["MDaaS-RunMD"]

    @staticmethod
    def get_default_path(example=False) -> Path:
        """The default path is the active GEMS instance configuration.

        TODO: change to active_path property.
        """
        name = "instance_config.json"
        if example:
            name += ".example"

        return Path(os.getenv("GEMSHOME", "")) / name

    # TODO: Context needs an enum.
    def get_keyed_arguments(
        self,
        key: KeyedArgManager.ConfigurationKeys,
        host: str = None,
        context: Contexts = None,
    ):
        if context not in self.Contexts:
            log.warning(f"Context {context} not found in {self.Contexts}.")

        if context is None:
            # TODO: Is this sensible? We also need to generalize it to a systemoperation or combine with one already in use.
            if is_GEMS_test_workflow():
                context = self.Contexts.DEV_ENV
            elif host is not None and self.Context.SWARM in self.get_available_contexts(
                host
            ):
                context = self.Contexts.SWARM

        return super().get_keyed_arguments(key, host, context)

    # Special Context Helpers for GEMS defined here.
    # "MDaaS-RunMD" context - MD Cluster host helpers
    def get_md_filesystem_path(self) -> str:
        """Returns the filesystem path for the MD compute cluster by hostname defined in the instance config's hosts dict."""
        if (
            "md_cluster_filesystem_path" not in self.config
            or len(self.config["md_cluster_filesystem_path"]) == 0
        ):
            log.error(
                "Access attempted but MD Cluster filesystem path not set in instance_config.json."
            )

        return self.config["md_cluster_filesystem_path"]

    def set_md_filesystem_path(self, path):
        """Sets the filesystem path for the MD compute cluster by hostname defined in the instance config's hosts dict.

        You probably want to save the instance config after this.
        """
        self.config["md_cluster_filesystem_path"] = path
