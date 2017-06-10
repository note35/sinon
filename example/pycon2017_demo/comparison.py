from unittest import mock
import unittest
import sinon

import os

class TestOS(unittest.TestCase):

    @mock.patch("os.system", return_value="mock!")
    def test_mock_os_system(self, mock):
        self.assertEqual(os.system("ls"), "mock!")

    @sinon.test
    def test_sinon_os_system(self):
        sinon.stub(os, "system").returns("mock!")
        self.assertEqual(os.system("ls"), "mock!")
