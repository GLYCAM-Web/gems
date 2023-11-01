import unittest
import tempfile
import os
import json
from pathlib import Path
import datetime
import shutil
from gemsModules.systemoperations.instance_config import DateReversioner


class TestDateReversioner(unittest.TestCase):
    def setUp(self):
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.active_config_path = Path(self.temp_dir.name, "active_config.json")
        self.example_config_path = Path(self.temp_dir.name, "example_config.json")

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_update_no_date(self):
        # Write data to the active config file without a date
        with open(self.active_config_path, "w") as f:
            json.dump({}, f)

        # Write data to the example config file with a date
        example_date = datetime.datetime.now().isoformat()
        with open(self.example_config_path, "w") as f:
            json.dump({"date": example_date}, f)

        reversioner = DateReversioner(self.active_config_path, self.example_config_path)
        reversioner.update()

        with open(self.active_config_path, "r") as f:
            data = json.load(f)

        self.assertEqual(data["date"], example_date)

    def test_update_with_older_date(self):
        # Write data to the active config file with an older date
        old_date = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        with open(self.active_config_path, "w") as f:
            json.dump({"date": old_date}, f)

        # Write data to the example config file with a newer date
        example_date = datetime.datetime.now().isoformat()
        with open(self.example_config_path, "w") as f:
            json.dump({"date": example_date}, f)

        reversioner = DateReversioner(self.active_config_path, self.example_config_path)
        reversioner.update()

        with open(self.active_config_path, "r") as f:
            data = json.load(f)

        self.assertEqual(data["date"], example_date)

    def test_no_update_with_newer_date(self):
        # Write data to the active config file with a newer date
        new_date = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        with open(self.active_config_path, "w") as f:
            json.dump({"date": new_date}, f)

        # Write data to the example config file with an older date
        example_date = datetime.datetime.now().isoformat()
        with open(self.example_config_path, "w") as f:
            json.dump({"date": example_date}, f)

        reversioner = DateReversioner(self.active_config_path, self.example_config_path)
        reversioner.update()

        with open(self.active_config_path, "r") as f:
            data = json.load(f)

        self.assertEqual(data["date"], new_date)

    def test_template_no_date(self):
        # Write data to the active config file with a date
        active_date = datetime.datetime.now().isoformat()
        with open(self.active_config_path, "w") as f:
            json.dump({"date": active_date}, f)

        # Write data to the example config file without a date
        with open(self.example_config_path, "w") as f:
            json.dump({}, f)

        reversioner = DateReversioner(self.active_config_path, self.example_config_path)

        with self.assertRaises(RuntimeError):
            reversioner.update()


if __name__ == "__main__":
    unittest.main()
