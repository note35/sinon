import sys
sys.path.insert(0, '../')

import unittest
import lib.SinonBase as sinon
from lib.SinonMatcher import SinonMatcher

"""
======================================================
                 FOR TEST ONLY START
======================================================
"""
# build-in module
import os
# customized class
class A_object(object):
    # class function
    def A_func(self):
        pass
# global function
def B_func():
    pass

from TestClass import ForTestOnly

"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonMatcher(unittest.TestCase):

    def setUp(self):
        sinon.init(globals())

    def test001_constructor_number(self):
        m = SinonMatcher(1)
        self.assertTrue(m.test(1))
        self.assertFalse(m.test(2))

    def test002_constructor_string(self):
        m = SinonMatcher("match string")
        self.assertTrue(m.test("match"))
        self.assertTrue(m.test("ch st"))
        self.assertTrue(m.test("match string"))
        self.assertFalse(m.test("match string++"))
        self.assertFalse(m.test("match strig"))

    def test003_constructor_regex(self):
        m = SinonMatcher("(\w*) (\w*)", is_regex=True)
        self.assertFalse(m.test("match"))
        self.assertTrue(m.test("ch st"))
        self.assertTrue(m.test("match string"))
        self.assertTrue(m.test("match string++"))
        self.assertTrue(m.test("match strig"))

    def test004_constructor_func(self):
        def custom_test_func(a, b, c):
            return a+b+c
        m = SinonMatcher(custom_test_func)
        self.assertEqual(m.test(1,2,3), 6)
        SinonMatcher.reset()

    def test020_any(self):
        m = SinonMatcher.any
        self.assertTrue(m.test())
        self.assertTrue(m.test(123))
        self.assertTrue(m.test(self))
        self.assertTrue(m.test("asd"))

    def test021_defined(self):
        m = SinonMatcher.defined
        self.assertFalse(m.test())
        self.assertFalse(m.test(None))
        self.assertTrue(m.test([]))
        self.assertTrue(m.test(['1']))
        self.assertTrue(m.test(""))
        self.assertTrue(m.test("1"))

    def test022_truthy(self):
        m = SinonMatcher.truthy
        self.assertFalse(m.test())
        self.assertTrue(m.test(True))
        self.assertFalse(m.test(False))
        self.assertFalse(m.test("asd"))

    def test023_falsy(self):
        m = SinonMatcher.falsy
        self.assertFalse(m.test())
        self.assertFalse(m.test(True))
        self.assertTrue(m.test(False))
        self.assertFalse(m.test("asd"))

    def test024_bool(self):
        m = SinonMatcher.bool
        self.assertFalse(m.test())
        self.assertTrue(m.test(True))
        self.assertTrue(m.test(False))
        self.assertFalse(m.test("asd"))

    def test025_number(self):
        m = SinonMatcher.number
        self.assertFalse(m.test())
        self.assertTrue(m.test(1))
        self.assertTrue(m.test(100000000000000000000))
        self.assertTrue(m.test(1.123))
        self.assertTrue(m.test(100000**10))
        self.assertFalse(m.test("1"))


    def test028_string(self):
        m = SinonMatcher.string
        self.assertFalse(m.test())
        self.assertFalse(m.test(1))
        self.assertTrue(m.test("1"))

    def test027_object(self):
        pass


