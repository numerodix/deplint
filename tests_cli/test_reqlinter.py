from collections import namedtuple
import subprocess
import sys


InvokeResult = namedtuple('InvokeResult', ['exit_code', 'stdout', 'stderr'])

def invoke(args):
    print("{invoke} Invoking: %s" % ' '.join(args))

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    result = InvokeResult(
        exit_code=proc.returncode,
        stdout=stdout,
        stderr=stderr,
    )

    print("{invoke} Returned: exit_code %s" % result.exit_code)
    print("{invoke} stdout: %s" % result.stdout)
    print("{invoke} stderr: %s" % result.stderr)

    return result


def test_run_missing_action():
    result = invoke(['bin/reqlinter'])

    assert result.exit_code == 2
    assert 'Traceback' not in result.stderr


def test_run_action_installed():
    result = invoke([
        'bin/reqlinter', 'installed',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ])

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_run_action_tracked():
    result = invoke([
        'bin/reqlinter', 'tracked',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ])

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr


def test_run_action_upgrade():
    result = invoke([
        'bin/reqlinter', 'upgrade',
        '-r', 'requirements.txt',
        '--python', sys.executable,
        '-v',
    ])

    assert result.exit_code == 0
    assert 'Traceback' not in result.stderr
