Stubs
=====

What are stubs?
---------------

Test stubs are functions (spies) with pre-programmed behavior. They support the full test :ref:`spy-api-label` in addition to methods which can be used to alter the stub’s behavior.

As spies, stubs can be either anonymous, or wrap existing functions. When wrapping an existing function with a stub, the original function is not called.

When to use stubs?
------------------

Use a stub when you want to:

1. Control a method’s behavior from a test to force the code down a specific path. Examples include forcing a method to throw an error in order to test error handling.

2. When you want to prevent a specific method from being called directly (possibly because it triggers undesired behavior).

Creating stubs: sinon.stub()
----------------------------

**stub = sinon.stub()**

    Creates an anonymous stub function.

**stub = sinon.stub(class/instance/module)**

    Stubs on the provided class/instance/module, which will be replaced into an :ref:`empty-class-label`.

**stub = sinon.stub(myFunc)**

    Stubs on the provided function

    *Note:* If there is a function declared in the same scope of unittest file, you should use :ref:`scope-label`. You can read the reason from :ref:`scope-reason-label`

**stub = sinon.stub(class/instance/module, "method")**

    Creates a stub for object.method and wraps the original method. The stub acts exactly an :ref:`empty-function-label` in all cases. The original method can be restored by calling :ref:`restore-label`. The returned stub is the function object which replaced the original method.

**stub = sinon.stub(class/instance/module, "method", func)**

    Creates a stub for object.method and wraps the original method. The stub acts exactly an provided func in all cases. The original method can be restored by calling :ref:`restore-label`. The returned stub is the function object which replaced the original method.

    Because in python2, if im_self is empty, the unbound function will not have fixed id, thus **class is only supported by python3**.

.. _stub-api-label:

Stub API
--------

*Defining stub behavior on consecutive calls*

    Calling behavior defining methods like returns or throws multiple times overrides the behavior of the stub. You can use the onCall method to make a stub respond differently on consecutive calls.

**stub.withArgs(\*args, \*\*kwargs)**

Stubs the method only for the provided arguments. This is useful to be more expressive in your assertions, where you can access the spy with the same call. It is also useful to create a stub that can act differently in response to different arguments.

**stub.withArgs(\*args, \*\*kwargs)**

Stubs the method only for the provided arguments. This is useful to be more expressive in your assertions, where you can access the spy with the same call. It is also useful to create a stub that can act differently in response to different arguments.

.. code-block:: python

    stub = sinon.stub()
    stub.withArgs(42).returns(1)
    stub.withArgs(1).throws(TypeError)

    assert stub() == None
    assert stub(42) == 1
    try:
        stub(1) # Throws TypeError
    except:
        pass
    stub.exceptions == [TypeError]

**stub.onCall(n)**

Defines the behavior of the stub on the nth call. Useful for testing sequential interactions.

There are methods onFirstCall, onSecondCall,onThirdCall to make stub definitions read more naturally.

.. code-block:: python

    stub = sinon.stub()
    stub.onCall(0).returns(1)
    stub.onCall(1).returns(2)
    stub.returns(3)

    assert stub() == 1
    assert stub() == 2
    assert stub() == 3
    assert stub() == 3

**stub.onFirstCall()**

Alias for stub.onCall(0);

.. code-block:: python

    stub = sinon.stub()
    stub.onFirstCall().returns(1)
    assert stub() == 1
    assert stub() == None

**stub.onSecondCall()**

Alias for stub.onCall(1)

.. code-block:: python

    stub = sinon.stub()
    stub.onSecondCall().returns(2)
    assert stub() == None
    assert stub() == 2

**stub.onThirdCall()**

Alias for stub.onCall(2)

.. code-block:: python

    stub = sinon.stub()
    stub.onThirdCall().returns(3)
    assert stub() == None
    assert stub() == None
    assert stub() == 3

**stub.returns(obj)**

Makes the stub return the provided value.

.. code-block:: python

    stub = sinon.stub()
    stub.returns(["list"])
    assert stub() == ["list"]
    stub.returns(object)
    assert stub() == object

**stub.throws(exception=Exception)**

Causes the stub to throw an exception, default exception is Exception.

.. code-block:: python

    stub = sinon.stub()
    stub.throws(TypeError)
    try:
        stub()
    except TypeError:
        pass
    assert stub.exceptions == [TypeError]

.. _empty-class-label:

Empty Class
-----------

.. code-block:: python

    class EmptyClass(object):
        pass

.. _empty-function-label:

Empty Function
--------------

.. code-block:: python

    def empty_function(\*args, \*\*kwargs):
        pass
