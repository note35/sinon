Practices
=========

With unittest framework
-----------------------

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

Above python2.7, it could be executed by commands below:

.. code:: shell

    $ python -m unittest [test_file_name]

An example of restful_flask application
---------------------------------------

Please refer the `link <https://github.com/note35/sinon/tree/dev/example/restful_flask_example_with_sinon>`_ to see the project
