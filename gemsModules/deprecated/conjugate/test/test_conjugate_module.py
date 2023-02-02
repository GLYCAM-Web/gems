import os
import unittest

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
Testing for the integrity of the delgator module in general
"""
class TestModule(unittest.TestCase):

    def test_help_file_exists(self):
        targetFile = GemsPath + "/gemsModules/deprecated/conjugate/helpme.py"
        exists = os.path.isfile(targetFile)
        self.assertTrue(exists)

    def test_receive_file_exists(self):
        targetFile = GemsPath + "/gemsModules/deprecated/conjugate/receive.py"
        exists = os.path.isfile(targetFile)
        self.assertTrue(exists)

    def test_settings_file_exists(self):
        targetFile = GemsPath + "/gemsModules/deprecated/conjugate/settings.py"
        exists = os.path.isfile(targetFile)
        self.assertTrue(exists)




if __name__ == '__main__':
    unittest.main()
