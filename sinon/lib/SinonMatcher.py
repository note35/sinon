"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
"""
import sys
import re
import inspect
from types import FunctionType, BuiltinFunctionType, MethodType

from .util import ErrorHandler, Wrapper

# compatible with python2.x
if sys.version_info[0] == 3:
    unicode = str #pylint: disable=invalid-name

class Matcher(object):
    """
    For various comparision, matcher provides different methods
    """

    def __get_type(self, expectation, options):
        """
        Determining the type of Matcher
        Return: string
        """
        if "is_custom_func" in options.keys():
            setattr(self, "mtest", expectation)
            return "CUSTOMFUNC"
        elif "is_substring" in options.keys():
            return "SUBSTRING"
        elif "is_regex" in options.keys():
            return "REGEX"
        elif isinstance(expectation, type):
            return "TYPE"
        else:
            return "VALUE"

    def __init__(self, expectation, options=None):
        if not options:
            options = {}
        self.another_matcher, self.another_compare = None, None
        self.expectation = expectation
        self.target_type = options["target_type"] if "target_type" in options.keys() else None
        self.arg_type = self.__get_type(expectation, options)

    def __value_compare(self, target):
        """
        Comparing result based on expectation if arg_type is "VALUE"
        Args: Anything
        Return: Boolean
        """
        if self.expectation == "__ANY__":
            return True
        elif self.expectation == "__DEFINED__":
            return True if target is not None else False
        elif self.expectation == "__TYPE__":
            return True if type(target) == self.target_type else False #pylint:disable=unidiomatic-typecheck
        elif self.expectation == "__INSTANCE__":
            return True if isinstance(target, self.target_type.__class__) else False
        else:
            return True if target == self.expectation else False

    def __get_test_return(self, target):
        """
        Getting different comparsions based on arg_type
        """
        if self.arg_type == "SUBSTRING":
            return True if target in self.expectation else False
        elif self.arg_type == "REGEX":
            pattern = re.compile(self.expectation)
            return pattern.match(target)
        elif self.arg_type == "TYPE":
            return True if isinstance(target, self.expectation) else False
        elif self.arg_type == "VALUE":
            return self.__value_compare(target)

    def __get_match_result(self, ret, ret2):
        """
        Getting match result
        """
        if self.another_compare == "__MATCH_AND__":
            return ret and ret2
        elif self.another_compare == "__MATCH_OR__":
            return ret or ret2
        return ret

    def __matcher_test(self, target, checked):
        """
        Internal function of mtest
        """
        ret = self.__get_test_return(target)
        ret2 = False
        if self.another_matcher and not checked:
            ret2 = self.another_matcher.mtest(target, checked=True)
        return self.__get_match_result(ret, ret2)

    def mtest(self, target=None, checked=False):
        """
        Comparing target and expectation of Matcher
        Args:
            Anything (target)
            Boolean (checked or not, default is not)
        Return:
            Boolean (Return of __matcher_test -> __get_match_result)
        """
        return self.__matcher_test(target, checked)

    def and_match(self, another_matcher):
        """
        Adding one additional matching condition (max is 2) for AND comparsion
        mtest must match to original matcher AND this new matcher
        Args: Matcher
        Return: self
        """
        self.another_compare = "__MATCH_AND__"
        self.another_matcher = another_matcher
        return self

    def or_match(self, another_matcher):
        """
        Adding one additional matching condition (max is 2) for OR comparsion
        mtest only need to match to original matcher OR this new matcher
        Args: Matcher
        Return: self
        """
        self.another_compare = "__MATCH_OR__"
        self.another_matcher = another_matcher
        return self


class SinonMatcher(object):
    """
    SinonMatcher is an external interface of Matcher
    """
    def __new__(cls, expectation=None, strcmp=None, is_custom_func=False):
        """
        Args:
            anything (expectation: the object you want to compare)
            "substring", "regex" (strcmp: the type of string comparsion)
            Boolean (is_custom_func: set True is object is a test function of Matcher
        Return:
            Matcher
        """
        options = {}
        if is_custom_func:
            if isinstance(expectation, (FunctionType, BuiltinFunctionType, MethodType)):
                options["is_custom_func"] = True
            else:
                # Todo: customized error exception
                raise TypeError("[{}] is not callable".format(expectation))
        if strcmp:
            if isinstance(expectation, (str, unicode)):
                if strcmp.upper() == "DEFAULT" or strcmp.upper() == "SUBSTRING":
                    options["is_substring"] = True
                elif strcmp.upper() == "REGEX":
                    options["is_regex"] = True
            else:
                raise TypeError("[{}] is not a string".format(expectation))
        return Matcher(expectation, options)

    @Wrapper.classproperty
    def any(cls): #pylint: disable=no-self-argument,no-self-use
        """
        Matcher.mtest(...) will always return True
        Return: Matcher
        """
        return Matcher("__ANY__")

    @Wrapper.classproperty
    def defined(cls): #pylint: disable=no-self-argument,no-self-use
        """
        Matcher.mtest(...) will return True if ... is defined
        Return: Matcher
        """
        return Matcher("__DEFINED__")

    @Wrapper.classproperty
    def truthy(cls): #pylint: disable=no-self-argument,no-self-use
        """
        Matcher.mtest(...) will return True if ... is True
        Return: Matcher
        """
        return Matcher(True)

    @Wrapper.classproperty
    def falsy(cls): #pylint: disable=no-self-argument,no-self-use
        """
        Matcher.mtest(...) will return False if ... is True
        Return: Matcher
        """
        return Matcher(False)

    @Wrapper.classproperty
    def bool(cls): #pylint: disable=no-self-argument,no-self-use
        """
        Matcher.mtest(...) will return True if ... is True
        Return: Matcher
        """
        return Matcher(bool)

    @classmethod
    def same(cls, expectation): #pylint: disable=no-self-argument,no-self-use
        """
        Matcher.mtest(...) will return True if ... == expectation
        Return: Matcher
        """
        return Matcher(expectation)

    @classmethod
    def typeOf(cls, expected_type): #pylint: disable=no-self-argument,invalid-name,no-self-use
        """
        (*Type does NOT consider inherited class)
        Matcher.mtest(...) will return True if type(...) == expected_type
        Return: Matcher
        Raise: matcher_type_error
        """
        if isinstance(expected_type, type):
            options = {}
            options["target_type"] = expected_type
            return Matcher("__TYPE__", options)
        ErrorHandler.matcher_type_error(expected_type)

    @classmethod
    def instanceOf(cls, expected_instance): #pylint: disable=no-self-argument,invalid-name,no-self-use
        """
        (*Instance consider inherited class)
        Matcher.mtest(...) will return True if instance(...) == expected_instance
        Return: Matcher
        Raise: matcher_instance_error
        """
        if not inspect.isclass(expected_instance):
            options = {}
            options["target_type"] = expected_instance
            return Matcher("__INSTANCE__", options)
        ErrorHandler.matcher_instance_error(expected_instance)
