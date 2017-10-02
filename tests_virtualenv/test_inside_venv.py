'''
Runs deplint inside another project's venv.
'''

import deplint
from deplint.systools.process import invoke


def test_venv_internal_app_works(appvenv_int):
    result = invoke(
        args=[
            appvenv_int.app_venv_python, 'app.py',
        ],
        cwd=appvenv_int.app_rootdir,
        noisy=True
    )

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_venv_internal_installed(appvenv_int):
    result = invoke(
        args=[
            'bin/deplint', 'installed',
            '-r', appvenv_int.app_requirements_txt,
            '--python', appvenv_int.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == '\n'.join([
        (
            "[RequiredInstalled] debug: "
            "Required dependency 'ansicolor==0.2.4' "
            "is satisfied by installed 'ansicolor-0.2.4'"
        ),
        (
            "[RequiredInstalled] debug: "
            "Required dependency 'deplint==%s' "
            "is satisfied by installed 'deplint-%s'"
        ) % (deplint.__version__, deplint.__version__),
    ])
    assert result.stderr == ''


def test_venv_internal_tracked(appvenv_int):
    # Clean bill of health
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', appvenv_int.app_requirements_txt,
            '--python', appvenv_int.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout == ''
    assert result.stderr == ''

    # Install something that is not required
    appvenv_int.install_pypi_package('pytest==3.2.2')

    # Report unnecessary installed package
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', appvenv_int.app_requirements_txt,
            '--python', appvenv_int.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 1
    assert result.stdout.strip() == (
        "[IsTransitiveDep] warn: "
        "Installed non-transitive dependency 'pytest-3.2.2' is not required"
    )
    assert result.stderr == ''


def test_venv_internal_unused(appvenv_int):
    # Report requirement that is never used
    result = invoke(
        args=[
            'bin/deplint', 'unused',
            '-r', appvenv_int.app_requirements_txt,
            '--python', appvenv_int.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == (
        "[IsUnused] info: "
        "Required dependency 'deplint==%s' "
        "is never imported (deplint)"
    ) % (deplint.__version__,)
    assert result.stderr == ''
