from enum import Enum
from gemsModules.logging.logger import Set_Up_Logging

from . import HostManager

log = Set_Up_Logging(__name__)


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
