Sandboxes
=========

Sandbox will make each test case isolated.

By default the properties of spy, stub and mock(expectation) of the sandbox is bound to whatever object the function is run on, so if you don’t want to manually restore(), you can use decorator(@sinon.test) to wrap the test function.

.. _restore-label:

.restore()
----------

All inspectors in sinon do not allow multiple wrapping. For example:
 
.. code-block:: shell 

    >>> spy = sinon.spy(os, "system")
    >>> stub = sinon.stub(os, "system")

This will cause an exception:

.. code-block:: shell 

    Exception: [system] have already been declared

Thus, for making test cases work, after you finish the mission of that inspector, you should restore it mannually by calling .restore()

.. code-block:: shell 

    >>> spy = sinon.spy(os, "system")
    >>> spy.restore()
    >>> stub = sinon.stub(os, "system")
    >>> stub.restore()

.. _sandbox-label:

@sinon.test
-----------

Using restore in the end of each testcase makes code size huge. For solving this problem, sandbox is a good solution. Below is a fully example about using sandbox of Sinon.PY.

.. code-block:: python 

    import os
    import sinon

    @sinon.test
    def test_os_system_ls():
        spy = sinon.spy(os, "system")
        os.system("ls")
        assert spy.called

    @sinon.test
    def test_os_system_pwd():
        spy = sinon.spy(os, "system")
        os.system("pwd")
        assert spy.called
       
    test_os_system_ls()
    test_os_system_pwd()

You don't need to call .restore() anymore, sinon.test will automatically clean all inspectors in each test cases.
