import sys
import re
from numbers import Number
from decimal import Decimal
from fractions import Fraction
from types import FunctionType, BuiltinFunctionType

from .util import ErrorHandler, Wrapper, CollectionHandler

python_version = sys.version_info[0]
if python_version == 3:
    unicode = str

class Matcher(object):

    def __init__(self, expectation, is_custom_func=False, is_substring=False, is_regex=False):
        self.message = ""
        self.expectation = expectation
        if is_custom_func:
            self.arg_type = "CUSTOMFUNC"
            setattr(Matcher, "test", staticmethod(expectation))
        elif is_substring:
            self.arg_type = "SUBSTRING"
        elif is_regex:
            self.arg_type = "REGEX"
        elif isinstance(expectation, type):
            self.arg_type = "TYPE"
        else:
            self.arg_type = "VALUE"

    def __str__(self):
        return self.message 

    def setMessage(self, message):
        self.message = message

    def setExpectation(self, expectation):
        self.expectation = expectation

    def test(self, target=None):
        if self.arg_type == "TYPE":
            return True if isinstance(target, self.expectation) else False
        elif self.arg_type == "SUBSTRING":
            return True if target in self.expectation else False
        elif self.arg_type == "REGEX":
            pattern = re.compile(self.expectation)
            return pattern.match(target)
        elif self.arg_type == "VALUE":
            if self.expectation == "__ANY__":
                return True
            elif self.expectation == "__DEFINED__":
                return True if target is not None else False
            elif self.expectation == "__NUMBER__":
                return True if isinstance(target, (Number, Decimal, Fraction)) else False
            elif self.expectation == "__STRING__":
                return True if isinstance(target, (str, unicode)) else False
            return True if target == self.expectation else False


original_matcher_test = Matcher.test

class SinonMatcher(object):

    def __new__(self, expectation=None, is_regex=False):
        if isinstance(expectation, FunctionType):
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
        Matcher.test = original_matcher_test

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

    @Wrapper.classproperty
    def number(cls):
        cls.m = Matcher("__NUMBER__")
        return cls.m

    @Wrapper.classproperty
    def string(cls):
        cls.m = Matcher("__STRING__")
        return cls.m

    @Wrapper.classproperty
    def object(cls):
        pass

    @Wrapper.classproperty
    def func(cls):
        cls.m = Matcher("__FUNC__")
        return cls.m

