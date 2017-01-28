Assertions
==========

Sinon.PY ships with a set of assertions that mirror most behavior verification. The advantage of using the assertions is that failed expectations on stubs and spies can be expressed directly as assertion failures with detailed and helpful error messages.

To make sure assertions integrate nicely with your test framework, you should customize sinon.assert.fail.

The assertions can be used with either spies or stubs.

.. _assertion-api-label:

Assertions API
--------------

**sinon.assertion.fail(message)**

Setting error message when assert failed, by default the error message is empty.

.. code-block:: python

    spy = sinon.spy()
    sinon.assertion.fail("expected exception message")
    sinon.assertion.called(spy)
    """
    Traceback (most recent call last):
      ...
    AssertionError: expected exception message
    """

**sinon.assertion.failException**

The exception when assert failed, by default the exception is "AssertError".

.. code-block:: python

    spy = sinon.spy()
    sinon.assertion.failException = Exception
    sinon.assertion.called(spy)
    """
    Traceback (most recent call last):
      ...
    Exception
    """

**sinon.assertion.notCalled(spy)**

Passes if spy was never called.

.. code-block:: python

    spy = sinon.spy(os, "system")
    sinon.assertion.notCalled(spy)

**sinon.assertion.called(spy)**

Passes if spy was called at least once.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.called(spy)

**sinon.assertion.calledOnce(spy)**

Passes if spy was called once and only once.

**sinon.assertion.calledTwice()**

Passes if spy was called exactly twice.

**sinon.assertion.calledThrice()**

Passes if spy was called exactly three times.

**sinon.assertion.callCount(spy, num)**

Passes if the spy was called exactly num times.

.. code-block:: python

    spy = sinon.spy()
    sinon.assertion.callCount(spy, 0)
    spy()
    sinon.assertion.callCount(spy, 1)

**sinon.assertion.callOrder(spy1, spy2, ...)**

Passes if the provided spies where called in the specified order.

.. code-block:: python

    spy1 = sinon.spy()
    spy2 = sinon.spy()
    spy3 = sinon.spy()

    spy1()
    spy2()
    spy3()
    sinon.assertion.callOrder(spy1, spy2, spy3)
    sinon.assertion.callOrder(spy2, spy3)
    sinon.assertion.callOrder(spy1, spy3)
    sinon.assertion.callOrder(spy1, spy2)

    spy1()
    sinon.assertion.callOrder(spy1, spy1)
    sinon.assertion.callOrder(spy3, spy1)
    sinon.assertion.callOrder(spy2, spy1)
    sinon.assertion.callOrder(spy2, spy3, spy1)
    sinon.assertion.callOrder(spy1, spy2, spy3, spy1)

**sinon.assertionion.calledWith(spy, \*args, \*\*kwargs)**

Passes if the spy was called with the provided arguments.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.calledWith(spy, "pwd")

**sinon.assertion.alwaysCalledWith(spy, \*args, \*\*kwargs)**

Passes if the spy was always called with the provided arguments.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.alwaysCalledWith(spy, "pwd") #pass
    os.system("ls")
    sinon.assertion.alwaysCalledWith(spy, "pwd") #fail

**sinon.assertion.neverCalledWith(spy, \*args, \*\*kwargs)**

Passes if the spy was never called with the provided arguments.

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.neverCalledWith(spy, "ls")

**sinon.assertion.calledWithExactly(spy, \*args, \*\*kwargs)**

Passes if the spy was called with the provided arguments and no others.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    os.getenv("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    sinon.assertion.calledWithExactly(spy, "NOT_EXIST_ENV_VAR", "DEFAULT_VALUE") #pass
    sinon.assertion.calledWithExactly(spy, "NOT_EXIST_ENV_VAR") #fail

**sinon.assertion.alwaysCalledWithExactly(spy, \*args, \*\*kwargs)**

Passes if the spy was always called with the provided arguments and no others.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    os.getenv("NOT_EXIST_ENV_VAR", "DEFAULT_VALUE")
    sinon.assertion.alwaysCalledWithExactly(spy, "NOT_EXIST_ENV_VAR", "DEFAULT_VALUE") #pass
    os.getenv("NOT_EXIST_ENV_VAR", "ANOTHER_VALUE")
    sinon.assertion.alwaysCalledWithExactly(spy, "NOT_EXIST_ENV_VAR", "DEFAULT_VALUE") #fail

**sinon.assertion.calledWithMatch(spy, \*args, \*\*kwargs)**

Passes if the spy was called with matching arguments. This behaves the same as sinon.assertion.calledWith(spy, sinon.match(arg1), sinon.match(arg2), ...).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.calledWithMatch(spy, str)
    sinon.assertion.calledWith(spy, sinon.match(str))

**sinon.assertion.alwaysCalledWithMatch(spy, \*args, \*\*kwargs)**

Passes if the spy was always called with matching arguments. This behaves the same as sinon.assertion.alwaysCalledWith(spy, sinon.match(arg1), sinon.match(arg2), ...).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.alwaysCalledWithMatch(spy, str)
    os.system("ls")
    sinon.assertion.alwaysCalledWithMatch(spy, str)

**sinon.assertion.neverCalledWithMatch(spy, \*args, \*\*kwargs)**

Passes if the spy was never called with matching arguments. This behaves the same as sinon.assertion.neverCalledWith(spy, sinon.match(arg1), sinon.match(arg2), ...).

.. code-block:: python

    spy = sinon.spy(os, "system")
    os.system("pwd")
    sinon.assertion.neverCalledWithMatch(spy, int)

**sinon.assertion.threw(spy, exception=None)**

Passes if the spy threw the given exception. If only one argument is provided, the assertion passes if the spy ever threw any exception.

.. code-block:: python

    spy = sinon.spy(os, "getenv")
    try:
        os.getenv(1000000000)
    except:
        sinon.assertion.threw(spy, TypeError)

**sinon.assertion.alwaysThrew(spy, exception=None)**

Like above, only required for all calls to the spy.
