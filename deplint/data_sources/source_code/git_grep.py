from deplint.systools.process import invoke


class GitGrep(object):
    def __init__(self, basedir):
        self.basedir = basedir

    def package_is_imported(self, package_name):
        args = [
            'git', 'grep', '-E',
            'import\s+' + package_name + '|from\s+' + package_name,
        ]

        result = invoke(args, cwd=self.basedir)

        if result.exit_code == 1 and not any((result.stdout, result.stderr)):
            return False

        return True
