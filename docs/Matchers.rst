Matchers
========

Matchers allow the parameter to be either more vague or more specific about the expected value. Matchers can be passed as arguments to spy.called with the corresponding sinon.assert functions. *Generally, there is no need to use Matcher directly.*

=> stub.withArgs, spy.returned is not supported

.. _match-api-label:

Matcher API
-----------

**sinon.match(number)**

Requires the value to be == to the given number.

.. code-block:: python

    match_int = sinon.match(1)
    assert match_int.mtest(1)

**sinon.match(string, strcmp="substring")**

Requires the value to be a string and have the expectation as a substring,

.. code-block:: python

    match_substr = sinon.match("a long string", strcmp="substring")
    assert match_substr.mtest("str")

**sinon.match(regex, strcmp="regex")**

Requires the value to be a string and match the given regular expression.

.. code-block:: python

    match_substr = sinon.match("(\d*)-(\d*)", strcmp="regex")
    assert match_substr.mtest("0000-0000")

**sinon.match(function, is_custom_func=True)**

See :ref:`custom-matcher-label`.

**sinon.match(ref)**

For anything that does not belong to the above, the argument will be processed as a value (usually, using sinon.match.same to compare).

.. code-block:: python

    match_int = sinon.match(int)
    assert match_int.mtest(1)
    match_str = sinon.match(str)
    assert match_str.mtest("str")

**sinon.match.any**

Matches anything.

.. code-block:: python

    match_any = sinon.match.any
    assert match_any.mtest(None)
    assert match_any.mtest(123)
    assert match_any.mtest("123")
    assert match_any.mtest(os)
    assert match_any.mtest(os.system)

**sinon.match.defined**

Requires the value which is not None.

.. code-block:: python

    match_defined = sinon.match.defined
    assert not match_defined.mtest(None)
    assert match_defined.mtest([])
    assert match_defined.mtest(1)

**sinon.match.truthy**

Requires the value to be truthy.

.. code-block:: python

    match_truthy = sinon.match.truthy
    assert match_truthy.mtest(True)
    assert match_truthy.mtest(1)
    assert not match_truthy.mtest(False)
    assert not match_truthy.mtest(0)

**sinon.match.falsy**

Requires the value to be falsy.

.. code-block:: python

    match_falsy = sinon.match.falsy
    assert not match_falsy.mtest(True)
    assert not match_falsy.mtest(1)
    assert match_falsy.mtest(False)
    assert match_falsy.mtest(0)

**sinon.match.bool**

Requires the value to be a boolean.

.. code-block:: python

    match_bool = sinon.match.bool
    assert match_bool.mtest(True)
    assert not match_bool.mtest(1)
    assert match_bool.mtest(False)
    assert not match_bool.mtest(0)

**sinon.match.same(ref)**

Requires the value to strictly equal ref.

**sinon.match.typeOf(type)**

Requires the value to be a type of the given type.

.. code-block:: python

    match_type = sinon.match.typeOf(int)
    assert match_type.mtest(1)
    assert not match_type.mtest(True)

**sinon.match.instanceOf(instance)**

Requires the value to be an instance of the given instance.

.. code-block:: python

    spy = sinon.spy()
    stub = sinon.stub()
    match_inst = sinon.match.instanceOf(spy)
    assert match_inst.mtest(stub) #True because stub inherits spy

Combining matchers
------------------

All matchers implement `and` and `or`. This allows to logically combine two matchers. The result is a new matcher that requires both (and) or one of the matchers (or) to return true.

**and_match(another_matcher)**

.. code-block:: python

    spy = sinon.spy()
    stub = sinon.stub()
    expectation = sinon.mock(os).expects("system")
    match_and = sinon.match.instanceOf(spy).and_match(sinon.match.instanceOf(stub))
    assert match_and.mtest(expectation) #True because expectation inherits spy and stub

**or_match(another_matcher)**

.. code-block:: python

    match_or = sinon.match(int).or_match(sinon.match(str))
    assert match_or.mtest(1)
    assert match_or.mtest("1")

.. _custom-matcher-label:

Custom matchers
---------------

Custom matchers are created with the `sinon.match` factory which takes a test. The test function takes a value as the only argument, returns `true` if the value matches the expectation and `false` otherwise.

.. code-block:: python

    def equal_to_square(give_value, expected_value):
        return True if give_value**2 == expected_value else False

    match_custom = sinon.match(equal_to_square, is_custom_func=True)
    assert not match_custom.mtest(6, 49)
    assert match_custom.mtest(6, 36)
