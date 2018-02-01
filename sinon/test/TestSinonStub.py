import sys
sys.path.insert(0, '../')

import unittest
import lib.base as sinon
from lib.stub import SinonStub
from lib.sandbox import sinontest

"""
======================================================
                 FOR TEST ONLY START
======================================================
"""
# build-in module
import os
# customized class
class A_object(object):
    # customized function
    def A_func(self):
        return "test_global_A_func"

# global function
def B_func(x=None):
    if x:
        return "test_local_B_func"+str(x)
    return "test_local_B_func"

def C_func(a="a", b="b", c="c"):
    return "test_local_C_func"

def D_func(err=False):
    if err:
        raise err
    else:
        return "test_local_D_func"

from TestClass import ForTestOnly
"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonStub(unittest.TestCase):

    @staticmethod
    def my_func(*args, **kwargs):
        return "my_func"

    def setUp(self):
        sinon.g = sinon.init(globals())

    @sinontest
    def test200_constructor_object_method_with_replaced_method(self):
        a = A_object()
        stub = SinonStub(a, "A_func", TestSinonStub.my_func)
        self.assertEqual(a.A_func(), "my_func")

    @sinontest
    def test201_constructor_empty_object(self):
        stub = SinonStub(A_object)
        a = sinon.g.A_object()
        self.assertTrue("A_func" not in dir(a))

    @sinontest
    def test202_constructor_empty_outside_function(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        self.assertEqual(fto.func1(), None)

    @sinontest
    def test203_constructor_empty_outside_instance_function(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(fto, "func1")
        self.assertEqual(fto.func1(), None)

    @sinontest
    def test204_constructor_empty_library_function(self):
        self.assertEqual(os.system("cd"), 0)
        stub = SinonStub(os, "system", TestSinonStub.my_func)
        self.assertEqual(os.system("cd"), "my_func")
        stub.restore()
        self.assertEqual(os.system("cd"), 0)

    @sinontest
    def test220_returns(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.returns(1)
        self.assertEqual(fto.func1(), 1)
        stub.returns({})
        self.assertEqual(fto.func1(), {})
        stub.returns(TestSinonStub.my_func)
        self.assertEqual(fto.func1(), TestSinonStub.my_func)

    @sinontest
    def test221_throws(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.throws()
        with self.assertRaises(Exception) as context:
            fto.func1()
        stub.throws(TypeError)
        with self.assertRaises(TypeError) as context:
            fto.func1()

    @sinontest
    def test222_withArgs(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs(1).returns("#")
        self.assertEqual(fto.func1(1), "#")
        stub.withArgs(b=1).returns("##")
        self.assertEqual(fto.func1(b=1), "##")
        stub.withArgs(1, b=1).returns("###")
        self.assertEqual(fto.func1(1, b=1), "###")
        self.assertEqual(fto.func1(2), None)

    @sinontest
    def test223_onCall(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.onSecondCall().returns("oncall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "oncall")
        stub.onThirdCall().returns("oncall")
        self.assertEqual(fto.func1(), "oncall")
        self.assertEqual(fto.func1(), None)

    @sinontest
    def test224_onCall_withArgs(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs(1).onThirdCall().returns("oncall")
        stub.withArgs(2).onSecondCall().returns("oncall")
        self.assertEqual(fto.func1(1), None)
        self.assertEqual(fto.func1(1), None)
        self.assertEqual(fto.func1(1), "oncall")
        self.assertEqual(fto.func1(1), None)
        self.assertEqual(fto.func1(2), None)
        self.assertEqual(fto.func1(2), "oncall")
        self.assertEqual(fto.func1(2), None)

    @sinontest
    def test225_onCall_plus_withArgs(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs(1).returns("1")
        stub.withArgs(1).onSecondCall().returns("oncall")
        stub.onThirdCall().returns("##")
        stub.onCall(4).returns("###") # on fifth call will return "###"
        self.assertEqual(fto.func1(1), "1")
        self.assertEqual(fto.func1(1), "oncall")
        self.assertEqual(fto.func1(1), "1") # the priority of onCall is lower than withArgs
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "###")

    @sinontest
    def test226_throws_with_condition(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.onSecondCall().throws()
        fto.func1()
        with self.assertRaises(Exception) as context:
            fto.func1()

    @sinontest
    def test230_onFirstCall(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onFirstCall().returns("onFirstCall")
        self.assertEqual(fto.func1(), "onFirstCall")

    @sinontest
    def test231_onSecondCall(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onSecondCall().returns("onSecondCall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "onSecondCall")

    @sinontest
    def test232_onThirdCall(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onThirdCall().returns("onThirdCall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "onThirdCall")

    @sinontest
    def test233_onThirdCall_random_args(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onThirdCall().returns("onThirdCall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(1), "onThirdCall")

    @sinontest
    def test300_cross_module_stub(self):
        fto = ForTestOnly()
        stub = SinonStub(os, "system") #in func3 of fto, it calls os.system
        stub.returns("it's a stub function")
        self.assertEqual(fto.func3(), "it's a stub function")

    @sinontest
    def test301_withArgs_os(self):
        stub = SinonStub(os, "system")
        stub.withArgs("pwd").returns("customized result")
        self.assertEqual(os.system("pwd"), "customized result")
        self.assertFalse(os.system())

    @sinontest
    def test350_withArgs_empty_stub(self):
        stub = SinonStub()
        stub.withArgs(42).returns(1)
        self.assertEqual(stub(42), 1)

    @sinontest
    def test360_pure_returns(self):
        stub = SinonStub()
        stub.returns(5)
        self.assertEqual(stub(), 5)

    @sinontest
    def test361_module_returns(self):
        stub = SinonStub(os, 'system')
        stub.returns(5)
        self.assertEqual(os.system(), 5)
        self.assertEqual(stub(), 5)

    @sinontest
    def test362_function_returns(self):
        stub = SinonStub(C_func)
        stub.returns(5)
        self.assertEqual(stub.g.C_func(), 5)
        self.assertEqual(stub(), 5)

    @sinontest
    def test363_method_returns(self):
        o = A_object()
        stub = SinonStub(o, 'A_func')
        stub.returns(5)
        self.assertEqual(o.A_func(), 5)
        self.assertEqual(stub(), 5)

    @sinontest
    def test364_class_returns(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.returns(5)
        self.assertEqual(stub(fto), 5)

    @sinontest
    def test370_multiple_onCall_returns(self):
        o = A_object()
        stub = SinonStub(o, 'A_func')
        stub.onCall(0).returns(5)
        stub.onCall(1).returns(10)
        stub.onCall(2).returns(20)
        stub.onCall(3).returns(30)
        self.assertEqual(o.A_func(), 5)
        self.assertEqual(o.A_func(), 10)
        self.assertEqual(o.A_func(), 20)
        self.assertEqual(o.A_func(), 30)

    @sinontest
    def test371_multiple_onCall_returns_named_functions(self):
        o = A_object()
        stub = SinonStub(o, 'A_func')
        stub.onFirstCall().returns(5)
        stub.onSecondCall().returns(10)
        stub.onThirdCall().returns(20)
        self.assertEqual(o.A_func(), 5)
        self.assertEqual(o.A_func(), 10)
        self.assertEqual(o.A_func(), 20)

    @sinontest
    def test380_chained_pure_returns(self):
        stub = SinonStub()
        stub.withArgs(42).onFirstCall().returns(1).onSecondCall().returns(2)
        self.assertEqual(stub(42), 1)
        self.assertEqual(stub(42), 2)

    @sinontest
    def test381_chained_module_returns(self):
        stub = SinonStub(os, 'system')
        stub.withArgs(42).onFirstCall().returns(1).onSecondCall().returns(2)
        self.assertEqual(os.system(42), 1)
        self.assertEqual(os.system(42), 2)

    @sinontest
    def test382_chained_function_returns(self):
        stub = SinonStub(C_func)
        stub.withArgs(42).onFirstCall().returns(1).onSecondCall().returns(2)
        self.assertEqual(stub.g.C_func(42), 1)
        self.assertEqual(stub.g.C_func(42), 2)

    @sinontest
    def test383_chained_method_returns(self):
        o = A_object()
        stub = SinonStub(o, 'A_func')
        stub.withArgs(42).onFirstCall().returns(1).onSecondCall().returns(2)
        self.assertEqual(o.A_func(42), 1)
        self.assertEqual(o.A_func(42), 2)

    @sinontest
    def test390_chained_pure_throws(self):
        stub = SinonStub()
        stub.withArgs(42).onFirstCall().throws(Exception('A')).onSecondCall().throws(Exception('B'))
        with self.assertRaisesRegexp(Exception, 'A'):
            stub(42)
        with self.assertRaisesRegexp(Exception, 'B'):
            stub(42)

    @sinontest
    def test391_chained_module_throws(self):
        stub = SinonStub(os, 'system')
        stub.withArgs(42).onFirstCall().throws(Exception('A')).onSecondCall().throws(Exception('B'))
        with self.assertRaisesRegexp(Exception, 'A'):
            os.system(42)
        with self.assertRaisesRegexp(Exception, 'B'):
            os.system(42)

    @sinontest
    def test392_chained_function_throws(self):
        stub = SinonStub(C_func)
        stub.withArgs(42).onFirstCall().throws(Exception('A')).onSecondCall().throws(Exception('B'))
        with self.assertRaisesRegexp(Exception, 'A'):
            stub.g.C_func(42)
        with self.assertRaisesRegexp(Exception, 'B'):
            stub.g.C_func(42)

    @sinontest
    def test393_chained_method_throws(self):
        o = A_object()
        stub = SinonStub(o, 'A_func')
        stub.withArgs(42).onFirstCall().throws(Exception('A')).onSecondCall().throws(Exception('B'))
        with self.assertRaisesRegexp(Exception, 'A'):
            o.A_func(42)
        with self.assertRaisesRegexp(Exception, 'B'):
            o.A_func(42)

    @sinontest
    def test400_correct_precedence(self):
        stub = SinonStub()
        stub.withArgs('A').returns('Arg of A')
        stub.onFirstCall().returns('First call!')
        stub.onSecondCall().returns('Second call!')
        stub.returns('No args')
        self.assertEqual(stub(), 'First call!')
        self.assertEqual(stub('A'), 'Arg of A')
        self.assertEqual(stub(), 'No args')

    @sinontest
    def test401_correct_precedence_throws(self):
        stub = SinonStub()
        stub.withArgs('A').throws(Exception('A'))
        stub.onFirstCall().throws(Exception('First call!'))
        stub.onSecondCall().throws(Exception('Second call!'))
        stub.throws(Exception('No args'))
        with self.assertRaisesRegexp(Exception, 'First call!'):
            stub()
        with self.assertRaisesRegexp(Exception, 'A'):
            stub('A')
        with self.assertRaisesRegexp(Exception, 'No args'):
            stub()

    @sinontest
    def test402_correct_precedence_withArgs_args(self):
        stub = SinonStub()
        stub.withArgs('A').onSecondCall().returns('second call!')
        stub.withArgs('A').returns('Arg of A')
        self.assertEqual(stub(), None)
        self.assertEqual(stub('A'), 'Arg of A')
        self.assertEqual(stub('A'), 'second call!')
        self.assertEqual(stub('A'), 'Arg of A')

    @sinontest
    def test403_correct_precedence_withArgs_kwargs(self):
        stub = SinonStub()
        stub.withArgs(a='A').onSecondCall().returns('second call!')
        stub.withArgs(a='A').returns('Kwarg of A')
        self.assertEqual(stub(), None)
        self.assertEqual(stub(a='A'), 'Kwarg of A')
        self.assertEqual(stub(a='A'), 'second call!')
        self.assertEqual(stub(a='A'), 'Kwarg of A')

    @sinontest
    def test404_correct_precedence_withArgs_args_kwargs(self):
        stub = SinonStub()
        stub.withArgs('A', b='B').onSecondCall().returns('second call!')
        stub.withArgs('A', b='B').returns('Arg of A, Kwarg of B')
        self.assertEqual(stub(), None)
        self.assertEqual(stub('A', b='B'), 'Arg of A, Kwarg of B')
        self.assertEqual(stub('A', b='B'), 'second call!')
        self.assertEqual(stub('A', b='B'), 'Arg of A, Kwarg of B')

    @sinontest
    def test405_correct_precedence_withArgs_args_throws(self):
        stub = SinonStub()
        stub.withArgs('A').onSecondCall().throws(Exception('second call!'))
        stub.withArgs('A').throws(Exception('Arg of A'))
        self.assertEqual(stub(), None)
        with self.assertRaisesRegexp(Exception, 'Arg of A'):
            stub('A')
        with self.assertRaisesRegexp(Exception, 'second call!'):
            stub('A')
        with self.assertRaisesRegexp(Exception, 'Arg of A'):
            stub('A')

    @sinontest
    def test406_correct_precedence_withArgs_kwargs_throws(self):
        stub = SinonStub()
        stub.withArgs(a='A').onSecondCall().throws(Exception('second call!'))
        stub.withArgs(a='A').throws(Exception('Kwarg of A'))
        self.assertEqual(stub(), None)
        with self.assertRaisesRegexp(Exception, 'Kwarg of A'):
            stub(a='A')
        with self.assertRaisesRegexp(Exception, 'second call!'):
            stub(a='A')
        with self.assertRaisesRegexp(Exception, 'Kwarg of A'):
            stub(a='A')

    @sinontest
    def test407_correct_precedence_withArgs_args_kwargs_throws(self):
        stub = SinonStub()
        stub.withArgs('A', b='B').onSecondCall().throws(Exception('second call!'))
        stub.withArgs('A', b='B').throws(Exception('Arg of A, Kwarg of B'))
        self.assertEqual(stub(), None)
        with self.assertRaisesRegexp(Exception, 'Arg of A, Kwarg of B'):
            stub('A', b='B')
        with self.assertRaisesRegexp(Exception, 'second call!'):
            stub('A', b='B')
        with self.assertRaisesRegexp(Exception, 'Arg of A, Kwarg of B'):
            stub('A', b='B')

    @sinontest
    def test408_chained_withArgs_onCall_returns(self):
        stub = SinonStub()
        stub.withArgs(42).onFirstCall().returns(1).onSecondCall().returns(2)
        stub.returns(0);
        self.assertEqual(stub(1), 0)
        self.assertEqual(stub(42), 1)
        self.assertEqual(stub(1), 0)
        self.assertEqual(stub(42), 2)
        self.assertEqual(stub(1), 0)
        self.assertEqual(stub(42), 0)

    @sinontest
    def test409_chained_withArgs_onCall_throws(self):
        stub = SinonStub()
        stub.withArgs(42).onFirstCall().throws(Exception('A')).onSecondCall().throws(Exception('B'))
        stub.throws(Exception('C'));
        with self.assertRaisesRegexp(Exception, 'C'):
            stub(1)
        with self.assertRaisesRegexp(Exception, 'A'):
            stub(42)
        with self.assertRaisesRegexp(Exception, 'C'):
            stub(1)
        with self.assertRaisesRegexp(Exception, 'B'):
            stub(42)
        with self.assertRaisesRegexp(Exception, 'C'):
            stub(1)
        with self.assertRaisesRegexp(Exception, 'C'):
            stub(42)

    @sinontest
    def test410_conditions_do_not_persist(self):
        stub = SinonStub()
        stub.withArgs('A')
        stub.onThirdCall()
        stub.returns(5)
        self.assertEqual(stub(), 5)

    @sinontest
    def test415_conditions_can_be_overwritten_withArgs(self):
        stub = SinonStub()
        stub.withArgs('A').withArgs('B').returns(3)
        self.assertEqual(stub('A'), None)
        self.assertEqual(stub('B'), 3)

    @sinontest
    def test420_conditions_can_be_overwritten_onCall(self):
        stub = SinonStub()
        stub.onFirstCall().onSecondCall().returns(3)
        self.assertEqual(stub(), None)
        self.assertEqual(stub(), 3)

    @sinontest
    def test425_returns_throws_can_be_overwritten(self):
        stub = SinonStub()
        self.assertEqual(stub(), None)
        stub.returns(5)
        self.assertEqual(stub(), 5)
        stub.throws()
        with self.assertRaises(Exception):
            stub()
        stub.returns(10)
        self.assertEqual(stub(), 10)

    @sinontest
    def test430_withArgs_onCall_combine_correctly_returns(self):
        stub = SinonStub()
        stub.withArgs('A').onFirstCall().returns(1)
        stub.withArgs('A').onSecondCall().returns(2)
        stub.withArgs('B').onFirstCall().returns(10)
        stub.withArgs('B').onSecondCall().returns(20)
        self.assertEqual(stub(), None)
        self.assertEqual(stub('A'), 1)
        self.assertEqual(stub('A'), 2)
        self.assertEqual(stub('A'), None)
        self.assertEqual(stub('B'), 10)
        self.assertEqual(stub('B'), 20)
        self.assertEqual(stub('B'), None)

    @sinontest
    def test431_withArgs_onCall_combine_correctly_throws(self):
        stub = SinonStub()
        stub.withArgs('A').onFirstCall().throws(Exception('1'))
        stub.withArgs('A').onSecondCall().throws(Exception('2'))
        stub.withArgs('B').onFirstCall().throws(Exception('10'))
        stub.withArgs('B').onSecondCall().throws(Exception('20'))
        self.assertEqual(stub(), None)
        with self.assertRaisesRegexp(Exception, '1'):
            stub('A')
        with self.assertRaisesRegexp(Exception, '2'):
            stub('A')
        self.assertEqual(stub('A'), None)
        with self.assertRaisesRegexp(Exception, '10'):
            stub('B')
        with self.assertRaisesRegexp(Exception, '20'):
            stub('B')
        self.assertEqual(stub('B'), None)

    @sinontest
    def test432_withArgs_onCall_combine_correctly_class(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs('A').onFirstCall().returns(1)
        stub.withArgs('A').onSecondCall().returns(2)
        stub.withArgs('B').onFirstCall().returns(10)
        stub.withArgs('B').onSecondCall().returns(20)
        self.assertEqual(stub(fto), None)
        self.assertEqual(stub(fto, 'A'), 1)
        self.assertEqual(stub(fto, 'A'), 2)
        self.assertEqual(stub(fto, 'A'), None)
        self.assertEqual(stub(fto, 'B'), 10)
        self.assertEqual(stub(fto, 'B'), 20)
        self.assertEqual(stub(fto, 'B'), None)

    @sinontest
    def test440_returns_does_not_reset_call_count(self):
        stub = SinonStub()
        stub.onFirstCall().returns('first call')
        self.assertEqual(stub(), 'first call')
        stub.onSecondCall().returns('second call')
        self.assertEqual(stub(), 'second call')

    @sinontest
    def test441_throws_does_not_reset_call_count(self):
        stub = SinonStub()
        stub.onFirstCall().throws(Exception('first call'))
        with self.assertRaisesRegexp(Exception, 'first call'):
            stub()
        stub.onSecondCall().throws(Exception('second call'))
        with self.assertRaisesRegexp(Exception, 'second call'):
            stub()

    @sinontest
    def test442_withArgs_onCall_returns_does_not_reset_call_count(self):
        stub = SinonStub()
        self.assertEqual(stub(), None)
        self.assertEqual(stub('A'), None)
        stub.withArgs('A').onSecondCall().returns('second call!')
        self.assertEqual(stub('A'), 'second call!')
        self.assertEqual(stub('A'), None)
        self.assertEqual(stub(), None)

    @sinontest
    def test443_withArgs_onCall_throws_does_not_reset_call_count(self):
        stub = SinonStub()
        self.assertEqual(stub(), None)
        self.assertEqual(stub('A'), None)
        stub.withArgs('A').onSecondCall().throws(Exception('second call!'))
        with self.assertRaisesRegexp(Exception, 'second call'):
            stub('A')
        self.assertEqual(stub('A'), None)
        self.assertEqual(stub(), None)

    @sinontest
    def test500_stub_is_SinonStubCondition_pure(self):
        pure_stub = SinonStub().onFirstCall().throws(BaseException('Hello World')).onSecondCall().returns(42)
        self.assertEqual(pure_stub.callCount, 0)
        with self.assertRaisesRegexp(BaseException, 'Hello World'):
            pure_stub()
        self.assertEqual(pure_stub(), 42)
        self.assertEqual(pure_stub(), None)
        self.assertEqual(pure_stub.callCount, 3)

    @sinontest
    def test510_stub_is_SinonStubCondition_module_function(self):
        module_function_stub = SinonStub(os, "system").onFirstCall().throws(BaseException('Hello World')).onSecondCall().returns(42)
        self.assertEqual(module_function_stub.callCount, 0)
        with self.assertRaisesRegexp(BaseException, 'Hello World'):
            os.system("cd")
        self.assertEqual(os.system("cd"), 42)
        self.assertEqual(os.system("cd"), None)
        self.assertEqual(module_function_stub.callCount, 3)

    @sinontest
    def test520_stub_is_SinonStubCondition_function(self):
        function_stub = SinonStub(C_func).onFirstCall().throws(BaseException('Hello World')).onSecondCall().returns(42)
        self.assertEqual(function_stub.callCount, 0)
        with self.assertRaisesRegexp(BaseException, 'Hello World'):
            sinon.g.C_func()
        self.assertEqual(sinon.g.C_func(), 42)
        self.assertEqual(sinon.g.C_func(), None)
        self.assertEqual(function_stub.callCount, 3)
