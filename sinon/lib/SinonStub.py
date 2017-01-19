'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
'''
from .util import Wrapper
from .SinonSpy import SinonSpy

class SinonStub(SinonSpy):
    """
    A stub class of any inspector such as stub/expectation
    It provides all spy functions
    It provides functions same as sinonjs. (excluding closure-related function)
    Argument of constructor can be:
    (1) an anonymous function
    (2) an existing function
    (3) a module function
    (4) a module

    All function/module will be replaced into customized or empty function/class
    Able to be assigned special condition (on which call, with what args...etc)
    """

    def __init__(self, obj=None, prop=None, func=None):
        super(SinonStub, self).__init__(obj, prop)
        self.stubfunc = func if func else Wrapper.empty_function
        super(SinonStub, self).wrap2stub(self.stubfunc)
        # Todo: target is a dirty hack
        self.condition = {"args":[], "kwargs":[], "action": [], "oncall":[], "target":self.obj}
        self.cond_args = self.cond_kwargs = self.oncall = None

    def __append_condition(self, func):
        self.condition["args"].append(self.cond_args)
        self.condition["kwargs"].append(self.cond_kwargs)
        self.condition["oncall"].append(self.oncall)
        self.condition["action"].append(func)
        self.cond_args = self.cond_kwargs = self.oncall = None

    def withArgs(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Adding arguments into condition list
        When meeting conditions, special return will be triggered

        When stub function is called with arguments 1, it will return "#"
            stub.withArgs(1).returns("#")

        Without returns/throws in the end of chained functions, nothing will happen
        In this case, although 1 is in condition list, nothing will happed
            stub.withArgs(1)

        Return:
            self (able to be chained)
        """
        if args:
            self.cond_args = args
        if kwargs:
            self.cond_kwargs = kwargs
        return self

    def onCall(self, n): #pylint: disable=invalid-name
        """
        Adding specified call number into condition list

        When stub function is called second times, it will return "#"
            stub.onCall(2).returns("#")

        Without returns/throws in the end of chained functions, nothing will happen
        In this case, although 2 is in condition list, nothing will happed
            stub.onCall(2)

        Return:
            self (able to be chained)
        """
        self.oncall = n
        return self

    def onFirstCall(self): #pylint: disable=invalid-name,missing-docstring
        self.oncall = 1
        return self

    def onSecondCall(self): #pylint: disable=invalid-name,missing-docstring
        self.oncall = 2
        return self

    def onThirdCall(self): #pylint: disable=invalid-name,missing-docstring
        self.oncall = 3
        return self

    def returns(self, obj):
        """
        Customizing return of stub function

        The final chained functions of returns/throws will be triggered
        If there is some conditions, it will ONLY triggered when meeting conditions

        Args: obj (anything)
        Return: self (able to be chained)
        """
        def return_function(*args, **kwargs):
            """
            A stub function with customized return
            """
            _ = args, kwargs
            return obj

        if self.cond_args or self.cond_kwargs or self.oncall:
            self.__append_condition(return_function)
            super(SinonStub, self).wrap2stub(self.stubfunc, self.condition)
        else:
            super(SinonStub, self).wrap2stub(return_function)
        return self

    def throws(self, exceptions=Exception):
        """
        Customizing exception of stub function

        The final chained functions of returns/throws will be triggered
        If there is some conditions, it will ONLY triggered when meeting conditions

        Args: exception (by default=Exception, it could be any customized exception)
        Return: self (able to be chained)
        """
        def exception_function(*args, **kwargs):
            """
            A stub function with customized exception
            """
            _ = args, kwargs
            raise exceptions

        if self.cond_args or self.cond_kwargs or self.oncall:
            self.__append_condition(exception_function)
            super(SinonStub, self).wrap2stub(self.stubfunc, self.condition)
        else:
            super(SinonStub, self).wrap2stub(exception_function)
        return self
