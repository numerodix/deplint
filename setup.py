import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="deplint",
    version="0.0.1",
    author="Martin Matusiak",
    author_email="numerodix@gmail.com",
    description=("A linter for dependencies"),
    long_description=read('README.rst'),
    license="MIT",
    keywords="requirements dependencies linter pip",
    # url="http://packages.python.org/an_example_pypi_project",

    scripts=[
        "bin/deplint",
    ],
    packages=find_packages(),

    # packages imported in the program
    install_requires=[
        'packaging',
        'six',
    ],
    # packages imported in the tests (not used, using tox instead)
    #  http://tox.readthedocs.io/en/latest/example/basic.html#integration-with-setup-py-test-command
    tests_require=[],

    classifiers=[
        "Development Status :: 3 - Alpha",
        # "Topic :: Utilities",
        # "License :: OSI Approved :: MIt License",  # XXX
    ],
)
