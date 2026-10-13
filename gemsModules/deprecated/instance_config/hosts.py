from gemsModules.logging.logger import Set_Up_Logging

from gemsModules.deprecated.instance_config.contexts import ContextManager

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
                "name": hostname,
                "host": host,
                "address": host,
                "slurmport": slurmport,
                "port": slurmport,
            }
        else:
            # slurmport or host differ, warn the user.
            existing_host = self.config["hosts"][hostname].get("host") or self.config["hosts"][hostname].get("address")
            if existing_host and existing_host != host:
                log.warning(
                    f"Host {hostname} already exists with a different host value: {existing_host}."
                )
            existing_port = self.config["hosts"][hostname].get("slurmport") or self.config["hosts"][hostname].get("port")
            if existing_port and str(existing_port) != str(slurmport):
                log.warning(
                    f"Host {hostname} already exists with a different slurmport value: {existing_port}."
                )
            if "host" not in self.config["hosts"][hostname]:
                self.config["hosts"][hostname]["host"] = host
            if "address" not in self.config["hosts"][hostname]:
                self.config["hosts"][hostname]["address"] = host
            if "slurmport" not in self.config["hosts"][hostname]:
                self.config["hosts"][hostname]["slurmport"] = slurmport
            if "port" not in self.config["hosts"][hostname]:
                self.config["hosts"][hostname]["port"] = slurmport

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
        if "entities_available" in self.config["hosts"][hostname]:
            legacy_map = {
                "MDaaS-RunMD": "MD",
                "Sequence-Build3DStructure": "CB",
                "AntibodyDocking": "AD",
                "Glycomimetics": "GM",
                "GlycoProtein": "GP",
            }
            entities = self.config["hosts"][hostname]["entities_available"]
            for ctx in contexts:
                ent = legacy_map.get(ctx, ctx)
                if ent not in entities:
                    entities.append(ent)

    def get_possible_hosts_for_context(
        self, context: str, with_slurmport=False, with_jsonport=False, return_names=False
    ) -> list:
        """
        Returns a list of possible hosts for a given context.
        """
        assert with_jsonport == False or with_slurmport == False, "Cannot have both with_jsonport and with_slurmport set to True."
        possible_hosts = []
        for name, host in self.config["hosts"].items():
            for host_context in host.get("contexts", []):
                if host_context == context:
                    if return_names:
                        possible_hosts.append(name)
                    else:
                        host_addr = host.get("host") or host.get("address")
                        sport = host.get("slurmport") or host.get("port")
                        jport = host.get("jsonport")
                        if with_slurmport and sport:
                            possible_hosts.append(f"{host_addr}:{sport}")
                        elif with_jsonport and jport:
                            possible_hosts.append(f"{host_addr}:{jport}")
                        else:
                            possible_hosts.append(host_addr)
        return possible_hosts

    def get_named_hostname(self, name) -> str:
        """Returns the actual hostname of a named host.

        Each host is keyed by an arbitrary name in the hosts dict of the instance_config.json.
        """
        host_entry = self.config["hosts"].get(name, {})
        if isinstance(host_entry, dict):
            return host_entry.get("host") or host_entry.get("address")
        return None

    def get_name_by_hostname(self, hostname) -> str:
        """Returns the name of a host given it's hostname."""
        for name, host in self.config["hosts"].items():
            if host.get("host") == hostname or host.get("address") == hostname:
                return name
        return None
