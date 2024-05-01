import socket

from gemsModules.logging.logger import Set_Up_Logging

from . import ConfigManager

log = Set_Up_Logging(__name__)


class ContextManager(ConfigManager):
    # Not an enum so we can extend. Intended to be an associated type / should probably be a Literal Union.
    Contexts: list = []

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
