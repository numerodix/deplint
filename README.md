deplint - Dependency linter
===========================

At the top of the file there should be a short introduction and/ or overview
that explains **what** the project is. This description should match
descriptions added for package managers (Gemspec, package.json, etc.). To
ensure that the project properly displays on the [open source project
listing](http://atlassian.bitbucket.org/), you should also do the following:

1. the project description that is displayed is pulled from the *Repository
   details: Description* within the repo *Settings*
2. the *Repository details: Language* should be specified within the repo
   *Settings*

Optionally, include a short description of the motivation behind the creation
and maintenance of the project. This should explain **why** the project exists.

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

Installation
============

Install from PyPI using:

    $ pip install deplint

Documentation
=============

Depending on the size of the project, if it is small and simple enough the
reference docs can be added to the README. For medium size to larger projects
it is important to at least provide a link to where the docs or API reference
live.

Tests
=====

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
