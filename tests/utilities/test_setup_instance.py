import json
import unittest
import tempfile
from unittest.mock import patch, Mock
import shutil, argparse, os, sys, json, datetime

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)
from bin.setup_instance import main


class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.active_config_path = os.path.join(self.temp_dir.name, "active_config.json")
        self.example_config_path = os.path.join(
            self.temp_dir.name, "example_config.json.example"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("os.getenv")
    @patch("your_module.InstanceConfig.is_configured", new_callable=Mock)
    def test_force_reconfiguration(self, is_configured_mock, getenv_mock):
        # Mock the environment variable to return "True"
        getenv_mock.return_value = "True"
        is_configured_mock.return_value = True  # Simulate that it's configured

        # Create dummy config files
        with open(self.example_config_path, "w") as f:
            f.write(json.dumps({"date": "2023-11-01T00:00:00"}))

        with open(self.active_config_path, "w") as f:
            f.write(json.dumps({"date": "2023-10-01T00:00:00"}))

        with patch(
            "sys.argv",
            ["script_name", "--add-host", "test_host;test_context;localhost:8000"],
        ):
            main()

        # Check if the active_config.json has been updated
        with open(self.active_config_path, "r") as f:
            data = json.load(f)
        self.assertEqual(data["date"], "2023-11-01T00:00:00")

    # You can add more tests similar to the above for other scenarios, like:
    # - when InstanceConfig.is_configured returns False
    # - testing other command-line arguments and their effects


if __name__ == "__main__":
    unittest.main()
