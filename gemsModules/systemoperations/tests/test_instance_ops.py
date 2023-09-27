import shutil
import unittest
import pathlib, os
from gemsModules.systemoperations.instance_ops import InstanceConfig


# test case
class Test_InstanceConfig(unittest.TestCase):
    """
    Test the InstanceConfig class.
    """

    def setUp(self):
        """
        Set up for testing InstanceConfig.
        """
        # copy instance_config.json.example to temporarily test.
        example_path = InstanceConfig.get_default_path(example=True)
        self.test_ic_path = pathlib.Path(os.getcwd()) / example_path.name.replace(
            ".example", ""
        )
        shutil.copyfile(example_path, self.test_ic_path)

        self.ic = InstanceConfig(config_path=self.test_ic_path)
        self.ic.load(instance_config_path=self.test_ic_path)

    def tearDown(self) -> None:
        os.remove(self.test_ic_path)

    def test_load(self):
        """
        Test that the load method correctly loads the JSON content.
        """
        config = self.ic.load(instance_config_path=self.test_ic_path)
        self.assertIsInstance(config, dict)
        self.assertIn("hosts", config)

    def test_get_default_path(self):
        """
        Test that the get_default_path returns a valid path.
        """
        default_path = self.ic.get_default_path()
        self.assertIsInstance(default_path, pathlib.Path)

    def test_get_available_contexts(self):
        """
        Test the get_available_contexts method.
        """
        contexts = self.ic.get_available_contexts(instance_hostname="gw-grpc-delegator")
        self.assertIsInstance(contexts, list)

    def test_get_possible_hosts_for_context(self):
        """
        Test the get_possible_hosts_for_context method.
        """
        hosts = self.ic.get_possible_hosts_for_context(context="MDaaS-RunMD")
        self.assertIsInstance(hosts, list)

    def test_get_default_sbatch_arguments(self):
        """
        Test the get_default_sbatch_arguments method.
        """
        sbatch_args = self.ic.get_default_sbatch_arguments(context="Default")
        self.assertIsInstance(sbatch_args, dict)

    def test_get_sbatch_arguments_by_context(self):
        """
        Test the get_sbatch_arguments_by_context method.
        """
        sbatch_args = self.ic.get_sbatch_arguments_by_context(context="MDaaS-RunMD")
        self.assertIsInstance(sbatch_args, list)

    def test_get_named_hostname(self):
        """
        Test the get_named_hostname method.
        """
        hostname = self.ic.get_named_hostname(name="swarm")
        self.assertIsInstance(hostname, str)

    def test_get_name_by_hostname(self):
        """
        Test the get_name_by_hostname method.
        """
        name = self.ic.get_name_by_hostname(hostname="gw-grpc-delegator")
        self.assertIsInstance(name, str)

    def test_get_sbatch_arguments_by_hostname(self):
        """
        Test the get_sbatch_arguments_by_hostname method.
        """
        sbatch_args = self.ic.get_sbatch_arguments_by_hostname(hostname="gw-slurm-head")
        self.assertIsInstance(sbatch_args, dict)

    def test_get_sbatch_arguments(self):
        """
        Test the get_sbatch_arguments method.
        """
        sbatch_args = self.ic.get_sbatch_arguments(host="swarm", context="MDaaS-RunMD")
        self.assertIsInstance(sbatch_args, dict)


if __name__ == "__main__":
    unittest.main()
