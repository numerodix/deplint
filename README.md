deplint - Dependency linter
===========================

Managing dependencies in Python medium/large projects tends to be tedious and
imperfect. Projects tend to adopt one of two conventions:

* List only top level dependencies in `requirements.txt` (either locked to a
  specific version, or left completely free with respect to version) and leave
  transitive dependencies unspecified. This can lead to problems of
  reproducibility when transitive dependencies change in unexpected ways.

* List the full dependency closure including exact versions for the whole
  dependency closure, ie. `pip freeze > requirements.txt`. This destroys the
  distinction between what is an intended (ie. top level) dependency and what
  is a by-product (a transitive dependency). Projects managed this way make it
  hard to know which dependencies are used, and for what. It makes it very
  tedious to review all dependencies to see if they can be updated, to see if
  they can be removed safely etc.

deplint collects information from a number of different sources:

* Your required dependencies (ie. the contents of your `requirements.txt`).

* Your installed dependencies (ie. what's in `pip freeze`).

* Package metadata from your virtualenv `site-packages`.

* Packages available in the package index (via `pip search`).

* Your source code (import statements).

Based on this it can advise you on your dependencies in a way that you could
do yourself manually, but it automates away the mechanical work.



Usage
======

deplint supports two modes of operation:

* Install it in your project's virtualenv and run it from within that
  virtualenv. You won't have to specify any paths on disk - deplint will infer
  them.

* Install it system wide and run it against multiple different project's
  virtualenvs. In this case you'll need to specify paths.

From inside your project's virtualenv:

```bash
$ deplint installed
```

Installed system wide, running against your project's virtualenv:

```bash
$ deplint installed \
    -r ~/src/project/requirements.txt \
    -p ~/.virtualenvs/project/bin/python
```


Examining installed dependencies
--------------------------------

Example:

```bash
$ deplint installed
[RequiredInstalled] debug: Required dependency 'packaging==16.8' is satisfied by installed 'packaging-16.8'
[RequiredInstalled] debug: Required dependency 'safety==1.5.1' is satisfied by installed 'safety-1.5.1'
[RequiredInstalled] debug: Required dependency 'six==1.11.0' is satisfied by installed 'six-1.11.0'
```

deplint examines your requirements and checks whether all of the dependencies
are installed and satisfy the requirements. Any discrepancies here should be
fixable using a simple `pip install -r requirements.txt`.


Examining tracked dependencies
------------------------------

Example:

```bash
$ deplint tracked
[IsTransitiveDep] warn: Installed non-transitive dependency 'flake8-3.4.1' is not required
[IsTransitiveDep] warn: Installed non-transitive dependency 'ipdb-0.10.3' is not required
[IsTransitiveDep] warn: Installed non-transitive dependency 'isort-4.2.15' is not required
[IsTransitiveDep] info: Required dependency 'packaging==16.8' is a transitive dependency of 'safety==1.5.1'
[IsTransitiveDep] warn: Installed non-transitive dependency 'pytest-cov-2.5.1' is not required
[IsTransitiveDep] info: Required dependency 'six==1.11.0' is a transitive dependency of 'safety==1.5.1'
[IsTransitiveDep] warn: Installed non-transitive dependency 'tox-2.8.2' is not required
```

deplint discovers the dependency relationship between packages based on
metadata in your virtualenv's `site-packages`. From this it will tell you
about:

* Packages that are installed but not required (and also not a transitive
  dependency of a required package). This could mean you installed something
  that is not needed, or that you installed something that should be a
  requirement, but you haven't included it in `requirements.txt` yet.

* Packages that are transitive dependencies (ie. implied by another
  dependency). This is a hint that perhaps they don't need to be a requirement
  (but it's up to you to decide that).


Examining unused dependencies
-----------------------------

Example:

```bash
$ deplint unused
[IsUnused] info: Required dependency 'Unidecode==0.04.21' is never imported (unidecode)
```

deplint will scan your source code for import statements. If your project
requires a specific package, but that package is never imported by your code
then you will see this here. This could mean the package is a command line tool
like `flake8` or `tox` that is often installed but not imported in code. If
not, it could mean that you do not need this requirement anymore (perhaps it
was used in earlier versions of the code?).


Examining upgradeable dependencies
----------------------------------

Example:

```bash
$ deplint upgrade
[CanBeUpgraded] info: Required dependency 'botocore==1.7.13' can be upgraded to 'botocore-1.7.28'
[CanBeUpgraded] info: Required dependency 'cryptography==2.0.3' can be upgraded to 'cryptography-2.1.1'
```

deplint can tell you two things here:

* If you have a requirement of the form `project<4.0`, your installed version
  is `project-3.1` and there is a `project-3.2` version available, it will be
  suggested to you as an update.

* If you have a requirement of the form `project==4.0` and there is a
  `project-4.1` version available, it will be suggested to you as an upgrade.


Examining vulnerable dependencies
---------------------------------

Example:

```bash
$ deplint vulnerable
[IsVulnerable] warn: Installed dependency 'tornado-2.2' has a known vulnerability in 'tornado<2.2.1'
    CRLF injection vulnerability in the tornado.web.RequestHandler.set_header function in Tornado before 2.2.1 allows remote attackers to inject arbitrary HTTP headers and conduct HTTP response splitting attacks via crafted input.
```

deplint will check if any of your installed dependencies have known
vulnerabilities in their installed versions.



Installation
============

Install from PyPI using:

    $ pip install deplint



Running tests
=============

There are several test suites:

* Unit tests. Run with `./test` or `./test_with_coverage` to see code coverage.

* Integration tests of the cli by running deplint on its own source code. Run
  with `./test_cli`.

* Integration tests of the cli by running deplint against another project, both
inside-virtualenv and outside-virtualenv. Run with: `./test_virtualenv`

* Testing against multiple Python versions using tox. Run with: `./test_with_tox`

Please note that the goal is to maintain near-100% test coverage through unit
tests and also have thorough integration testing in place at all times.



Contributors
============

Pull requests, issues and comments welcome. For pull requests:

* Add tests for new features and bug fixes
* Follow the existing style
* Separate unrelated changes into multiple pull requests

See the existing issues for things to start contributing.

For bigger changes, make sure you start a discussion first by creating an issue
and explaining the intended change.

Atlassian requires contributors to sign a Contributor License Agreement, known
as a CLA. This serves as a record stating that the contributor is entitled to
contribute the code/documentation/translation to the project and is willing to
have it used in distributions and derivative works (or is willing to transfer
ownership).

Prior to accepting your contributions we ask that you please follow the
appropriate link below to digitally sign the CLA. The Corporate CLA is for
those who are contributing as a member of an organization and the individual
CLA is for those contributing as an individual.

* [CLA for corporate contributors](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=e1c17c66-ca4d-4aab-a953-2c231af4a20b)
* [CLA for individuals](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=3f94fbdc-2fbe-46ac-b14c-5d152700ae5d)



License
========

Copyright (c) 2017 Atlassian and others.
Apache 2.0 licensed, see [LICENSE.txt](LICENSE.txt) file.
