from deplint.systools.process import invoke


class GitGrep(object):
    def __init__(self, basedir):
        self.basedir = basedir

    def as_display_name(self):
        return 'git grep'

    def package_is_imported(self, package_name):
        # Using git grep is a bit dubious because git grep only matches content
        # in the git index/history - not content in files on disk not yet
        # tracked by git. Still, as a grep it's extremely widely available.
        # A more robust method would be to have a fallback on another grep as
        # plan B.
        args = [
            'git', 'grep', '-E',
            (
                '^\s*'
                '(' +
                'import\s+' + package_name +
                '|from\s+' + package_name +
                ')'
            ),
        ]

        result = invoke(args, cwd=self.basedir)

        # code == 0 => found
        if result.exit_code == 0:
            return True

        # code 1 and no output => not found
        if result.exit_code == 1 and not any((result.stdout, result.stderr)):
            return False

        # code != 0 and output => error
        raise RuntimeError('git grep failed: %s' % result.stderr)
