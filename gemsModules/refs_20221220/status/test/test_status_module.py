import os
import unittest
import gemsModules
from gemsModules import logging

GemsPath = os.environ.get('GEMSHOME')
if GemsPath == None:
    this_dir, this_filename = os.path.split(__file__)
    print("""

    GEMSHOME environment variable is not set.

    Set it using somthing like:

      BASH:  export GEMSHOME=/path/to/gems
      SH:    setenv GEMSHOME /path/to/gems
""")

"""
Testing for the integrity of the status module in general.
"""
class TestModule(unittest.TestCase):

    def test_help_file_exists(self):
        print("GemsPath: " + GemsPath)
        targetFile = GemsPath + "/gemsModules/status/helpme.py"
        exists = os.path.isfile(targetFile)
        self.assertTrue(exists)

    def test_receive_file_exists(self):
        targetFile = GemsPath + "/gemsModules/status/receive.py"
        exists = os.path.isfile(targetFile)
        self.assertTrue(exists)

    def test_settings_file_exists(self):
        targetFile = GemsPath + "/gemsModules/status/settings.py"
        exists = os.path.isfile(targetFile)
        self.assertTrue(exists)

"""
Testing for all methods involved in report generation.
"""
class TestReportGeneration(unittest.TestCase):

    """main() must always return a string"""
    def test_main_returns_string(self):
        response = logging.receive.main()
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
