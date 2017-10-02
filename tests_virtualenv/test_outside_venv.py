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

        # ve
        self.app_venv_dirname = 've'

        # /tests_virtualenv/demoapp/ve/
        self.app_venvdir = os.path.join(self.app_rootdir, self.app_venv_dirname)

        # /tests_virtualenv/demoapp/ve/python/
        self.app_venv_python = os.path.join(self.app_venvdir, 'bin', 'python')
        # /tests_virtualenv/demoapp/ve/pip/
        self.app_venv_pip = os.path.join(self.app_venvdir, 'bin', 'pip')

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
            args=[self.app_venv_pip, 'install', '-r', 'requirements.txt'],
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


@pytest.fixture(scope='session')
def demoapp_venv():
    venv = AppVirtualenv('demoapp_external', noisy=True)

    try:
        venv.initialize()
        venv.install_reqs()

        yield venv

    finally:
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
            '-r', os.path.join(demoapp_venv.app_rootdir, 'requirements.txt'),
            '--python', demoapp_venv.app_venv_python,
            '-v',
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_venv_external_tracked(demoapp_venv):
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', os.path.join(demoapp_venv.app_rootdir, 'requirements.txt'),
            '--python', demoapp_venv.app_venv_python,
            '-v',
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_venv_external_unused(demoapp_venv):
    result = invoke(
        args=[
            'bin/deplint', 'unused',
            '-r', os.path.join(demoapp_venv.app_rootdir, 'requirements.txt'),
            '--python', demoapp_venv.app_venv_python,
            '-v',
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr
