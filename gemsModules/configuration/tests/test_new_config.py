import unittest
import pathlib
import os
import json
from gemsModules.configuration.main_api import InstanceConfig, Host, SupportedEntities
from gemsModules.configuration.resource_management_api import Slurm_Specific_Information

class TestNewConfig(unittest.TestCase):
    def setUp(self):
        self.test_dir = pathlib.Path(__file__).parent
        self.cluster_ic_path = self.test_dir / "cluster_ic.json"

    def test_parse_config(self):
        # Test basic loading and Pydantic parsing
        ic = InstanceConfig.parse_file(self.cluster_ic_path)
        self.assertIsNotNone(ic.hosts)
        self.assertGreater(len(ic.hosts), 0)
        
    def test_get_localhost(self):
        ic = InstanceConfig.parse_file(self.cluster_ic_path)
        # In cluster_ic.json, we have hosts. Let's make sure the validator and methods work.
        # Let's set one host as localhost
        for host in ic.hosts:
            if host.name == "swarm":
                host.is_localhost = "True"
            else:
                host.is_localhost = "False"
                
        local_host = ic.get_localhost()
        self.assertIsNotNone(local_host)
        self.assertEqual(local_host.name, "swarm")
        self.assertEqual(ic.get_localhost_hostName(), "swarm")

    def test_get_possible_hosts_for_context(self):
        ic = InstanceConfig.parse_file(self.cluster_ic_path)
        
        # Test with legacy context name mapping
        hosts = ic.get_possible_hosts_for_context("MDaaS-RunMD", return_names=True)
        self.assertIn("thoreau", hosts)
        
        # Test with direct SupportedEntities values
        hosts_ad = ic.get_possible_hosts_for_context("AD", return_names=True)
        self.assertIn("thoreau", hosts_ad)

    def test_get_available_contexts(self):
        ic = InstanceConfig.parse_file(self.cluster_ic_path)
        contexts = ic.get_available_contexts(instance_hostname="thoreau")
        self.assertIn("MD", contexts)
        self.assertIn("MDaaS-RunMD", contexts)
        self.assertIn("AD", contexts)

    def test_paths_lookups(self):
        ic = InstanceConfig.parse_file(self.cluster_ic_path)
        # cluster_ic.json has filesystem_paths: { "MD": "/website/userdata/mmservice/md" }
        # Note that the json keys are strings, which Pydantic converts to SupportedEntities enums
        path = ic.get_filesystem_path_by_service_ID("MD")
        self.assertEqual(path, "/website/userdata/mmservice/md")
        
        path_lower = ic.get_filesystem_path_by_service_ID("md")
        self.assertEqual(path_lower, "/website/userdata/mmservice/md")

    def test_slurm_validation(self):
        # Test that resource specific info is parsed to Slurm_Specific_Information when scheduler is slurm
        host_dict = {
            "name": "cluster_node",
            "address": "10.0.0.1",
            "scheduler": "slurm",
            "resource_specific_information": {
                "use_gres_for_gpus": "False",
                "cpu_hardware_equivalent": "thread"
            }
        }
        host = Host(**host_dict)
        self.assertIsInstance(host.resource_specific_information, Slurm_Specific_Information)
        self.assertEqual(host.resource_specific_information.use_gres_for_gpus, "False")
        self.assertEqual(host.resource_specific_information.cpu_hardware_equivalent, "thread")

if __name__ == "__main__":
    unittest.main()
