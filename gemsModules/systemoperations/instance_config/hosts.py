from gemsModules.logging.logger import Set_Up_Logging

from . import ContextManager

log = Set_Up_Logging(__name__)


class HostManager(ContextManager):
    """ "Host Manager is a Contextual Manager"
    HostManager depends on contexts, which the ContextManager provides.
    """

    def add_host(self, hostname, host, slurmport, contexts=None):
        """Adds a host to the instance_config.json.

        This is the only way to add a host to the instance_config.json.
        """
        if hostname not in self.config["hosts"]:
            self.config["hosts"][hostname] = {
                "host": host,
                "slurmport": slurmport,
            }
        else:
            # slurmport or host differ, warn the user.
            if self.config["hosts"][hostname]["host"] != host:
                log.warning(
                    f"Host {hostname} already exists with a different host value: {self.config['hosts'][hostname]['host']}."
                )
            if self.config["hosts"][hostname]["slurmport"] != slurmport:
                log.warning(
                    f"Host {hostname} already exists with a different slurmport value: {self.config['hosts'][hostname]['slurmport']}."
                )

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
