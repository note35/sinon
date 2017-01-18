from .lib import SinonBase, SinonSpy, SinonStub, SinonMock, SinonSandbox, SinonAssertion, SinonMatcher 

init = SinonBase.init
test = SinonSandbox.sinontest
stub = SinonStub.SinonStub
spy = SinonSpy.SinonSpy
mock = SinonMock.SinonMock
assertion = SinonAssertion.SinonAssertion
match = SinonMatcher.SinonMatcher
