from .lib import SinonBase, SinonSpy, SinonStub, SinonMock, SinonSandbox

init = SinonBase.init
test = SinonSandbox.sinontest
stub = SinonStub.SinonStub
spy = SinonSpy.SinonSpy
mock = SinonMock.SinonMock
