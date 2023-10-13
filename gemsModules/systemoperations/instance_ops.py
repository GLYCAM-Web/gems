import json, os, glob, shutil, socket
from pathlib import Path

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


class InstanceConfig(dict):
    """
    A class for parsing and using the instance_config.yml of the active GEMS installation.

    This class is a singleton, so it can be instantiated once and then used throughout the
    lifetime of the program.

    >>> instance_config = InstanceConfig()
    >>> instance_config.get_available_contexts('gw-grpc-delegator')

    TODO: This class is getting monolithic, break out functionality. (e.g. md cluster related)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InstanceConfig, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, *args, config_dict=None, config_path=None, **kwargs):
        # Only initialize once
        if self.__initialized:
            return

        super().__init__(*args, **kwargs)
        self.__initialized = True

        if config_dict is None:
            config_dict = self.load(instance_config_path=config_path)

        # update the InstanceConfig dict with the loaded config_dict
        self.update(config_dict)

    @staticmethod
    def is_configured() -> bool:
        """Returns True if the $GEMSHOME/instance_config.json exists and is valid."""
        return InstanceConfig.get_default_path().exists()

    @classmethod
    def from_dict(cls, config_dict):
        return cls(config_dict=config_dict)

    @staticmethod
    def load(instance_config_path=None) -> dict:
        if instance_config_path is None:
            instance_config_path = InstanceConfig.get_default_path()

        with open(instance_config_path, "r") as f:
            instance_config = json.load(f)

        return instance_config

    def save(self, instance_config_path):
        with open(instance_config_path, "w") as f:
            json.dump(self, f, indent=2)

    ### HOSTS METHODS ###
    def add_host(self, hostname, host, slurmport, contexts=None, sbatch_arguments=None):
        """Adds a host to the instance_config.json.

        This is the only way to add a host to the instance_config.json.
        """
        self["hosts"][hostname] = {
            "host": host,
            "slurmport": slurmport,
        }

        if isinstance(sbatch_arguments, dict):
            for ctx, args in sbatch_arguments.items():
                self.add_keyed_arguments_to_host(
                    "sbatch_arguments", hostname, ctx, args
                )

        if isinstance(contexts, list):
            self.add_contexts_to_host(hostname, contexts)

    def add_contexts_to_host(self, hostname, contexts):
        """Adds contexts to a host."""
        if "contexts" not in self["hosts"][hostname]:
            self["hosts"][hostname]["contexts"] = []

        self["hosts"][hostname]["contexts"].extend(contexts)
        self["hosts"][hostname]["contexts"] = list(
            set(self["hosts"][hostname]["contexts"])
        )

    def add_keyed_arguments_to_host(self, key, hostname, context, args):
        """Adds sbatch arguments to a host for a given context."""
        if hostname not in self["hosts"]:
            raise InstanceConfigError(
                f"Hostname {hostname} not found in instance_config.json."
            )

        if key not in self["hosts"][hostname]:
            self["hosts"][hostname][key] = {}

        if context not in self["hosts"][hostname][key]:
            self["hosts"][hostname][key][context] = {}
        self["hosts"][hostname][key][context].update(args)

    ### GETTERS AND SETTERS ###
    @staticmethod
    def get_default_path(example=False) -> Path:
        """The default path is the active GEMS instance configuration."""
        name = "instance_config.json"
        if example:
            name += ".example"

        return Path(os.getenv("GEMSHOME", "")) / name

    # context stuff
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
        for host in self["hosts"].keys():
            h = self["hosts"][host]
            if instance_hostname == host or instance_hostname == h["host"]:
                available_contexts.extend(h["contexts"])
        return available_contexts

    def get_possible_hosts_for_context(
        self, context: str, with_slurmport=False, return_names=False
    ) -> list:
        """
        Returns a list of possible hosts for a given context.
        """
        possible_hosts = []
        for name, host in self["hosts"].items():
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
        return self["hosts"][name]["host"]

    def get_name_by_hostname(self, hostname) -> str:
        """Returns the name of a host given it's hostname."""
        for name, host in self["hosts"].items():
            if host["host"] == hostname:
                return name
        return None

    # sbatch argument
    def get_default_keyed_arguments(self, key, context="Default") -> dict:
        """Returns the default sbatch arguments for a given context."""
        return self[f"default_{key}"][context]

    def get_keyed_arguments_by_context(self, key, context) -> list[dict]:
        """Returns a list of possible sbatch arguments per host for a given context."""
        l = []
        for host in self["hosts"].values():
            if context in host["contexts"] and key in host:
                l.append(host[key])

        if context in self[f"default_{key}"]:
            l.append(self[f"default_{key}"][context])

        return l

    # TODO: if we make sbatch_arguments a property we could do this more cleanly.
    def get_keyed_arguments_by_named_host(self, key, name) -> dict[str, dict]:
        """Returns a dict of possible sbatch arguments per context for a given named host."""
        if key not in self["hosts"][name]:
            return {}

        return self["hosts"][name][key]

    def get_keyed_arguments_by_hostname(self, key, hostname) -> dict[str, dict]:
        """Returns a dict of possible sbatch arguments per context for a given host."""
        name = self.get_name_by_hostname(hostname)
        if name is None or key not in self["hosts"][name]:
            return {}
        return self["hosts"][name][key]

    def get_keyed_arguments(self, key, host=None, context=None):
        """Returns the sbatch arguments for a given host and context."""

        if context is None:
            # TODO: Is this sensible?
            if is_GEMS_test_workflow():
                context = "DevEnv"
            elif host is not None and "Swarm" in self.get_available_contexts(host):
                context = "Swarm"

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

    # md cluster host helpers aka "MDaaS-RunMD" context helpers
    def get_md_filesystem_path(self) -> str:
        """Returns the filesystem path for the compute cluster by hostname defined in the instance config's hosts dict."""
        if (
            "md_cluster_filesystem_path" not in self
            or len(self["md_cluster_filesystem_path"]) == 0
        ):
            log.error(
                "Access attempted but MD Cluster filesystem path not set in instance_config.json."
            )

        return self["md_cluster_filesystem_path"]

    def set_md_filesystem_path(self, path):
        """Sets the filesystem path for the compute cluster by hostname defined in the instance config's hosts dict.

        You probably want to save the instance config after this.
        """
        self["md_cluster_filesystem_path"] = path
