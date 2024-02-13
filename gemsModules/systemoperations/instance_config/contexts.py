import re
import socket

from gemsModules.logging.logger import Set_Up_Logging

from . import ConfigManager

log = Set_Up_Logging(__name__)


ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


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
        elif ip_regex.match(instance_hostname):
            log.debug(f"Instance hostname is an IP: {instance_hostname}")
            try:
                instance_hostname = socket.gethostbyaddr(instance_hostname)[0]
            except socket.herror:
                log.error(f"Unable to resolve the IP: {instance_hostname}")
                raise ValueError(
                    f"Unable to resolve the GEMS host IP: {instance_hostname}"
                )

        available_contexts = []
        for host in self.config["hosts"].keys():
            h = self.config["hosts"][host]
            if instance_hostname == host or instance_hostname == h["host"]:
                available_contexts.extend(h["contexts"])
        return available_contexts
