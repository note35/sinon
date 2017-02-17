Mocks
=====

What are mocks?
---------------

Mocks (and mock expectations) are fake methods (like spies) with pre-programmed behavior (like stubs) as well as pre-programmed expectations. A mock will return False if it is not used as expected.

When to use mocks?
------------------

Mocks should only be used for the method under test. In every unit test, there should be one unit under test. If you want to control how your unit is being used and like stating expectations upfront (as opposed to asserting after the fact), use a mock.

When to not use mocks?
----------------------

In general you should never have more than one mock (possibly with several expectations) in a single test.

Expectations implement both the :ref:`spy-api-label` and :ref:`stub-api-label`.

To see how mocks look like in Sinon.JS, here’s one of the tests example:

.. code-block:: python

    mock = sinon.mock(os)

    mock.expects("system").returns(0) #always execute successfully
    assert os.system("not exist this command") == 0

    mock.expects("getenv").withArgs("SHELL").returns("/bin/bash") #always return same string
    assert os.getenv("SHELL") == "/bin/bash"

.. _mock-api-label:

Mock API
--------

**mock = sinon.mock(class/instance/module)**

    Creates a mock for the provided class/instance/module. Does not change it, but returns a mock object to set expectations on the it’s methods.

**expectation = mock.expects("function")**

    Overrides the provided function of the mock object and returns it. See :ref:`expectation-label` below.

**mock.restore()**

    Restores all mocked methods.

**mock.verify()**

    Verifies all expectations on the mock. If any expectation is not satisfied, an exception is thrown. Also restores the mocked methods.

.. _expectation-label:

Expectations API
----------------

(1) The constructor of expectation is as same as Spy and Stub.

(2) All the expectation methods return the expectation, meaning you can chain them. Typical usage is below.

.. code-block:: python

    mock = sinon.mock(os).expects("system").atLeast(2).atMost(5)
    os.system("ls")
    assert not mock.verify()
    os.system("ls")
    assert mock.verify()


**expectation.atLeast(number)**

Specify the minimum amount of calls expected.

.. code-block:: python

    mock = sinon.mock(os).expects("system").atLeast(1)
    assert not mock.verify()
    os.system("ls")
    assert mock.verify()

**expectation.atMost(number)**

Specify the maximum amount of calls expected.

.. code-block:: python

    mock = sinon.mock(os).expects("system").atMost(1)
    assert mock.verify()
    os.system("ls")
    os.system("ls")
    assert not mock.verify()

**expectation.never()**

Expect the method to never be called.

.. code-block:: python

    mock = sinon.mock(os).expects("system").never()
    assert mock.verify()
    os.system("ls")
    assert not mock.verify()

**expectation.once()**

Expect the method to be called exactly once.

.. code-block:: python

    mock = sinon.mock(os).expects("system").once()
    assert not mock.verify()
    os.system("ls")
    assert mock.verify()
    os.system("ls")
    assert not mock.verify()

**expectation.twice()**

Expect the method to be called exactly twice.

**expectation.thrice()**

Expect the method to be called exactly thrice.

**expectation.exactly(number)**

Expect the method to be called exactly number times.

**expectation.withArgs(\*args, \*\*kwargs)**

Expect the method to be called with the provided arguments and possibly others.

.. code-block:: python

    mock = sinon.mock(os).expects("getenv").withArgs("SHELL")
    assert not mock.verify()
    os.getenv("SHELL")
    assert mock.verify()

**expectation.withExactArgs(\*args, \*\*kwargs)**

Expect the method to be called with the provided arguments and no others.

.. code-block:: python

    mock = sinon.mock(os).expects("getenv").withExactArgs("SHELL", "/bin/bash")
    assert not mock.verify()
    os.getenv("SHELL")
    assert not mock.verify()
    os.getenv("SHELL", "/bin/bash")
    assert mock.verify()

**expectation.restore()**

Restores current mocked method

.. code-block:: python

    mock = sinon.mock(os)
    expectation = mock.expects("system").returns("stub")
    assert os.system("pwd") == "stub"
    expectation.restore()
    assert os.system("pwd") == 0

**expectation.verify()**

Verifies the expectation and throws an exception if it’s not met.

.. code-block:: python

    mock = sinon.mock(os)
    expectation_system = mock.expects("system").once()
    expectation_getenv = mock.expects("getenv").once()
    os.system("pwd")
    assert not mock.verify()
    assert expectation_system.verify()
