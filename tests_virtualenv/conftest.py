import os
import shutil

import pytest

from deplint.systools.process import invoke


class AppVirtualenv(object):
    '''
    Represents a virtualenv for demoapp.
    '''

    def __init__(self, app_dirname, venv_dirname='ve', noisy=False):
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
        self.app_venv_dirname = venv_dirname

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

    def install_pypi_package(self, pkg):
        result = invoke(
            args=[self.app_venv_pip, 'install', pkg],
            cwd=self.app_rootdir,
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

        for line in result.stdout.splitlines():
            if line.startswith('deplint'):
                break

        open(self.app_requirements_txt, 'a').write(line)

    def restore_app_reqs(self):
        open(self.app_requirements_txt, 'w').write(self.app_requirements_txt_orig_content)


@pytest.fixture(scope='module')
def appvenv_int():
    '''
    A virtualenv for demoapp with deplint being used from inside (installed in
    the app's virtualenv).
    '''

    venv = AppVirtualenv('demoapp', venv_dirname='ve-int', noisy=True)

    try:
        venv.initialize()
        venv.install_reqs()
        venv.install_deplint()
        venv.inject_installed_deplint_into_reqs()

        yield venv

    finally:
        venv.restore_app_reqs()
        venv.destroy()


@pytest.fixture(scope='module')
def appvenv_ext():
    '''
    A virtualenv for demoapp with deplint being used from outside (not
    installed in the app's virtualenv).
    '''

    venv = AppVirtualenv('demoapp', venv_dirname='ve-ext', noisy=True)

    try:
        venv.initialize()
        venv.install_reqs()

        yield venv

    finally:
        venv.restore_app_reqs()
        venv.destroy()
