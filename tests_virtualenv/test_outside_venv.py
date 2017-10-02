'''
Runs deplint against another project's venv from the outside.
'''

from deplint.systools.process import invoke
import deplint


def test_venv_external_app_works(appvenv_ext):
    result = invoke(
        args=[
            appvenv_ext.app_venv_python, 'app.py',
        ],
        cwd=appvenv_ext.app_rootdir,
        noisy=True
    )

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_venv_external_installed(appvenv_ext):
    result = invoke(
        args=[
            'bin/deplint', 'installed',
            '-r', appvenv_ext.app_requirements_txt,
            '--python', appvenv_ext.app_venv_python,
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


def test_venv_external_tracked(appvenv_ext):
    # Clean bill of health
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', appvenv_ext.app_requirements_txt,
            '--python', appvenv_ext.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout == ''
    assert result.stderr == ''

    # Install something that is not required
    appvenv_ext.install_deplint()

    # Report unnecessary installed package
    result = invoke(
        args=[
            'bin/deplint', 'tracked',
            '-r', appvenv_ext.app_requirements_txt,
            '--python', appvenv_ext.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 1
    assert result.stdout.strip() == (
        "[IsTransitiveDep] warn: "
        "Installed non-transitive dependency 'deplint-%s' is not required"
    ) % (deplint.__version__,)
    assert result.stderr == ''


def test_venv_external_unused(appvenv_ext):
    # Clean bill of health
    result = invoke(
        args=[
            'bin/deplint', 'unused',
            '-r', appvenv_ext.app_requirements_txt,
            '--python', appvenv_ext.app_venv_python,
        ],
        noisy=True
    )

    assert result.exit_code == 0
    assert result.stdout == ''
    assert result.stderr == ''

    # Install and require something that is not used
    appvenv_ext.install_deplint()
    appvenv_ext.inject_installed_deplint_into_reqs()

    # Report requirement that is never used
    result = invoke(
        args=[
            'bin/deplint', 'unused',
            '-r', appvenv_ext.app_requirements_txt,
            '--python', appvenv_ext.app_venv_python,
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
