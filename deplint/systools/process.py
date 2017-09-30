import subprocess


class InvokeResult(object):
    def __init__(self, exit_code, stdout, stderr):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


def invoke(args, cwd=None, noisy=False):
    cwd = cwd or '.'

    if noisy:
        print("{invoke} Invoking: %s" % ' '.join(args))

    proc = subprocess.Popen(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    result = InvokeResult(
        exit_code=proc.returncode,
        stdout=stdout,
        stderr=stderr,
    )

    if noisy:
        print("{invoke} Returned: exit_code %s" % result.exit_code)
        print("{invoke} stdout: %s" % result.stdout)
        print("{invoke} stderr: %s" % result.stderr)

    return result
