import sys
import re
import inspect
from types import FunctionType, BuiltinFunctionType, MethodType

from .util import ErrorHandler, Wrapper, CollectionHandler

python_version = sys.version_info[0]
if python_version == 3:
    unicode = str

class Matcher(object):

    def __init__(self, expectation, is_custom_func=False, is_substring=False, is_regex=False, expected_type=None, expected_instance=None):
        self.message = ""
        self.another_matcher = None
        self.another_compare = None
        self.expectation = expectation
        self.expected_type = expected_type
        self.expected_instance = expected_instance
        if is_custom_func:
            self.arg_type = "CUSTOMFUNC"
            setattr(Matcher, "sinonMatcherTest", staticmethod(expectation))
        elif is_substring:
            self.arg_type = "SUBSTRING"
        elif is_regex:
            self.arg_type = "REGEX"
        elif isinstance(expectation, type):
            self.arg_type = "TYPE"
        else:
            self.arg_type = "VALUE"

    def sinonMatcherTest(self, target=None, checked=False):
        ret = False
        if self.arg_type == "TYPE":
            ret = True if isinstance(target, self.expectation) else False
        elif self.arg_type == "SUBSTRING":
            ret = True if target in self.expectation else False
        elif self.arg_type == "REGEX":
            pattern = re.compile(self.expectation)
            ret = pattern.match(target)
        elif self.arg_type == "VALUE":
            if self.expectation == "__ANY__":
                ret = True
            elif self.expectation == "__DEFINED__":
                ret = True if target is not None else False
            elif self.expectation == "__TYPE__":
                ret = True if type(target) == self.expected_type else False
            elif self.expectation == "__INSTANCE__":
                ret = True if isinstance(target, self.expected_instance.__class__) else False
            else:
                ret = True if target == self.expectation else False

        if self.another_matcher and not checked:
            ret2 = self.another_matcher.sinonMatcherTest(target, checked=True)

        if self.another_compare == "__AND__":
            return ret and ret2
        elif self.another_compare == "__OR__":
            return ret or ret2
        else:
            return ret

    def _and(self, another_matcher):
        self.another_compare = "__AND__"
        self.another_matcher = another_matcher
        return self

    def _or(self, another_matcher):
        self.another_compare = "__OR__"
        self.another_matcher = another_matcher
        return self


original_matcher_test = Matcher.sinonMatcherTest

class SinonMatcher(object):

    def __new__(self, expectation=None, is_regex=False):
        if isinstance(expectation, (FunctionType, BuiltinFunctionType, MethodType)):
            self.m = Matcher(expectation, is_custom_func=True)
        elif isinstance(expectation, (str, unicode)):
            if is_regex:
                self.m = Matcher(expectation, is_regex=True)
            else:
                self.m = Matcher(expectation, is_substring=True)
        else:
            self.m = Matcher(expectation)
        return self.m

    @classmethod
    def reset(cls):
        global original_matcher_test
        Matcher.sinonMatcherTest = original_matcher_test

    @Wrapper.classproperty
    def any(cls):
        cls.m = Matcher("__ANY__")
        return cls.m

    @Wrapper.classproperty
    def defined(cls):
        cls.m = Matcher("__DEFINED__")
        return cls.m

    @Wrapper.classproperty
    def truthy(cls):
        cls.m = Matcher(True)
        return cls.m

    @Wrapper.classproperty
    def falsy(cls):
        cls.m = Matcher(False)
        return cls.m

    @Wrapper.classproperty
    def bool(cls):
        cls.m = Matcher(bool)
        return cls.m

    @classmethod
    def same(cls, expectation):
        cls.m = Matcher(expectation)
        return cls.m

    @classmethod
    def typeOf(cls, expectation):
        if isinstance(expectation, type):
            cls.m = Matcher("__TYPE__", expected_type=expectation)
            return cls.m
        ErrorHandler.matcherTypeError(expectation)

    @classmethod
    def instanceOf(cls, expectation):
        if not inspect.isclass(expectation):
            cls.m = Matcher("__INSTANCE__", expected_instance=expectation)
            return cls.m
        ErrorHandler.matcherInstanceError(expectation)
