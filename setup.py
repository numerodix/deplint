import os

from setuptools import find_packages, setup

import deplint


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="deplint",
    version=deplint.__version__,
    author="Martin Matusiak",
    author_email="numerodix@gmail.com",
    description=("A linter for dependencies"),
    long_description=read('README.md'),
    license="Apache",
    keywords="requirements dependencies linter pip",
    url="https://github.com/numerodix/deplint",

    scripts=[
        "bin/deplint",
    ],
    packages=find_packages(
        where='.',
        exclude=[
            'tests*',
        ],
    ),

    # packages imported in the program
    install_requires=[
        'packaging',
        'safety',
        'six',
    ],
    # packages imported in the tests (not used, using tox instead)
    #  http://tox.readthedocs.io/en/latest/example/basic.html#integration-with-setup-py-test-command
    tests_require=[],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
    ],
)
