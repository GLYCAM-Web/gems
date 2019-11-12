import unittest
import gemsModules
from gemsModules import status

class TestReportGeneration(unittest.TestCase):

    def test_main(self):

        response = status.receive.main()
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
