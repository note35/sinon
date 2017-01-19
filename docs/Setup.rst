Setup
=====

Installation
------------

You can get lastest Sinon.PY from pypi:

.. code-block:: shell

    $ pip install sinon

Install manually:

.. code-block:: shell

    $ git clone https://github.com/note35/sinon.git
    $ cd sinon/
    $ python setup.py install

Since Sinon.PY is a library for unittest, It would be good if using virtualenv
in development environment by following command below:

.. code-block:: shell

    $ pip install virtualenv
    $ virtualenv env
    $ . env/bin/activate   
    $ pip install sinon

Getting Started
---------------

**Spies**

    >>> import sinon
    >>> import os
    >>> spy = sinon.spy(os, "system")
    >>> os.system("pwd")
    to/your/current/path
    >>> spy.called
    True
    >>> spy.calledWith("pwd")
    True
    >>> spy.calledWith(sinon.match(str))
    True 
    >>> spy.calledOnce
    True
    >>> spy.restore()

**Stubs**

    >>> import sinon
    >>> import os
    >>> stub = sinon.stub(os, "system").returns("stub result")
    >>> os.system("pwd")
    'stub result'
    >>> stub.restore()
    >>>
    >>> stub = sinon.stub(os, "system").onCall(2).returns("stub result")
    >>> os.system("pwd")
    >>> os.system("pwd")
    'stub result'
    >>> os.system("pwd")
    >>> stub.restore()
    >>>
    >>> sinon.stub(os, "system").throws()
    >>> stub = sinon.stub(os, "system").throws()
    >>> try:
    ...     system("pwd")
    ... except:
    ...     pass
    ... 
    >>> stub.restore()

.. _virtualenv: https://virtualenv.pypa.io/en/stable/
