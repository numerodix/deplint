import contextlib
import os
import shutil
import tempfile

import pytest

from deplint.data_sources.source_code.git_grep import GitGrep
from deplint.systools.process import invoke


@contextlib.contextmanager
def dummy_project(pkg, variant, git_init=True):
    direc = tempfile.mkdtemp(prefix='.deplint.tests-')

    # top level imports
    if variant == 'import-x':
        code = 'import %s' % pkg
    elif variant == 'import-x.y':
        code = 'import %s.hammer' % pkg

    elif variant == 'from-x-import-y':
        code = 'from %s import hammer' % pkg
    elif variant == 'from-x.y-import-z':
        code = 'from %s.hammer import rabbit' % pkg

    # nested imports
    elif variant == 'import-y.x':
        code = 'import hammer.%s' % pkg

    elif variant == 'from-y.x-import-z':
        code = 'from hammer.%s import rabbit' % pkg

    elif variant == 'from-y.z-import-x':
        code = 'from hammer.rabbit import %s' % pkg

    fd, file = tempfile.mkstemp(dir=direc, suffix='.py')
    os.write(fd, b'%s\n' % code.encode('utf-8'))
    os.close(fd)

    # create a git repo there and add the file - otherwise git grep won't work
    git_result = invoke(['git', 'init'], cwd=direc)
    assert git_result.exit_code == 0
    git_result = invoke(['git', 'add', '.'], cwd=direc)
    assert git_result.exit_code == 0

    try:
        yield direc

    finally:
        if os.path.exists(direc):
            shutil.rmtree(direc)


def test_git_grep_as_display_name():
    git_grep = GitGrep(basedir=None)
    assert git_grep.as_display_name() == 'git grep'


def test_git_grep_imports_top_level():
    with dummy_project(pkg='ply', variant='import-x') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is True

    with dummy_project(pkg='ply', variant='import-x.y') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is True


    with dummy_project(pkg='ply', variant='from-x-import-y') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is True

    with dummy_project(pkg='ply', variant='from-x.y-import-z') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is True


def test_git_grep_imports_nested():
    with dummy_project(pkg='ply', variant='import-y.x') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is False

    with dummy_project(pkg='ply', variant='from-y.x-import-z') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is False

    with dummy_project(pkg='ply', variant='from-y.z-import-x') as direc:
        git_grep = GitGrep(basedir=direc)
        assert git_grep.package_is_imported('ply') is False


def test_git_grep_not_a_repo():
    git_grep = GitGrep(basedir='/')

    with dummy_project(pkg='ply', variant='from-y.z-import-x', git_init=False):
        # can't run in a dir that isn't a git repo
        with pytest.raises(RuntimeError):
            git_grep.package_is_imported('ply')
