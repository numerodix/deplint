from deplint.systools.process import invoke


def test_invoke():
    result = invoke(['echo', 'hello'])

    assert result.exit_code == 0
    assert result.stdout == 'hello\n'
    assert result.stderr == ''


def test_invoke_noisy(capsys):
    result = invoke(['echo', 'hello'], cwd='/tmp', noisy=True)

    assert result.exit_code == 0
    assert result.stdout == 'hello\n'
    assert result.stderr == ''

    stdout, stderr = capsys.readouterr()
    assert stdout.strip() == '\n'.join([
        '{invoke} [cwd: /tmp] Invoking: echo hello',
        '{invoke} Returned: exit_code 0',
        '{invoke} stdout: hello\n',
        '{invoke} stderr:',
    ])
    assert stderr == ''
