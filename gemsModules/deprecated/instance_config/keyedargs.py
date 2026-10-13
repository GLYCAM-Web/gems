from enum import Enum
from typing import Dict, List

from gemsModules.deprecated.instance_config.errors import InstanceConfigError
from gemsModules.deprecated.instance_config.hosts import HostManager

from gemsModules.logging.logger import Set_Up_Logging
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
    ) -> Dict:
        """Returns the default keyed arguments for a given context."""
        def_dict = self.config.get(f"default_{key}", {})
        if isinstance(def_dict, dict) and context in def_dict:
            return def_dict[context].copy() if isinstance(def_dict[context], dict) else def_dict[context]
        return {}

    def get_keyed_arguments_by_context(
        self, key: ConfigurationKeys, context
    ) -> List[Dict]:
        """Returns a list of possible keyed arguments per host for a given context."""
        l = []
        hosts_iter = self.config["hosts"].values() if isinstance(self.config.get("hosts"), dict) else (self.config.get("hosts") or [])
        for host in hosts_iter:
            if isinstance(host, dict) and context in host.get("contexts", []) and key in host:
                l.append(host[key])

        def_key = f"default_{key}"
        if def_key in self.config and context in self.config[def_key]:
            l.append(self.config[def_key][context])

        return l

    def get_keyed_arguments_by_named_host(
        self, key: ConfigurationKeys, name
    ) -> Dict[str, Dict]:
        """Returns a dict of possible keyed arguments per context for a given named host."""
        if key not in self.config["hosts"][name]:
            return {}

        return self.config["hosts"][name][key]

    def get_keyed_arguments_by_hostname(
        self, key: ConfigurationKeys, hostname
    ) -> Dict[str, Dict]:
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

    # using setdefault here:
    def add_keyed_arguments_to_host(
        self, key: ConfigurationKeys, hostname, context, args
    ):
        """Adds sbatch arguments to a host for a given context."""
        if hostname not in self.config["hosts"]:
            raise InstanceConfigError(
                f"Hostname {hostname} not found in instance_config.json."
            )

        self.config["hosts"][hostname].setdefault(key, {}).setdefault(
            context, {}
        ).update(args)
        print(f"Added {key} to {hostname} for context {context} via {args}.")
