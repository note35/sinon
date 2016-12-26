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

    def test30_same(self):
        m = SinonMatcher.same("100")
        self.assertTrue(m.test("100"))
        m = SinonMatcher.same(100)
        self.assertTrue(m.test(100))
        m = SinonMatcher.same(os.system)
        self.assertTrue(m.test(os.system))

    def test40_typeOf_class(self):
        # This is a silly test, normal condition will not use this kinda cases.
        fto = ForTestOnly()
        m = SinonMatcher.typeOf(type)
        self.assertTrue(m.test(ForTestOnly)) # class is a type
        self.assertFalse(m.test(fto))        # instance is not a type

    def test41_typeOf_instance(self):
        fto = ForTestOnly()
        m = SinonMatcher.typeOf(ForTestOnly)
        self.assertFalse(m.test(ForTestOnly))
        self.assertTrue(m.test(fto))

    def test42_typeOf_value(self):
        m = SinonMatcher.typeOf(int)
        self.assertFalse(m.test("1"))       # string is not a number
        self.assertTrue(m.test(1))          # number is a number

    def test50_instanceOf_class(self):
        fto = ForTestOnly()
        exception = "[{}] is an invalid property, it should be an instance".format(ForTestOnly)
        with self.assertRaises(Exception) as context:
            m = SinonMatcher.instanceOf(ForTestOnly)
        self.assertTrue(exception in str(context.exception))

    def test51_instanceOf_instance(self):
        spy = SinonSpy()
        stub = SinonStub()
        m = SinonMatcher.instanceOf(spy)
        self.assertTrue(m.test(spy))
        self.assertTrue(m.test(stub))

    def test060_and(self):
        pass

    def test061_or(self):
        m = SinonMatcher.typeOf(int)._or(SinonMatcher.typeOf(str))
        self.assertTrue(m.test("1"))
        self.assertTrue(m.test(1))
        self.assertFalse(m.test())
        self.assertFalse(m.test([1, "1"]))
