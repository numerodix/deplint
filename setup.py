import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="reqlint",
    version="0.0.1",
    author="Martin Matusiak",
    author_email="numerodix@gmail.com",
    description=("A linter for requirements.txt"),
    license="MIT",
    keywords="requirements dependencies linter pip",
    # url="http://packages.python.org/an_example_pypi_project",
    scripts=[
        "bin/reqlinter",
    ],
    packages=find_packages(),
    install_requires=read('requirements.txt'),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        # "Topic :: Utilities",
        # "License :: OSI Approved :: MIt License",  # XXX
    ],
)
