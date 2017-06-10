try:
    import mock
except ImportError:
    from unittest import mock

import unittest
import os

class TestExample(unittest.TestCase):

    def mock_os_system(command):
        return 0

    @mock.patch("os.system", return_value=1)
    def test_mock_os_system(self, mock_os_system):
        self.assertEqual(os.system("ls"), 1)
        self.assertEqual(os.system("wrong command"), 1)

    def test_os_system(self):
        self.assertEqual(os.system("ls"), 0)
        self.assertNotEqual(os.system("wrong command"), 0)
