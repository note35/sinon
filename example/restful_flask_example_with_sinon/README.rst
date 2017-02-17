How to run this example test?
-----------------------------

This test is current for python3 only.


**1.Setup virtual environment**

.. code-block:: shell

    $ pip install virtualenv
    $ virtualenv -p /usr/local/bin/python3.5 venv
    $ . venv/bin/activate

**2.Install requirement.txt**

.. code-block:: shell

    $ pip install -r requirement.txt

**3.Run test**

.. code-block:: shell

    $ python test.py

**Note**

    According to `this <http://stackoverflow.com/questions/18264578/why-does-id-of-an-unbound-method-in-python-2-change-for-every-access>`_ explanation, python2 is not able to run pure class in spy/stub/expectation.
