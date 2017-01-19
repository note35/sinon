Test spies
==========

*Note*

    This document is partially referenced from Sinon.JS. However, most usages and API are redesigned.


What is a test spy?
-------------------

A test spy is a function that records arguments, return value, the value of this and exception thrown (if any) for all its calls. A test spy can be an anonymous function or it can wrap an existing function.

When to use spies?
------------------

Test spies are useful to test both callbacks and how certain functions/methods are used throughout the system under test. The following simplified example shows how to use spies to test how a function handles a callback:

.. code-block:: python

    import sinon

    def test_handle_empty_spy():
        callback = sinon.spy()

        def __inner_func(func):
            func("expected_args")

        __inner_func(spy)

        assert spy.called
        assert spy.calledWith("expected_args")

    if __name__ == "__main__":
        test_handle_empty_spy()

Spying on existing methods
--------------------------

.. code-block:: python

    import sinon
    import os

    def test_inspect_os_system():
        spy = sinon.spy(os, "system")
        os.system("pwd")
        assert spy.called
        assert spy.calledWith("pwd")

    if __name__ == "__main__":
        test_inspect_os_system()

Creating spies: sinon.spy()
---------------------------

**spy = sinon.spy()**

    Creates an anonymous function that records arguments, exceptions and return values for all calls.
    
**spy = sinon.spy(myFunc)**

    Spies on the provided function

    *Note:* If there is a function declare in the same scope of unittest file, you should use :ref:`scope-label`. You can read the reason from :ref:`scope-reason-label`

**spy = sinon.spy(class, "method")**

**spy = sinon.spy(instance, "method")**

**spy = sinon.spy(module, "method")**

    Creates a spy for object.method and wraps the original method. The spy acts exactly like the original method in all cases. The original method can be restored by calling :ref:`restore-label`. The returned spy is the function object which replaced the original method.

Spy API
-------

**spy.callCount**

The number of recorded calls.

.. code-block:: python

    spy = sinon.spy(os, "system")
    assert spy.callCount == 0
    os.system("pwd")
    assert spy.callCount == 1
    os.system("pwd")
    assert spy.callCount == 2

**spy.called**

true if the spy was called at least once

.. code-block:: python

    spy = sinon.spy(os, "system")
    assert not spy.called
    os.system("pwd")
    assert spy.called

**spy.calledOnce**

true if spy was called exactly once

.. code-block:: python

    spy = sinon.spy(os, "system")
    assert not spy.calledOnce
    os.system("pwd")
    assert spy.calledOnce
    os.system("pwd")
    assert not spy.calledOnce

**spy.calledTwice**

true if the spy was called exactly twice

.. code-block:: python

    spy = sinon.spy(os, "system")
    assert not spy.calledTwice
    os.system("pwd")
    assert not spy.calledTwice
    os.system("pwd")
    assert spy.calledTwice

**spy.calledThrice**

true if the spy was called exactly thrice

.. code-block:: python

    spy = sinon.spy(os, "system")
    assert not spy.calledThrice
    os.system("pwd")
    assert not spy.calledThrice
    os.system("pwd")
    assert not spy.calledThrice
    os.system("pwd")
    assert spy.calledThrice

**spy.firstCall**

The first call

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    os.getcwd()
    assert spy.firstCall

**spy.secondCall**

The second call

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    os.getcwd()
    assert spy2.secondCall

**spy.thirdCall**

The third call

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    os.getcwd()
    os.system("pwd")
    assert spy.thirdCall

**spy.thirdCall**

The third call

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    os.getcwd()
    os.system("pwd")
    assert spy.thirdCall

**spy.lastCall**

The last call

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    assert spy.lastCall
    os.getcwd()
    assert not spy.lastCall
    assert spy2.lastCall

**spy.calledBefore(anotherSpy)**

Returns true if the spy was called before anotherSpy

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    os.getcwd()
    assert spy.calledBefore(spy2)

**spy.calledAfter(anotherSpy)**

Returns true if the spy was called after anotherSpy

.. code-block:: python

    spy = sinon.spy(os, "system")
    spy2 = sinon.spy(os, "getcwd")
    os.system("pwd")
    os.getcwd()
    assert spy2.calledAfter(spy)

**spy.calledWith(\*args, \*\*kwargs)**

Returns true if spy was called at least once with the provided arguments. Can be used for partial matching, Sinon only checks the provided arguments against actual arguments, so a call that received the provided arguments (in the same spots) and possibly others as well will return true.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    assert spy.calledWith("pwd")

**spy.alwaysCalledWith(\*args, \*\*kwargs)**

Returns true if spy was always called with the provided arguments (and possibly others).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    assert spy.alwaysCalledWith("pwd")
    os.system("ls")
    assert not spy.alwaysCalledWith("pwd")

**spy.calledWithExactly(\*args, \*\*kwargs)**

Returns true if spy was called at least once with the provided arguments and no others.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    os.getenv("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    assert spy.calledWithExactly("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    assert not spy.calledWithExactly("NOT_EXIST_ENV_VAR")
    assert spy.calledWith("NOT_EXIST_ENV_VAR")

**spy.alwaysCalledWithExactly(\*args, \*\*kwargs)**

Returns true if spy was always called with the exact provided arguments.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    os.getenv("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    assert spy.alwaysCalledWithExactly("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    os.getenv("NOT_EXIST_ENV_VAR", "ANOTHER_VALUE")
    assert not spy.alwaysCalledWithExactly("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")

**spy.calledWithMatch(\*args, \*\*kwargs)**

Returns true if spy was called with matching arguments (and possibly others). This behaves the same as spy.calledWith(sinon.match(arg1), sinon.match(arg2), ...).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    assert spy.calledWithMatch(str)
    assert spy.calledWithMatch(sinon.match(str))

**spy.alwaysCalledWithMatch(\*args, \*\*kwargs)**

Returns true if spy was always called with matching arguments (and possibly others). This behaves the same as spy.alwaysCalledWith(sinon.match(arg1), sinon.match(arg2), ...).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    assert spy.alwaysCalledWithMatch(str)
    os.system("ls")
    assert spy.alwaysCalledWithMatch(str)

**spy.neverCalledWith(\*args, \*\*kwargs)**

Returns true if the spy/stub was never called with the provided arguments.

.. code-block:: python

    spy = sinon.spy(os, "system")
    assert spy.neverCalledWith(None)
    os.system("pwd")
    assert spy.neverCalledWith("ls")

**spy.neverCalledWithMatch(\*args, \*\*kwargs)**

Returns true if the spy/stub was never called with matching arguments. This behaves the same as spy.neverCalledWith(sinon.match(arg1), sinon.match(arg2), ...).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    assert spy.neverCalledWithMatch(int)

**spy.threw(Exception=None)**

Returns true if spy threw an provided exception at least once. By default, all exception is included.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    try:
        os.getenv(1000000000)
    except:
        assert spy.threw()
        assert spy.threw(TypeError)

**spy.alwaysThrew(Exception=None)**

Returns true if spy always threw an provided exception.

**spy.returned(obj)**

Returns true if spy returned the provided value at least once.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("ls")
    assert spy.returned(0)

**spy.alwaysReturned(obj)**

Returns true if spy returned the provided value at least once.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("ls")
    os.system("not exist command") # return non-zero value
    assert not spy.alwaysReturned(0)

**var spyCall = spy.getCall(n)**

Returns the nth [call](#spycall).

.. code-block:: python

    sinon.spy(os, "getcwd")
    os.getcwd()
    spy = sinon.spy.getCall(0)
    spy.calledWith("getcwd")

**spy.args**

Array of arguments received, spy.args is a list of arguments(tuple).

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    os.getenv("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    os.getenv("NOT_EXIST_ENV_VAR2")
    assert spy.args == [('NOT_EXIST_ENV_VAR', 'DEFAULT_VALUE'), ('NOT_EXIST_ENV_VAR2',)]

**spy.kwargs**

Array of arguments received, spy.args is a list of arguments(dict).

**spy.exceptions**

Array of exception objects thrown, spy.exceptions is a list of exceptions thrown by the spy. If the spy did not throw an error, the value will be empty.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    try:
        os.getenv(1000000000)
    except:
        assert spy.exceptions == [TypeError]

**spy.returnValues**

Array of return values, spy.returnValues is a list of values returned by the spy. If the spy did not return a value, the value will be None.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("ls")
    assert spy.returnValues == [0]

**spy.reset()**

Resets the state of a spy.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    assert spy.callCount == 1
    os.reset()
    assert spy.callCount == 0
