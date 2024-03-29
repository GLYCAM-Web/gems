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
# deprecated
# class TestModule(unittest.TestCase):

#     def test_services_file_exists(self):
#         targetFile = GemsPath + "/gemsModules/common/services.py"
#         exists = os.path.isfile(targetFile)
#         self.assertTrue(exists)

#     def test_settings_file_exists(self):
#         targetFile = GemsPath + "/gemsModules/common/settings.py"
#         exists = os.path.isfile(targetFile)
#         self.assertTrue(exists)

#     def test_transaction_file_exists(self):
#         targetFile = GemsPath + "/gemsModules/common/transaction.py"
#         exists = os.path.isfile(targetFile)
#         self.assertTrue(exists)

#     def test_utils_file_exists(self):
#         targetFile = GemsPath + "/gemsModules/common/utils.py"
#         exists = os.path.isfile(targetFile)
#         self.assertTrue(exists)

if __name__ == '__main__':
    unittest.main()
