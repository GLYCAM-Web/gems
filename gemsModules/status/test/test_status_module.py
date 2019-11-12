import os
import unittest
import gemsModules
from gemsModules import status

"""
Testing for the integrity of the status module in general.
"""
class TestSettingsModule(unittest.TestCase):

    """settings.py must exist."""
    def test_settings_exist(self):
        targetFile = "../settings.py"
        settingsExist = os.path.isfile(targetFile)
        self.assertTrue(settingsExist)

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
