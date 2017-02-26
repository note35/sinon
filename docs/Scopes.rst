Scopes
======

.. _scope-reason-label:

Why should use scope?
---------------------

In a general unittest, the test function will import other classes or modules and test them. However, there are some exceptional possibilities for testing functions in the same module/class/function level.

**For example**

.. code-block:: python

    import sinon

    def a_function_of_test():
        pass

    def test_func():

        spy = sinon.spy(a_function_of_test)
        assert not spy.called
        a_function_of_test()
        assert spy.called

    test_func()

In this case, a_function_of_test is not wrapped successfully. Because the scope is not able to be inspected.

.. code-block:: shell

    AttributeError: 'NoneType' object has no attribute 'a_function_of_test'

.. _scope-label:


Scope API
---------

**sinon.init(scope)**

For getting a inspectable scope, passing globals()/locals() as an argument into .init()

For inspecting the function, using the return scope to call the inspected function instead of calling original function directly.

**Example1: globals()**

.. code-block:: python

    import sinon

    def a_global_function_in_test():
        pass

    def test_func():
        scope = sinon.init(globals())
        spy = sinon.spy(a_global_function_in_test)
        assert not spy.called
        scope.a_global_function_in_test()
        assert spy.called

    test_func()

**Example2: locals()**

.. code-block:: python

    import sinon

    def test_func():

        def a_local_function_in_test():
            pass

        scope = sinon.init(locals())
        spy = sinon.spy(a_local_function_in_test)
        assert not spy.called
        scope.a_local_function_in_test()
        assert spy.called

    test_func()
