import json, os, glob, shutil, socket
from pathlib import Path

from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow

# from gemsModules.logging.logger import Set_Up_Logging


# log = Set_Up_Logging(__name__)


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
    def load() -> dict:
        instance_config_path = Path(os.getenv("GEMSHOME", "")) / "instance_config.json"
        if not instance_config_path.exists():
            raise FileNotFoundError(
                f"instance_config.json not found at GEMSHOME: {instance_config_path}\n"
                f"Please copy the example file from {os.getenv('GEMSHOME', '$GEMSHOME')}/instance_config.json.example.",
            )

        with open(instance_config_path, "r") as f:
            instance_config = json.load(f)
        return instance_config

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
        self, context: str, with_slurmport=False
    ) -> list:
        """
        Returns a list of possible hosts for a given context.
        """
        possible_hosts = []
        for host in self["hosts"].values():
            for host_context in host["contexts"]:
                if host_context == context:
                    if with_slurmport:
                        possible_hosts.append(f"{host['host']}:{host['slurmport']}")
                    else:
                        possible_hosts.append(host["host"])
        return possible_hosts

    # sbatch argument helpers
    def get_default_sbatch_arguments(self, context="Default") -> dict:
        return self["default_sbatch_arguments"][context]

    def get_sbatch_arguments_by_context(self, context) -> list[dict]:
        l = []
        for host in self["hosts"].values():
            l.append(host["sbatch_arguments"])

    def get_named_hostname(self, name) -> str:
        return self["hosts"][name]["host"]

    def get_name_by_hostname(self, hostname) -> str:
        for name, host in self["hosts"].items():
            if host["host"] == hostname:
                return name
        return None

    def get_sbatch_arguments_by_host(self, hostname) -> dict[str, dict]:
        name = self.get_name_by_hostname(hostname)
        return self["hosts"][name]["sbatch_arguments"]

    def get_sbatch_arguments(self, host=None, context=None):
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
                possible_hosts = self.get_possible_hosts_for_context(context)
                # TODO: More complicated selection of proper host
                host = possible_hosts.pop()

        possible_sbatch_args = self.get_sbatch_arguments_by_host(host)
        for ctx, args in possible_sbatch_args.items():
            if ctx == context:
                sb_arg_dict.update(args)
                return sb_arg_dict
