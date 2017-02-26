Sandboxes
=========

Sandbox will make each test case isolated.

By default the properties of spy, stub and mock(expectation) of the sandbox is bound to whatever object the function is run on, so if you don’t want to manually restore(), you can use decorator(@sinon.test) to wrap the test function.

.. _restore-label:

.restore()
----------

All inspectors in sinon do not allow multiple wrapping. For example:
 
    >>> spy = sinon.spy(os, "system")
    >>> stub = sinon.stub(os, "system")

This will cause an exception:

.. code-block:: shell 

    Exception: [system] have already been declared

Therefore, for making test cases work, after finishing the mission of that inspector, it should be restored mannually by .restore()

    >>> spy = sinon.spy(os, "system")
    >>> spy.restore()
    >>> stub = sinon.stub(os, "system")
    >>> stub.restore()

.. _sandbox-api-label:

Sandbox API
-----------

**decorator: sinon.test**

Using restore in the end of each testcase makes code size huge. For solving this problem, sandbox is a good solution. Below is an example using sandbox of Sinon.PY. In this example, there is no need to call .restore() anymore, sinon.test will automatically clean all inspectors in each test cases.

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
