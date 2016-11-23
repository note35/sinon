import sys
sys.path.insert(0, '../')

from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler
from lib.sinon.SinonBase import SinonBase

class SinonStub(SinonBase):

    def __init__(self, obj=None, prop=None, func=None):
        super(SinonStub, self).__init__(obj, prop)
        super(SinonStub, self).addWrapStub(func)
