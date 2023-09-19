import json, os, glob, shutil, socket
from pathlib import Path

from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow

# from gemsModules.logging.logger import Set_Up_Logging


# log = Set_Up_Logging(_z_name__)


# TODO: tests
class InstanceConfig(dict):
    """
    A class for parsing and using the instance_config.yml of the active GEMS installation.

    This class is a singleton, so it can be instantiated once and then used throughout the
    lifetime of the program.

    >>> instance_config = InstanceConfig()
    >>> instance_config.get_available_contexts('gw-grpc-delegator')


    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InstanceConfig, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if self.__initialized:
            return
        super().__init__(*args, **kwargs)
        self.__initialized = True
        self.update(self.load())

    @staticmethod
    def load(instance_config_path=None) -> dict:
        if instance_config_path is None:
            instance_config_path = InstanceConfig.get_default_path()
        if not instance_config_path.exists():
            raise FileNotFoundError(
                f"instance_config.json not found at GEMSHOME: {instance_config_path}\n"
                f"Please copy the example file from {os.getenv('GEMSHOME', '$GEMSHOME')}/instance_config.json.example.",
            )

        with open(instance_config_path, "r") as f:
            instance_config = json.load(f)
        return instance_config

    @staticmethod
    def get_default_path(example=False) -> Path:
        name = "instance_config.json"
        if example:
            name += ".example"

        return Path(os.getenv("GEMSHOME", "")) / name

    def get_available_contexts(self, instance_hostname=None) -> list:
        """
        Returns a list of available contexts for the active GEMS instance.
        """
        if instance_hostname is None:
            instance_hostname = socket.gethostname()

        available_contexts = []
        for host in self["hosts"].keys():
            if instance_hostname == host:
                available_contexts.extend(host["contexts"])
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

    # sbatch argument helpers
    def get_default_sbatch_arguments(self, context="Default") -> dict:
        """Returns the default sbatch arguments for a given context."""
        return self["default_sbatch_arguments"][context]

    def get_sbatch_arguments_by_context(self, context) -> list[dict]:
        """Returns a list of possible sbatch arguments per host for a given context."""
        l = []
        for host in self["hosts"].values():
            if context in host["contexts"] and "sbatch_arguments" in host:
                l.append(host["sbatch_arguments"])

        l.append(self["default_sbatch_arguments"][context])
        return l

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

    def get_sbatch_arguments_by_named_host(self, name) -> dict[str, dict]:
        """Returns a dict of possible sbatch arguments per context for a given named host."""
        return self["hosts"][name]["sbatch_arguments"]

    def get_sbatch_arguments_by_hostname(self, hostname) -> dict[str, dict]:
        """Returns a dict of possible sbatch arguments per context for a given host."""
        name = self.get_name_by_hostname(hostname)
        return self["hosts"][name]["sbatch_arguments"]

    def get_sbatch_arguments(self, host=None, context=None):
        """Returns the sbatch arguments for a given host and context."""

        if context is None:
            # TODO: Is this sensible?
            if is_GEMS_test_workflow():
                context = "DevEnv"
            elif host is not None and "Swarm" in self.get_available_contexts(host):
                context = "Swarm"

        sb_arg_dict = self.get_default_sbatch_arguments()
        if host is None:
            if context is None:
                return sb_arg_dict
            else:
                possible_hosts = self.get_possible_hosts_for_context(
                    context, return_names=True
                )
                # TODO: More complicated selection of proper host
                host = possible_hosts.pop()

        possible_sbatch_args = self.get_sbatch_arguments_by_named_host(host)
        for ctx, args in possible_sbatch_args.items():
            if ctx == context:
                sb_arg_dict.update(args)
                return sb_arg_dict