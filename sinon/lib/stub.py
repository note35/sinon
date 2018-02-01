'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
'''
from .util import Wrapper
from .spy import SinonSpy

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
    Able to be assigned special conditions (on which call, with what args, etc.)
    """

    def __init__(self, obj=None, prop=None, func=None):
        super(SinonStub, self).__init__(obj, prop)
        self._stubfunc = func if func else self.__default_custom_function
        self._wrapper = super(SinonStub, self).wrap2stub(self._stubfunc)
        self._cond_args = self._cond_kwargs = self._oncall = None
        self._copy = self
        self._conditions = {"args":[], "kwargs":[], "action":[], "oncall":[]}
        self._conditions["default"] =  lambda *args, **kwargs: None

    def __default_custom_function(self, *args, **kwargs):
        """
        If the user does not specify a custom function with which to replace the original,
        then this is the function that we shall use. This function allows the user to call
        returns/throws to customize the return value.
        
        Args:
            args: tuple, the arguments inputed by the user
            kwargs: dictionary, the keyword arguments inputed by the user
        Returns:
            anything, the return values specified by the conditions
                      (i.e. what the user defined with returns/throws)
        """
        index_list = self.__get_matching_withargs_indices(*args, **kwargs)
        # if there are 'withArgs' conditions that might be applicable
        if index_list:
            return self.__get_return_value_withargs(index_list, *args, **kwargs)
        # else no 'withArgs' conditions are applicable
        else:
            return self.__get_return_value_no_withargs(*args, **kwargs)

    def __get_matching_indices(self, args, kwargs, args_list, kwargs_list):
        """
        Args:
            args: tuple, the arguments inputed by the user
            kwargs: dictionary, the keyword arguments inputed by the user
            args_list: list, a list of argument tuples
            kwargs_list: list, a list of keyword argument dictionaries
        Returns:
            list, the list of indices in args_list/kwargs_list for which the user args/kwargs match
        """
        if args and kwargs:
            if args in args_list and kwargs in kwargs_list:
                args_indices = [i for i, x in enumerate(args_list) if x == args]
                kwargs_indices = [i for i, x in enumerate(kwargs_list) if x == kwargs]
                return list(set(args_indices).intersection(kwargs_indices))
        # args only
        elif args:
            if args in args_list:
                return [i for i, x in enumerate(args_list) if x == args and not kwargs_list[i]]
        #kwargs only
        elif kwargs:
            if kwargs in kwargs_list:
                return [i for i, x in enumerate(kwargs_list) if x == kwargs and not args_list[i]]
        else:
            return []

    def __get_matching_withargs_indices(self, *args, **kwargs):
        """
        Args:
            args: tuple, the arguments inputed by the user
            kwargs: dictionary, the keyword arguments inputed by the user
        Returns:
            list, the list of indices in conditions for which the user args/kwargs match
        """
        return self.__get_matching_indices(args, kwargs, self._conditions["args"], self._conditions["kwargs"])

    def __get_call_count(self, args, kwargs, args_list, kwargs_list):
        """
        Args:
            args: tuple, the arguments inputed by the user
            kwargs: dictionary, the keyword arguments inputed by the user
            args_list: list, the tuples of args from all the times this stub was called
            kwargs_list: list, the dictionaries of kwargs from all the times this stub was called
        Returns:
            integer, the number of times this combination of args/kwargs has been called
        """
        return len(self.__get_matching_indices(args, kwargs, args_list, kwargs_list))

    def __get_return_value_withargs(self, index_list, *args, **kwargs):
        """    
        Pre-conditions:
           (1) The user has created a stub and specified the stub behaviour
           (2) The user has called the stub function with the specified "args" and "kwargs"
           (3) One or more 'withArgs' conditions were applicable in this case
        Args:
            index_list: list, the list of indices in conditions for which the user args/kwargs match
            args: tuple, the arguments inputed by the user
            kwargs: dictionary, the keyword arguments inputed by the user
        Returns:
            any type, the appropriate return value, based on the stub's behaviour setup and the user input
        """
        c = self._conditions
        args_list = self._wrapper.args_list
        kwargs_list = self._wrapper.kwargs_list

        # indices with an arg and oncall have higher priority and should be checked first
        indices_with_oncall = [i for i in reversed(index_list) if c["oncall"][i]]

        # if there are any combined withArgs+onCall conditions
        if indices_with_oncall:
            call_count = self.__get_call_count(args, kwargs, args_list, kwargs_list)
            for i in indices_with_oncall:
                if c["oncall"][i] == call_count:
                    return c["action"][i](*args, **kwargs)

        # else if there are simple withArgs conditions
        indices_without_oncall = [i for i in reversed(index_list) if not c["oncall"][i]]
        if indices_without_oncall:
            max_index = max(indices_without_oncall)
            return c["action"][max_index](*args, **kwargs)

        # else all conditions did not match
        return c["default"](*args, **kwargs)

    def __get_return_value_no_withargs(self, *args, **kwargs):
        """    
        Pre-conditions:
           (1) The user has created a stub and specified the stub behaviour
           (2) The user has called the stub function with the specified "args" and "kwargs"
           (3) No 'withArgs' conditions were applicable in this case
        Args:
            args: tuple, the arguments inputed by the user
            kwargs: dictionary, the keyword arguments inputed by the user
        Returns:
            any type, the appropriate return value, based on the stub's behaviour setup and the user input
        """
        c = self._conditions
        call_count = self._wrapper.callCount

        # if there might be applicable onCall conditions
        if call_count in c["oncall"]:
            index_list = [i for i, x in enumerate(c["oncall"]) if x and not c["args"][i] and not c["kwargs"][i]]
            for i in reversed(index_list):
                # if the onCall condition applies
                if call_count == c["oncall"][i]:
                    return c["action"][i](*args, **kwargs)

        # else all conditions did not match
        return c["default"](*args, **kwargs)

    def _append_condition(self, sinon_stub_condition, func):
        '''
        Permanently saves the current (volatile) conditions, which would be otherwise lost

        In the _conditions dictionary, the keys "args", "kwargs", "oncall" and "action"
        each refer to a list. All 4 lists have a value appended each time the user calls
        returns or throws to add a condition to the stub. Hence, all 4 lists are in sync,
        so a single index refers to the same condition in all 4 lists.

        e.g.
            stub.withArgs(5).returns(7)
              # conditions: args [(5,)] kwargs [()] oncall [None] action [7]
            stub.withArgs(10).onFirstCall().returns(14)
              # conditions: args [(5,),(10,)] kwargs [(),()] oncall [None,1] action [7,14]

        Args:
            sinon_stub_condition: the _SinonStubCondition object that holds the current conditions
            func: returns a value or raises an exception (i.e. the action to take, as specified by the user)
        '''
        self._conditions["args"].append(sinon_stub_condition._cond_args)
        self._conditions["kwargs"].append(sinon_stub_condition._cond_kwargs)
        self._conditions["oncall"].append(sinon_stub_condition._oncall)
        self._conditions["action"].append(func)

    def withArgs(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Adds a condition for when the stub is called. When the condition is met, a special
        return value can be returned. Adds the specified argument(s) into the condition list.

        For example, when the stub function is called with argument 1, it will return "#":
            stub.withArgs(1).returns("#")

        Without returns/throws at the end of the chain of functions, nothing will happen.
        For example, in this case, although 1 is in the condition list, nothing will happen:
            stub.withArgs(1)

        Return:
            a SinonStub object (able to be chained)
        """
        cond_args = args if len(args) > 0 else None
        cond_kwargs = kwargs if len(kwargs) > 0 else None
        return _SinonStubCondition(copy=self._copy, cond_args=cond_args, cond_kwargs=cond_kwargs, oncall=self._oncall)

    def onCall(self, n): #pylint: disable=invalid-name
        """
        Adds a condition for when the stub is called. When the condition is met, a special
        return value can be returned. Adds the specified call number into the condition
        list.

        For example, when the stub function is called the second time, it will return "#":
            stub.onCall(1).returns("#")

        Without returns/throws at the end of the chain of functions, nothing will happen.
        For example, in this case, although 2 is in the condition list, nothing will happen:
            stub.onCall(2)

        Args:
            n: integer, the call # for which we want a special return value.
               The first call has an index of 0.

        Return:
            a SinonStub object (able to be chained)
        """
        cond_oncall = n + 1
        return _SinonStubCondition(copy=self._copy, oncall=cond_oncall, cond_args=self._cond_args, cond_kwargs=self._cond_kwargs)

    def onFirstCall(self): #pylint: disable=invalid-name
        """
        Equivalent to stub.onCall(0)
        """
        return self.onCall(0)

    def onSecondCall(self): #pylint: disable=invalid-name
        """
        Equivalent to stub.onCall(1)
        """
        return self.onCall(1)

    def onThirdCall(self): #pylint: disable=invalid-name
        """
        Equivalent to stub.onCall(2)
        """
        return self.onCall(2)

    def returns(self, obj):
        """
        Customizes the return values of the stub function. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: obj (anything)
        Return: a SinonStub object (able to be chained)
        """
        self._conditions["default"] = lambda *args, **kwargs: obj
        return self

    def throws(self, exception=Exception):
        """
        Customizes the stub function to raise an exception. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: exception (by default=Exception, it could be any customized exception)
        Return: a SinonStub object (able to be chained)
        """
        def exception_function(*args, **kwargs):
            raise exception
        self._conditions["default"] = exception_function
        return self

class _SinonStubCondition(SinonStub):
    """
    Allows a new SinonStub object to be created each time the end user specifies a new condition. This is necessary
    to mimic the behaviour of Sinon.JS.

    Author: Jonathan Benn
    """

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ provided by SinonBase, since we don't want to do any function wrapping
        """
        return object.__new__(cls)

    def __init__(self, copy, cond_args, cond_kwargs, oncall):
        """
        Args:
            copy: the original SinonStub object that spawned this one
            cond_args: the args to which a subsequent call to returns/throws should apply
            cond_kwargs: the kwargs to which a subsequent call to returns/throws should apply
            oncall: the integer call number to which a subsequent call to returns/throws should apply
        """
        self._copy = copy
        self._cond_args = cond_args
        self._cond_kwargs = cond_kwargs
        self._oncall = oncall

    @property
    def args_type(self): #pylint: disable=missing-docstring
        return self._copy.args_type

    @property
    def pure(self): #pylint: disable=missing-docstring
        return self._copy.pure

    @property
    def obj(self): #pylint: disable=missing-docstring
        return self._copy.obj

    @property
    def prop(self): #pylint: disable=missing-docstring
        return self._copy.prop

    @property
    def orig_func(self): #pylint: disable=missing-docstring
        return self._copy.orig_func

    def restore(self): #pylint: disable=missing-docstring
        self._copy.restore()

    def returns(self, obj):
        """
        Customizes the return values of the stub function. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: obj (anything)
        Return: a SinonStub object (able to be chained)
        """
        self._copy._append_condition(self, lambda *args, **kwargs: obj)
        return self

    def throws(self, exception=Exception):
        """
        Customizes the stub function to raise an exception. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: exception (by default=Exception, it could be any customized exception)
        Return: a SinonStub object (able to be chained)
        """
        def exception_function(*args, **kwargs):
            raise exception
        self._copy._append_condition(self, exception_function)
        return self
