class ForTestOnly(object):

    def __init__(self):
        pass

    def func1(self, opt=None):
        if opt:
            return "func1+opt"
        return "func1"

    def func2(self, opt=None):
        if opt:
            return "func2+opt"
        return "func2"
