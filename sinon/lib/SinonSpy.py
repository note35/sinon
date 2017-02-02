'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
'''
from .util import ErrorHandler, Wrapper
from .util import CollectionHandler as uch
from .SinonBase import SinonBase
from .SinonMatcher import SinonMatcher, Matcher

class SinonSpy(SinonBase): #pylint: disable=too-many-public-methods
    """
    A spy class of any inspector such as spy/stub/expectation
    It provides functions same as sinonjs. (excluding closure-related function)
    Argument of constructor can be:
    (1) an anonymous function
    (2) an existing function
    (3) an module function

    The function which is wrapped,
    records arguments, return value and exception thrown for all its calls.
    """

    def __init__(self, obj=None, prop=None):
        """
        Constructor of SinonSpy

        instance variable:
            __get_func: storing whether using matcher or not
        """
        super(SinonSpy, self).__init__(obj, prop)
        self.__get_func = SinonSpy.__get_by_matcher

    @staticmethod
    def __get_by_matcher(arg):
        """
        Inspecting argument as a duck type
        Return:
            argument: if argument is a SinonMatcher
            SinonMatcher: if argument is not a SinonMatcher
        """
        return SinonMatcher(arg) if not isinstance(arg, Matcher) else arg

    @staticmethod
    def __get_directly(arg):
        """
        counterpart of __get_by_matcher
        """
        return arg

    def __remove_args_first_item(self):
        """
        # Todo: finding a better solution
        This is a dirty solution
        Because the first argument of inspectors' args will be itself
        For current implementation, it should be ignore
        """
        if len(self._args_list()) > 0:
            new_args_list = []
            for item in self._args_list():
                if self.obj == item[0].__class__:
                    new_args_list.append(item[1:])
                else:
                    new_args_list.append(item[:])
            self._set_args_list(new_args_list)

    def _set_args_list(self, new_args_list):
        """
        For solving special case of mock
        Args: List (new argument list)
        """
        if self.args_type == "MODULE_FUNCTION":
            getattr(self.obj, self.prop).__set__("args_list", new_args_list)
        elif self.args_type == "FUNCTION":
            getattr(self.g, self.obj.__name__).__set__("args_list", new_args_list)
        elif self.args_type == "PURE":
            getattr(self.pure, "func").__set__("args_list", new_args_list)

    def _args_list(self):
        """
        Return: List (arguments which are called)
        """
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).args_list
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).args_list
        elif self.args_type == "PURE":
            return getattr(self.pure, "func").args_list

    def _kwargs_list(self):
        """
        Return: List (dictionary arguments which are called)
        """
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).kwargs_list
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).kwargs_list
        elif self.args_type == "PURE":
            return getattr(self.pure, "func").kwargs_list

    def _error_list(self):
        """
        Return: List (exceptions which are happened)
        """
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).error_list
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).error_list
        elif self.args_type == "PURE": #TODO: consider to remove this condition
            return getattr(self.pure, "func").error_list

    def _ret_list(self):
        """
        Return: List (returns which are happened)
        """
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).ret_list
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).ret_list
        elif self.args_type == "PURE": #TODO: consider to remove this condition
            return getattr(self.pure, "func").ret_list

    def get_callqueue_idx(self):
        """
        Return: List (indexes of self in the CALLQUEUE of Wrapper)
        """
        if self.args_type == "MODULE_FUNCTION":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE)
                    if val == getattr(self.obj, self.prop)]
        elif self.args_type == "MODULE": #TODO: consider to remove this condition
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE)
                    if val == self]
        elif self.args_type == "FUNCTION":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE)
                    if val == getattr(self.g, self.obj.__name__)]
        elif self.args_type == "PURE":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE)
                    if val == getattr(self.pure, "func")]

    def withArgs(self, *args, **kwargs):
        """
        Todo: feature in the future
        """
        return self

    @property
    def callCount(self): #pylint: disable=invalid-name
        """
        Return:
            count of target function
        """
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).callCount
        elif self.args_type == "MODULE": #TODO: consider to remove this condition
            return self.pure_count
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).callCount
        elif self.args_type == "PURE":
            return self.pure_count

    @property
    def called(self): #pylint: disable=missing-docstring
        return True if self.callCount > 0 else False

    @property
    def calledOnce(self): #pylint: disable=invalid-name,missing-docstring
        return True if self.callCount == 1 else False

    @property
    def calledTwice(self): #pylint: disable=invalid-name,missing-docstring
        return True if self.callCount == 2 else False

    @property
    def calledThrice(self): #pylint: disable=invalid-name,missing-docstring
        return True if self.callCount == 3 else False

    @property
    def firstCall(self): #pylint: disable=invalid-name,missing-docstring
        return True if 0 in self.get_callqueue_idx() else False

    @property
    def secondCall(self): #pylint: disable=invalid-name,missing-docstring
        return True if 1 in self.get_callqueue_idx() else False

    @property
    def thirdCall(self): #pylint: disable=invalid-name,missing-docstring
        return True if 2 in self.get_callqueue_idx() else False

    @property
    def lastCall(self): #pylint: disable=invalid-name,missing-docstring
        return True if len(Wrapper.CALLQUEUE)-1 in self.get_callqueue_idx() else False

    def calledBefore(self, obj): #pylint: disable=invalid-name
        """
        Comparing two spys' functions order in CALLQUEUE
        Eg.
            a()
            b()
            spy_a.calledBefore(spy_b) will return True, because a is called before b
            a()
            spy_b.calledBefore(spy_a) will return True, because a is called after b
        Return: Boolean
        """
        idx = self.get_callqueue_idx()
        idx2 = obj.get_callqueue_idx()

        if len(idx) == 0:
            ErrorHandler.callqueue_is_empty_error()
        if Wrapper.CALLQUEUE:
            return True if min(idx) < max(idx2) else False

    def calledAfter(self, obj): #pylint: disable=invalid-name
        """
        Same as calledBefore
        """
        idx = self.get_callqueue_idx()
        idx2 = obj.get_callqueue_idx()

        if len(idx) == 0:
            ErrorHandler.callqueue_is_empty_error()
        if Wrapper.CALLQUEUE:
            return True if max(idx) > min(idx2) else False

    def calledWith(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Determining whether args/kwargs are called previously
        Eg.
            f(1, 2, 3)
            spy.calledWith(1, 2) will return True, because they are called partially
            f(a=1, b=2, c=3)
            spy.calledWith(a=1, b=3) will return True, because they are called partially
        Return: Boolean
        """
        self.__get_func = SinonSpy.__get_directly
        return self.calledWithMatch(*args, **kwargs)

    def alwaysCalledWith(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Determining whether args/kwargs are the ONLY args/kwargs called previously
        Eg.
            f(1, 2, 3)
            f(1, 2, 3)
            spy.alwaysCalledWith(1, 2) will return True, because they are the ONLY called args
            f(1, 3)
            spy.alwaysCalledWith(1) will return True, because 1 is the ONLY called args
            spy.alwaysCalledWith(1, 2) will return False, because 2 is not the ONLY called args
        Return: Boolean
        """
        self.__get_func = SinonSpy.__get_directly
        return self.alwaysCalledWithMatch(*args, **kwargs)

    def calledWithExactly(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Determining whether args/kwargs are fully matched args/kwargs called previously
        Eg.
            f(1, 2, 3)
            spy.alwaysCalledWith(1, 2) will return False, because they are not fully matched
            spy.alwaysCalledWith(1, 2, 3) will return True, because they are fully matched
        Return: Boolean
        """
        self.__remove_args_first_item()
        if args and kwargs:
            return True if (uch.tuple_in_list(self._args_list(), args) and
                            uch.dict_in_list(self._kwargs_list(), kwargs)) else False
        elif args:
            return True if uch.tuple_in_list(self._args_list(), args) else False
        elif kwargs:
            return True if uch.dict_in_list(self._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.called_with_empty_error()

    def alwaysCalledWithExactly(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Determining whether args/kwargs are the ONLY fully matched args/kwargs called previously
        Eg.
            f(1, 2, 3)
            spy.alwaysCalledWith(1, 2, 3) will return True, because they are fully matched
            f(1, 2, 4)
            spy.alwaysCalledWith(1, 2, 4) will return False, because they are not fully matched
        Return: Boolean
        """
        self.__remove_args_first_item()
        if args and kwargs:
            return True if (uch.tuple_in_list_always(self._args_list(), args) and
                            uch.dict_in_list_always(self._kwargs_list(), kwargs)) else False
        elif args:
            return True if uch.tuple_in_list_always(self._args_list(), args) else False
        elif kwargs:
            return True if uch.dict_in_list_always(self._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.called_with_empty_error()

    def calledWithMatch(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Determining whether args/kwargs are matched args/kwargs called previously
        Handle each arg/kwarg as a SinonMatcher
        Eg.
            f(1, 2, 3)
            spy.alwaysCalledWith(1, 2, 3) will return True, because they are fully matched
            spy.alwaysCalledWith(int) will return True, because type are partially matched
        Return: Boolean

        Note: sinon.js have no definition of combination case, here is current implementation:

            for args or kwargs, it should be matched in each individual call
            Eg. func(1,2,3) -> func(4,5,6)
                spy.calledWithMatch(1,5) is not valid
            Eg. func(a=1,b=2,c=3) -> func(a=4,b=5,c=6)
                spy.calledWithMatch(a=1,b=5,c=6) is not valid

            however, for combination case, it should be matched separated
            Eg. func(1,2,c=3) -> func(2,b=5,c=6)
                spy.calledWithMatch(1,2,c=3) is valid,
                    because spy.calledWithMatch(1,2) and spy.calledWithMatch(c=3) are valid
                spy.calledWithMatch(1,c=6) is valid,
                    because spy.calledWithMatch(1) and spy.calledWithMatch(c=6) are valid
                spy.calledWithMatch(1,2,c=6) is valid,
                    because spy.calledWithMatch(1,2) and spy.calledWithMatch(c=6) are valid
        """
        self.__remove_args_first_item()
        if args and kwargs:
            return (uch.tuple_partial_cmp(args, self._args_list(), self.__get_func) and
                    uch.dict_partial_cmp(kwargs, self._kwargs_list(), self.__get_func))
        elif args:
            return uch.tuple_partial_cmp(args, self._args_list(), self.__get_func)
        elif kwargs:
            return uch.dict_partial_cmp(kwargs, self._kwargs_list(), self.__get_func)
        else:
            ErrorHandler.called_with_empty_error()
        self.__get_func = SinonSpy.__get_by_matcher

    def alwaysCalledWithMatch(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Determining whether args/kwargs are the ONLY matched args/kwargs called previously
        Handle each arg/kwarg as a SinonMatcher
        Return: Boolean
        """
        self.__remove_args_first_item()
        alist, klist, gfunc = self._args_list(), self._kwargs_list(), self.__get_func
        if args and kwargs:
            return (uch.tuple_partial_cmp_always(args, alist, gfunc) and
                    uch.dict_partial_cmp_always(kwargs, klist, gfunc))
        elif args:
            return uch.tuple_partial_cmp_always(args, alist, gfunc)
        elif kwargs:
            return uch.dict_partial_cmp_always(kwargs, klist, gfunc)
        else:
            ErrorHandler.called_with_empty_error()
        self.__get_func = SinonSpy.__get_by_matcher

    def neverCalledWith(self, *args, **kwargs): #pylint: disable=invalid-name,missing-docstring
        return not self.calledWith(*args, **kwargs)

    def neverCalledWithMatch(self, *args, **kwargs): #pylint: disable=invalid-name,missing-docstring
        return not self.calledWithMatch(*args, **kwargs)

    def threw(self, error_type=None):
        """
        Determining whether the exception is thrown
        Args:
            error_type:
                None: checking without specified exception
                Specified Exception
        Return: Boolean
        """
        if not error_type:
            return True if len(self._error_list()) > 0 else False
        else:
            return uch.obj_in_list(self._error_list(), error_type)

    def alwaysThrew(self, error_type=None): #pylint: disable=invalid-name
        """
        Determining whether the specified exception is the ONLY thrown exception
        Args:
            error_type:
                None: checking without specified exception
                Specified Exception
        Return: Boolean
        """
        if self.callCount == 0:
            return False
        if not error_type:
            return True if len(self._error_list()) == self.callCount else False
        else:
            return uch.obj_in_list_always(self._error_list(), error_type)

    def returned(self, obj):
        """
        Determining whether the value of obj is returned
        Args: Anything
        Return: Boolean
        """
        return uch.obj_in_list(self._ret_list(), obj)

    def alwaysReturned(self, obj): #pylint: disable=invalid-name
        """
        Determining whether the value of obj is the ONLY returned
        Args: Anything
        Return: Boolean
        """
        return uch.obj_in_list_always(self._ret_list(), obj)

    @property
    def args(self): #pylint: disable=invalid-name,missing-docstring
        return self._args_list()

    @property
    def kwargs(self): #pylint: disable=invalid-name,missing-docstring
        return self._kwargs_list()

    @property
    def exceptions(self): #pylint: disable=invalid-name,missing-docstring
        return self._error_list()

    @property
    def returnValues(self): #pylint: disable=invalid-name,missing-docstring
        return self._ret_list()

    def reset(self):
        """
        Reseting wrapped function
        """
        super(SinonSpy, self).unwrap()
        super(SinonSpy, self).wrap2spy()
