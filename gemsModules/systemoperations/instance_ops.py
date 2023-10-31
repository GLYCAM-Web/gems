import json, os, glob, shutil, socket
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal
from enum import Enum
from abc import ABC, abstractmethod

from gemsModules.systemoperations.environment_ops import (
    is_GEMS_test_workflow,
    is_GEMS_live_swarm,
)

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class InstanceConfigError(Exception):
    pass


class InstanceConfigNotFoundError(FileNotFoundError):
    """Raised when the $GEMSHOME/instance_config.json file is not found.

    This file is required for GEMS to route requests appropriately. Please copy the example file
    from $GEMSHOME/instance_config.json.example.

    """

    def __init__(self, msg=None, *args, **kwargs):
        if msg is None:
            msg = (
                "Warning! Did you configure your GEMS instance?\n"
                "\tThe GEMS instance_config.json was not found in $GEMSHOME.\n\n"
                "\tPlease copy the example file:\n"
                "\t\t`cp $GEMSHOME/instance_config.json.example $GEMSHOME/instance_config.json`\n\n"
                "\tOtherwise, some GEMS requests may not function as expected.\n"
                f"\t$GEMSHOME is {os.getenv('GEMSHOME', '$GEMSHOME')}."
            )

        log.error(msg)

        super().__init__(msg, *args, **kwargs)


class SbatchArguments(BaseModel):
    partition: str
    time: str
    nodes: str
    tasks_per_node: str


class LocalParameters(BaseModel):
    numProcs: str


class Host(BaseModel):
    host: str
    slurmport: Optional[str]
    contexts: List[str]
    routes: Optional[List[str]]
    sbatch_arguments: Optional[Dict[str, SbatchArguments]]
    local_parameters: Optional[Dict[str, LocalParameters]]


class Config(BaseModel):
    hosts: Dict[str, Host]
    default_sbatch_arguments: Dict[str, SbatchArguments]
    default_local_parameters: Dict[str, LocalParameters]
    md_cluster_filesystem_path: str


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
        self, config: dict = None, config_path=None, reinitialize=False, **kwargs
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
    def is_configured() -> bool:
        """Returns True if the $GEMSHOME/instance_config.json exists and is valid."""
        return InstanceConfig.get_default_path().exists()

    def set_active_config(self, config_path: Path):
        self._config = self.load(instance_config_path=config_path)

    def set_config_data(self, config: dict):
        self._config = config

    @abstractmethod
    def get_default_path(example=False) -> Path:
        """Must be overridden to return the default path for the instance config file."""
        raise NotImplementedError("Must be overridden to return the default path.")

    @classmethod
    def from_dict(cls, config_dict):
        return cls(config=config_dict)

    @staticmethod
    def load(instance_config_path=None) -> dict:
        """Load a json instance config file."""
        if instance_config_path is None:
            instance_config_path = InstanceConfig.get_default_path()

        with open(instance_config_path, "r") as f:
            instance_config = json.load(f)

        return instance_config

    def save(self, instance_config_path):
        """Save a json instance config file."""
        with open(instance_config_path, "w") as f:
            json.dump(self.config, f, indent=2)


class ContextManager(ConfigManager):
    # Not an enum so we can extend. Intended to be an associated type / should probably be a Literal Union.
    Contexts: list = ["DevEnv", "Swarm"]

    def get_available_contexts(self, instance_hostname=None) -> list:
        """
        Returns a list of available contexts for the active GEMS instance.

        Can be keyed by a given name (["hosts"] key) or hostname (["hosts"][host]['host']),
        but the instance config must contain the real hostname in either. (In some cases,
        you need to use the ip for the host, in which case the hosts key must be the
        hostname.)

        """
        if instance_hostname is None:
            instance_hostname = socket.gethostname()

        available_contexts = []
        for host in self.config["hosts"].keys():
            h = self.config["hosts"][host]
            if instance_hostname == host or instance_hostname == h["host"]:
                available_contexts.extend(h["contexts"])
        return available_contexts


class HostManager(ContextManager):
    """ "Host Manager is a Contextual Manager"
    HostManager depends on contexts, which the ContextManager provides.
    """

    def add_host(self, hostname, host, slurmport, contexts=None, sbatch_arguments=None):
        """Adds a host to the instance_config.json.

        This is the only way to add a host to the instance_config.json.
        """
        self.config["hosts"][hostname] = {
            "host": host,
            "slurmport": slurmport,
        }

        if isinstance(contexts, list):
            self.add_contexts_to_host(hostname, contexts)

    def add_contexts_to_host(self, hostname, contexts):
        """Adds contexts to a host."""
        if "contexts" not in self.config["hosts"][hostname]:
            self.config["hosts"][hostname]["contexts"] = []

        self.config["hosts"][hostname]["contexts"].extend(contexts)
        self.config["hosts"][hostname]["contexts"] = list(
            set(self.config["hosts"][hostname]["contexts"])
        )

    def get_possible_hosts_for_context(
        self, context: str, with_slurmport=False, return_names=False
    ) -> list:
        """
        Returns a list of possible hosts for a given context.
        """
        possible_hosts = []
        for name, host in self.config["hosts"].items():
            for host_context in host["contexts"]:
                if host_context == context:
                    if return_names:
                        possible_hosts.append(name)
                    else:
                        if with_slurmport:
                            possible_hosts.append(f"{host['host']}:{host['slurmport']}")
                        else:
                            possible_hosts.append(host["host"])
        return possible_hosts

    def get_named_hostname(self, name) -> str:
        """Returns the actual hostname of a named host.

        Each host is keyed by an arbitrary name in the hosts dict of the instance_config.json.
        """
        return self.config["hosts"][name]["host"]

    def get_name_by_hostname(self, hostname) -> str:
        """Returns the name of a host given it's hostname."""
        for name, host in self.config["hosts"].items():
            if host["host"] == hostname:
                return name
        return None


class KeyedArgManager(HostManager):
    """
    Because this uses extra functionality, but depends on hosts, we inherit from HostManager.
    """

    # associated type to define the possible values for key
    # # in more modern python we could use `type ConfigurationKeys` to define a type alias.
    # I believe we can import this functionality (TypeAlias?) from typing as well...
    # Anyways, I envision this being an associated typed
    class ConfigurationKeys(Enum):
        """Defines the possible host key values."""

        SBATCH_ARGUMENTS = "sbatch_arguments"
        LOCAL_PARAMETERS = "local_parameters"

    # should actually wrap host manager(super) and add the isinstance sbatcha_args check here
    def add_host(self, hostname, host, slurmport, contexts=None, sbatch_arguments=None):
        super().add_host(hostname, host, slurmport, contexts, sbatch_arguments)

        if isinstance(sbatch_arguments, dict):
            for ctx, args in sbatch_arguments.items():
                self.add_keyed_arguments_to_host(
                    "sbatch_arguments", hostname, ctx, args
                )

    def get_default_keyed_arguments(
        self, key: ConfigurationKeys, context="Default"
    ) -> dict:
        """Returns the default keyed arguments for a given context."""
        return self.config[f"default_{key}"][context]

    def get_keyed_arguments_by_context(
        self, key: ConfigurationKeys, context
    ) -> list[dict]:
        """Returns a list of possible keyed arguments per host for a given context."""
        l = []
        for host in self.config["hosts"].values():
            if context in host["contexts"] and key in host:
                l.append(host[key])

        if context in self.config[f"default_{key}"]:
            l.append(self.config[f"default_{key}"][context])

        return l

    def get_keyed_arguments_by_named_host(
        self, key: ConfigurationKeys, name
    ) -> dict[str, dict]:
        """Returns a dict of possible keyed arguments per context for a given named host."""
        if key not in self.config["hosts"][name]:
            return {}

        return self.config["hosts"][name][key]

    def get_keyed_arguments_by_hostname(
        self, key: ConfigurationKeys, hostname
    ) -> dict[str, dict]:
        """Returns a dict of possible keyed arguments per context for a given host."""
        name = self.get_name_by_hostname(hostname)
        if name is None or key not in self.config["hosts"][name]:
            return {}
        return self.config["hosts"][name][key]

    def get_keyed_arguments(self, key: ConfigurationKeys, host=None, context=None):
        """Returns the keyed arguments for a given host and context.

        ex. key in ('sbatch_arguments', 'local_parameters')
        """
        args_dict = self.get_default_keyed_arguments(key)
        if host is None:
            if context is None:
                return args_dict
            else:
                possible_hosts = self.get_possible_hosts_for_context(
                    context, return_names=True
                )
                # TODO: More complicated selection of proper host
                host = possible_hosts.pop()

        possible_keyed_args = self.get_keyed_arguments_by_named_host(key, host)
        for ctx, args in possible_keyed_args.items():
            if ctx == context:
                args_dict.update(args)

        return args_dict

    def add_keyed_arguments_to_host(
        self, key: ConfigurationKeys, hostname, context, args
    ):
        """Adds sbatch arguments to a host for a given context."""
        if hostname not in self.config["hosts"]:
            raise InstanceConfigError(
                f"Hostname {hostname} not found in instance_config.json."
            )

        if key not in self.config["hosts"][hostname]:
            self.config["hosts"][hostname][key] = {}

        if context not in self.config["hosts"][hostname][key]:
            self.config["hosts"][hostname][key][context] = {}
        self.config["hosts"][hostname][key][context].update(args)


class DateReversioner:
    """A class to check if a ConfigManger's config file is older than the updated config file.

    This class should not modify production configuratoin files. It should only run in a DevEnv.
    """

    ...


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
            # TODO: Is this sensible?
            if is_GEMS_test_workflow():
                context = self.Context.DEV_ENV
            elif host is not None and self.Context.SWARM in self.get_available_contexts(
                host
            ):
                context = self.Context.SWARM

        return super().get_keyed_arguments(key, host, context)

    # specialized md cluster host helpers aka "MDaaS-RunMD" context helpers
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
