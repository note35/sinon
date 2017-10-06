'''
Copyright (c) 2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

Author(s): Jonathan Benn
'''

class SpyCall(object):
    """
    Holds data and test functions related to a single function call
    """

    def __init__(self):
        """
        Constructor
        """
        self.args = []
        self.kwargs = []
        self.callId = -1
        self.exception = None
        self.proxy = None
        self.returnValue = None
        self.stack = None
