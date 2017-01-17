import sys
sys.path.insert(0, '../')

import unittest
import lib.SinonBase as sinon
from lib.SinonMatcher import SinonMatcher
from lib.SinonSpy import SinonSpy
from lib.SinonStub import SinonStub

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
        sinon.g = sinon.init(globals())

    def test001_constructor_number(self):
        m = SinonMatcher(1)
        self.assertTrue(m.mtest(1))
        self.assertFalse(m.mtest(2))

    def test002_constructor_strcmp_string(self):
        m = SinonMatcher("match string", strcmp="default")
        self.assertTrue(m.mtest("match"))
        self.assertTrue(m.mtest("ch st"))
        self.assertTrue(m.mtest("match string"))
        self.assertFalse(m.mtest("match string++"))
        self.assertFalse(m.mtest("match strig"))

    def test003_constructor_strcmp_regex(self):
        m = SinonMatcher("(\w*) (\w*)", strcmp="regex")
        self.assertFalse(m.mtest("match"))
        self.assertTrue(m.mtest("ch st"))
        self.assertTrue(m.mtest("match string"))
        self.assertTrue(m.mtest("match string++"))
        self.assertTrue(m.mtest("match strig"))

    def test004_constructor_func(self):
        def custom_test_func(a, b, c):
            return a+b+c
        m = SinonMatcher(custom_test_func, is_custom_func=True)
        self.assertEqual(m.mtest(1,2,3), 6)
        m = SinonMatcher("(\w*) (\w*)", strcmp="regex")
        self.assertFalse(m.mtest("match"))

    def test005_constructor_func_invalid(self):
        something = "Not Function"
        with self.assertRaises(Exception) as context:
            m = SinonMatcher(something, is_custom_func=True)

    def test006_constructor_strcmp_invalid(self):
        something = 123
        with self.assertRaises(Exception) as context:
            m = SinonMatcher(something, strcmp="default")

    def test020_any(self):
        m = SinonMatcher.any
        self.assertTrue(m.mtest())
        self.assertTrue(m.mtest(123))
        self.assertTrue(m.mtest(self))
        self.assertTrue(m.mtest("asd"))

    def test021_defined(self):
        m = SinonMatcher.defined
        self.assertFalse(m.mtest())
        self.assertFalse(m.mtest(None))
        self.assertTrue(m.mtest([]))
        self.assertTrue(m.mtest(['1']))
        self.assertTrue(m.mtest(""))
        self.assertTrue(m.mtest("1"))

    def test022_truthy(self):
        m = SinonMatcher.truthy
        self.assertFalse(m.mtest())
        self.assertTrue(m.mtest(True))
        self.assertFalse(m.mtest(False))
        self.assertFalse(m.mtest("asd"))

    def test023_falsy(self):
        m = SinonMatcher.falsy
        self.assertFalse(m.mtest())
        self.assertFalse(m.mtest(True))
        self.assertTrue(m.mtest(False))
        self.assertFalse(m.mtest("asd"))

    def test024_bool(self):
        m = SinonMatcher.bool
        self.assertFalse(m.mtest())
        self.assertTrue(m.mtest(True))
        self.assertTrue(m.mtest(False))
        self.assertFalse(m.mtest("asd"))

    def test30_same(self):
        m = SinonMatcher.same("100")
        self.assertTrue(m.mtest("100"))
        m = SinonMatcher.same(100)
        self.assertTrue(m.mtest(100))
        m = SinonMatcher.same(os.system)
        self.assertTrue(m.mtest(os.system))

    def test40_typeOf_class(self):
        # This is a silly test, normal condition will not use this kinda cases.
        fto = ForTestOnly()
        m = SinonMatcher.typeOf(type)
        self.assertTrue(m.mtest(ForTestOnly)) # class is a type
        self.assertFalse(m.mtest(fto))        # instance is not a type

    def test41_typeOf_instance(self):
        fto = ForTestOnly()
        m = SinonMatcher.typeOf(ForTestOnly)
        self.assertFalse(m.mtest(ForTestOnly))
        self.assertTrue(m.mtest(fto))

    def test42_typeOf_value(self):
        m = SinonMatcher.typeOf(int)
        self.assertFalse(m.mtest("1"))       # string is not a number
        self.assertTrue(m.mtest(1))          # number is a number

    def test43_typeOf_invalid_type(self):
        with self.assertRaises(Exception) as context:
            m = SinonMatcher.typeOf(123)

    def test50_instanceOf_class(self):
        fto = ForTestOnly()
        with self.assertRaises(Exception) as context:
            m = SinonMatcher.instanceOf(ForTestOnly)

    def test51_instanceOf_instance(self):
        spy = SinonSpy()
        stub = SinonStub()
        m = SinonMatcher.instanceOf(spy)
        self.assertTrue(m.mtest(spy))
        self.assertTrue(m.mtest(stub))

    def test060_and_match(self):
        spy = SinonSpy()
        stub = SinonStub()
        m = SinonMatcher.instanceOf(spy).and_match(SinonMatcher.instanceOf(stub))
        self.assertFalse(m.mtest(spy))
        self.assertTrue(m.mtest(stub))

    def test061_or_match(self):
        m = SinonMatcher.typeOf(int).or_match(SinonMatcher.typeOf(str))
        self.assertTrue(m.mtest("1"))
        self.assertTrue(m.mtest(1))
        self.assertFalse(m.mtest())
        self.assertFalse(m.mtest([1, "1"]))
