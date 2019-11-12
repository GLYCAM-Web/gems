import os
import unittest
import gemsModules
from gemsModules import status

"""
Testing for the integrity of the status module in general.
"""
class TestSettingsModule(unittest.TestCase):

    """settings.py must exist."""
    def test_settings_file_exists(self):
        targetFile = "../settings.py"
        settingsExist = os.path.isfile(targetFile)
        self.assertTrue(settingsExist)

    def test_receive_file_exists(self):
        targetFile = "../receive.py"
        receiveExists = os.path.isfile(targetFile)
        self.assertTrue(receiveExists)

    def test_help_file_exists(self):
        targetFile = "../helpme.py"
        helpmeExists = os.path.isfile(targetFile)
        self.assertTrue(helpmeExists)

"""
Testing for all methods involved in report generation.
"""
class TestReportGeneration(unittest.TestCase):

    """main() must always return a string"""
    def test_main_returns_string(self):
        response = status.receive.main()
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
