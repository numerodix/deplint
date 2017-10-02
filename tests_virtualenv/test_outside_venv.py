'''
Runs deplint against another project's venv.
'''

import os
import shutil
import sys

import pytest

from deplint.systools.process import invoke


class AppVirtualenv(object):
    def __init__(self, app_dirname, noisy=False):
        self.app_dirname = app_dirname
        self.noisy = noisy

        # /tests_virtualenv
        mydir = os.path.dirname(__file__)

        # /
        self.deplint_rootdir = os.path.dirname(mydir)

        # /tests_virtualenv/demoapp/
        self.app_rootdir = os.path.join(mydir, app_dirname)

        # /tests_virtualenv/demoapp/requirements.txt
        self.app_requirements_txt = os.path.join(self.app_rootdir, 'requirements.txt')

        # ve
        self.app_venv_dirname = 've'

        # /tests_virtualenv/demoapp/ve/
        self.app_venvdir = os.path.join(self.app_rootdir, self.app_venv_dirname)

        # /tests_virtualenv/demoapp/ve/python/
        self.app_venv_python = os.path.join(self.app_venvdir, 'bin', 'python')
        # /tests_virtualenv/demoapp/ve/pip/
        self.app_venv_pip = os.path.join(self.app_venvdir, 'bin', 'pip')

        # Snapshot the content in case we overwrite it later
        self.app_requirements_txt_orig_content = open(self.app_requirements_txt).read()

    def initialize(self):
        result = invoke(
            args=['virtualenv', self.app_venv_dirname],
            cwd=self.app_rootdir,
            noisy=self.noisy,
        )
        assert result.exit_code == 0

    def destroy(self):
        if os.path.exists(self.app_venvdir):
            shutil.rmtree(self.app_venvdir)

    def install_reqs(self):
        result = invoke(
            args=[self.app_venv_pip, 'install', '-r', self.app_requirements_txt],
            cwd=self.app_rootdir,
            noisy=True,
        )
        assert result.exit_code == 0

    def install_deplint(self):
        result = invoke(
            args=[self.app_venv_python, 'setup.py', 'install'],
            cwd=self.deplint_rootdir,
            noisy=True,
        )
        assert result.exit_code == 0

    def inject_installed_deplint_into_reqs(self):
        result = invoke(
            args=[self.app_venv_pip, 'freeze'],
            cwd=self.app_rootdir,
            noisy=True,
        )
        assert result.exit_code == 0

        deplint_req = None
        for line in result.stdout.splitlines():
            if line.startswith('deplint'):
                deplint_req = line
                break

        open(self.app_requirements_txt, 'a').write(line)

    def restore_app_reqs(self):
        open(self.app_requirements_txt, 'w').write(self.app_requirements_txt_orig_content)



@pytest.fixture(scope='session')
def demoapp_venv():
    venv = AppVirtualenv('demoapp_external', noisy=True)

    try:
        venv.initialize()
        venv.install_reqs()

        yield venv

    finally:
        venv.restore_app_reqs()
        venv.destroy()


def test_venv_external_app_works(demoapp_venv):
    result = invoke(
        args=[
            demoapp_venv.app_venv_python, 'app.py',
        ],
        cwd=demoapp_venv.app_rootdir,
        noisy=True
    )

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_venv_external_installed(demoapp_venv):
    result = invoke(
        args=[
            'bin/deplint', 'installed',
            '-r', demoapp_venv.app_requirements_txt,
            '--python', demoapp_venv.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == (
        "[RequiredInstalled] debug: "
        "Required dependency 'ansicolor==0.2.4' "
        "is satisfied by installed 'ansicolor-0.2.4'"
    )
    assert result.stderr == ''


def test_venv_external_tracked(demoapp_venv):
    # Clean bill of health
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', demoapp_venv.app_requirements_txt,
            '--python', demoapp_venv.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout == ''
    assert result.stderr == ''

    # Install something that is not required
    demoapp_venv.install_deplint()

    # Report unnecessary installed package
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', demoapp_venv.app_requirements_txt,
            '--python', demoapp_venv.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 1
    assert result.stdout.strip() == (
        "[IsTransitiveDep] warn: "
        "Installed non-transitive dependency 'deplint-0.0.1' is not required"
    )
    assert result.stderr == ''


def test_venv_external_unused(demoapp_venv):
    # Clean bill of health
    result = invoke(
        args=[
            'bin/deplint', 'unused',
            '-r', demoapp_venv.app_requirements_txt,
            '--python', demoapp_venv.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout == ''
    assert result.stderr == ''

    # Install and require something that is not used
    demoapp_venv.install_deplint()
    demoapp_venv.inject_installed_deplint_into_reqs()

    # Report requirement that is never used
    result = invoke(
        args=[
            'bin/deplint', 'unused',
            '-r', demoapp_venv.app_requirements_txt,
            '--python', demoapp_venv.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == (
        "[IsUnused] info: "
        "Required dependency 'deplint==0.0.1' "
        "is never imported (deplint)"
    )
    assert result.stderr == ''
