.. image:: https://badge.fury.io/py/sinon.svg
    :target: https://badge.fury.io/py/sinon
.. image:: https://travis-ci.org/note35/sinon.svg?branch=dev
    :alt: dev-branch-ci-status
    :target: https://travis-ci.org/note35/sinon
.. image:: https://coveralls.io/repos/github/note35/sinon/badge.svg
    :target: https://coveralls.io/github/note35/sinon


:Version: 0.0.4
:Download: http://pypi.python.org/pypi/sinon
:Source: https://github.com/note35/sinon
:Keywords: python, unittest, spy, stub, mock, sandbox, unittest2, pytest, sinon, doctest

.. contents::
    :local:

Sinon.py
========

Standalone and test framework agnostic Python test spies, stubs and
mocks (pronounced “sigh-non”).

Special Thanks
==============

This idea is inspired by `sinonjs`_ All the content is copied the idea
but rewriting in python.

.. _sinonjs: https://github.com/sinonjs/sinon

Progress
========

This project is still under developing.

The first release will include four basic features. The second release
have not planned yet.

Because the concept of closure in JS and Python are different, I plan to
skip all closure related functions.


*spy[80%]*
  excluding “JS-closure related function”

*stub[50%]*
  excluding “JS-closure related function”, lack callsArgs/yield feature

*mock[99%]*
  almost done (need more use cases to verify)

*sandbox[20%]*
  may ignore sandbox feature, only keep decorator

Installation
============

    pip install sinon

Usage
=====

    import sinon.sinon as sinon 

Spy
---

pass

Stub
----

pass

Mock
----

pass

Sandbox
-------

pass
