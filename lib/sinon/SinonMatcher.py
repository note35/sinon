import sys
sys.path.insert(0, '../')
from types import ModuleType, FunctionType

class Matcher(object):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SinonMatcher(object):

    def __init__(self, expectation, message):
        m = create(matcher);
        type = typeOf(expectation);


    def typeOf(self, type):
        def compare(value):
            return isinstance(typeOf(value), type)
        if type and (isinstance(type, str) or isinstance(type, unicode)):
            return self(compare, "typeOf(\"" + type + "\")"
       

    @classmethod
    @property
    def bool(self):
        return self.typeOf("boolean");
