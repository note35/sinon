.. image:: https://badge.fury.io/py/sinon.svg
    :target: https://badge.fury.io/py/sinon
.. image:: https://travis-ci.org/note35/sinon.svg?branch=dev
    :alt: dev-branch-ci-status
    :target: https://travis-ci.org/note35/sinon
.. image:: https://coveralls.io/repos/github/note35/sinon/badge.svg
    :target: https://coveralls.io/github/note35/sinon


:Version: 0.0.5
:Download: http://pypi.python.org/pypi/sinon
:Source: https://github.com/note35/sinon
:Keywords: python, unittest, spy, stub, mock, sandbox, unittest2, pytest, sinon, doctest

.. contents::
    :local:

Sinon.py
========

Standalone and test framework agnostic Python test spies, stubs and
mocks (pronounced “sigh-non”).

Special Thanks
==============

This idea is inspired by `sinonjs`_ All the content is copied the idea
but rewriting in python.

.. _sinonjs: https://github.com/sinonjs/sinon

Progress
========

This project is still under developing.

The concept of closure in JS and Python are different,  All features which
are related to Excluding “JS-closure related function” will be ignored.


*base[100%]*
  future: better init() feature

*spy[100%]*
  future: _comb_list feature

*stub[100%]*
  future: callsArgs/yield feature

*mock[100%]*

*sandbox[20%]*
  future: fully sandbox feature

*assertion[100%]*

*matcher[100%]*

*comment of testcases[0%]*

*Documentation[0%]*

Installation
============

    pip install sinon

Usage
=====

    import sinon

Basic Usage
-----------

.. code:: python

    import sinon
    g = sinon.init(globals()) #after all global functions in test cases
    g = sinon.init(locals())  #after all local functions in test cases

Spy
---

Spy contains same functions which are mentioned in `spies`_

.. _spies: http://sinonjs.org/docs/#spies

Declaration:

- spy = sinon.spy()
- spy = sinon.spy(myFunc) #please see example2 below
- spy = sinon.spy(object, "method")
- spy.restore()

Feature:

- spy.withArgs(\*args, \*\*kwargs)
- spy.callCount
- spy.called
- spy.calledOnce
- spy.calledTwice
- spy.calledThrice
- spy.firstCall
- spy.secondCall
- spy.thirdCall
- spy.lastCall
- spy.calledBefore(anotherSpy)
- spy.calledAfter(anotherSpy)
- spy.calledWith(\*args, \*\*kwargs)
- spy.alwaysCalledWith(\*args, \*\*kwargs)
- spy.calledWithExactly(\*args, \*\*kwargs)
- spy.alwaysCalledWithExactly(\*args, \*\*kwargs)
- spy.neverCalledWith(\*args, \*\*kwargs)
- spy.threw(error_type=None)
- spy.alwaysThrew(error_type=None)
- spy.returned(obj)
- spy.alwaysReturned(obj)
- spyCall = spy.getCall(n)
- spy.args
- spy.exceptions
- spy.returnValues
- spy.reset()

*Example1: spy outside function of module*

.. code:: python

    import os

    def some_test_func():
        spy_system = sinon.spy(os, "system")
        os.system("ls")
        assert spy_system.called
        spy_system.restore()

*Example2: spy function in testcase*

.. code:: python

    def func():
        pass

    g = sinon.init(globals())

    def some_test_func():
        spy_func = sinon.spy(func)
        g.func()
        assert spy_func.called
        spy_func.restore()

*Example3: pass spy as a parameter in a local function*

.. code:: python

    def some_test_func():

        def func(arg):
            arg()

        g = sinon.init(locals())
        spy = sinon.spy()
        g.func(spy)
        assert spy.called
        spy.restore()

Stub
----

Stub contains same functions which are mentioned in `stubs`_, which also contains features of spy.

.. _stubs: http://sinonjs.org/docs/#stubs

Declaration:

- stub = sinon.stub()
- stub = sinon.stub(object, "method")
- stub = sinon.stub(object, "method", func)
- stub = sinon.stub(obj)
- stub.restore()

Feature:

- stub.withArgs(\*args, \*\*kwargs)
- stub.onCall(n)
- stub.onFirstCall()
- stub.onSecondCall()
- stub.onThirdCall()
- stub.returns(obj)
- stub.throws(exceptions=Exception)

*Example1: stub outside function of module*

.. code:: python

    import os

    def some_test_func():
        stub_system = sinon.stub(os, "system")
        stub_system.returns(1)
        assert os.system("ls") == 1
        stub_system.restore()

*Example2: stub function in testcase*

.. code:: python

    def func():
        pass

    g = sinon.init(globals())

    def some_test_func():
        stub_func = sinon.stub(func)
        stub_func.onCall(2).returns(100)
        g.func()
        assert stub_func.returned(None)
        g.func()
        assert stub_func.returned(100)
        stub_func.restore()

Mock (Expectation)
------------------

Mock and Expectation contains same functions which are mentioned in `mocks`_. Expectation also contains all features of stub and spy. 

.. _mocks: http://sinonjs.org/docs/#mocks

Declaration:

- mock = sinon.mock(obj)
- expectation = mock.expects("method")
- mock.restore()
- mock.verify()

Feature of expectation:

- expectation.atLeast(number)
- expectation.atMost(number)
- expectation.never()
- expectation.once()
- expectation.twice()
- expectation.thrice()
- expectation.exactly()
- expectation.withArgs(\*args, \*\*kwargs)
- expectation.withExactArgs(\*args, \*\*kwargs)
- expectation.verify() #return boolean instead of raise exception

*Example1: mock single function of module*

.. code:: python

    import os
    def some_test_func():
        mock = sinon.mock(os)
        expectation = mock.expects("system").twice().atLeast(1).atMost(3)
        os.system("ls")
        os.system("ls")
        assert mock.verify()
        mock.restore()

*Example2: mock multiple functions*

.. code:: python

    import os
    def some_test_func():
        mock = sinon.mock(os)
        expectation1 = mock.expects("system").once()
        expectation2 = mock.expects("listdir").never()
        assert not mock.verify()
        assert expectation2.verify()
        mock.restore()

Sandbox
-------

In v1.0.0, sinon.py does not provide any features of sandbox except a decorator.

.. code:: python

    import sinon.sinon as sinon

    @sinon.test
    def someTest():
       ...

After someTest finished, all sinon related objects will be restored automatically.

Test example with unittest framework
------------------------------------

sinon can be used with any test framework, here is a full example.

    python -m unittest [test_file_name]

.. code:: python

    import unittest
    import sinon

    class GlobalCls(object):
        def clsFunc(self):
            return "A"

    def localFunc():
        return "B"

    class TestExample(unittest.TestCase):
 
        def setUp(self):
            global g
            g = sinon.init(globals())

        @sinon.test
        def test001(self):
            import os
            spy_system = sinon.spy(os, "system")
            os.system("ls")
            self.assertTrue(spy_system.called)

        @sinon.test
        def test002(self):
            spy_global_cls = sinon.spy(GlobalCls, "clsFunc")
            gc = GlobalCls()
            gc.clsFunc()
            self.assertTrue(spy_global_cls.called)

        @sinon.test
        def test003(self):
            stub_local_func = sinon.stub(localFunc)
            stub_local_func.returns("A")
            self.assertEqual(g.localFunc(), "A")
