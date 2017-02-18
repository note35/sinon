try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name = 'sinon',
  version = '0.1.0',
  author = 'Kir Chou',
  author_email = 'note351@hotmail.com',
  packages = ['sinon', 'sinon.lib', 'sinon.lib.util'],
  url = 'https://github.com/note35/sinon',
  license='LICENSE.txt',
  description = 'Standalone and test framework agnostic Python test spies, stubs and mocks (pronounced "sigh-non"). ',
  long_description=open('README.rst').read(),
  download_url = 'https://github.com/note35/sinon/archive/master.zip',
  keywords = ['unittest', 'spy', 'stub', 'mock', 'unittest2', 'pytest', 'sinon'], 
  classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: BSD License",
    "Intended Audience :: Developers",
    "Operating System :: POSIX",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Testing",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Natural Language :: English",
  ],
)
