"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
"""
from .lib import base, spy, stub, mock, sandbox, assertion, matcher 

init = base.init
test = sandbox.sinontest
stub = stub.SinonStub
spy = spy.SinonSpy
mock = mock.SinonMock
assertion = assertion.SinonAssertion
match = matcher.SinonMatcher
