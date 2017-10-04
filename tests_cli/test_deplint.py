'''
These tests run against the deplint project itself and aim to smoke test the
cli, nothing more.
'''

import sys

from deplint.systools.process import invoke


def test_run_missing_action():
    result = invoke(['bin/deplint'], noisy=True)

    assert result.exit_code == 2
    assert 'Traceback' not in result.stderr


def test_run_action_installed():
    result = invoke([
        'bin/deplint', 'installed',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ], noisy=True)

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_run_action_tracked():
    result = invoke([
        'bin/deplint', 'tracked',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ], noisy=True)

    # warning about dev dependencies being installed
    assert result.exit_code == 1
    assert 'Traceback' not in result.stderr


def test_run_action_upgrade():
    result = invoke([
        'bin/deplint', 'upgrade',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ], noisy=True)

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_run_action_unused():
    result = invoke([
        'bin/deplint', 'unused',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ], noisy=True)

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_run_action_vuln():
    result = invoke([
        'bin/deplint', 'vuln',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ], noisy=True)

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr
