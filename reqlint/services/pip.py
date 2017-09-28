import logging
import re
import subprocess

from reqlint.model.package_releases import PackageReleases


_logger = logging.getLogger(__name__)


class Pip(object):
    pattern_name = '[A-Za-z0-9-_.]+'
    pattern_version = '[0-9a-z-.]+'

    # six (1.11.0)                       - Python 2 and 3 compatibility utilities
    rx_starting_line = re.compile(
        '^'
        '(?P<name>' + pattern_name + ')'
        '\s*'
        '[(](?P<version>' + pattern_version + ')[)]'
        '\s+'
        '[-]'
        '\s*'
        '(?P<desc>.*)'
        '$'
    )

    #                   cameras as Python objects.
    rx_continuation_line = re.compile(
        '^'
        '[ ]+'
        '(?P<desc>.*)'
        '$'
    )

    #  INSTALLED: 1.10.0
    #  LATEST:    1.11.0
    rx_version_line = re.compile(
        '^'
        '[ ]{2}'
        '(?P<keyword>INSTALLED|LATEST)'
        '[:]'
        '\s*'
        '(?P<version>' + pattern_version + ')'
        '\s*'
        '$'
    )

    def __init__(self, pip_path):
        self.pip_path = pip_path

    def invoke_search(self, package_name):
        args = [
            self.pip_path,
            'search',
            package_name,
        ]

        output_bytes = subprocess.check_output(args)
        output = output_bytes.decode('utf-8')
        return output

    def parse_search_output(self, package_name, output):
        versions = []

        for line in output.splitlines():
            # the line is all whitespace, skip it
            if not line.strip():
                continue

            match_starting = self.rx_starting_line.match(line)
            match_continuation = self.rx_continuation_line.match(line)
            match_version = self.rx_version_line.match(line)

            # we don't recognize this line
            if not any((match_starting, match_continuation, match_version)):
                _logger.warn('Unable to parse pip search line: %s', line)
                continue

            cur_pkgname = match_starting and match_starting.groupdict()['name']

            # we've entered a new package block
            if cur_pkgname and not cur_pkgname == package_name:
                continue

            if match_starting:
                version = match_starting.groupdict()['version']
                versions = [version]

            if match_version:
                keyword = match_version.groupdict()['keyword']
                version = match_version.groupdict()['version']
                versions.append(version)

        pkg_rels = PackageReleases(
            name=package_name,
            versions=versions,
        )
        return pkg_rels

    def search_for_releases(self, package_name):
        output = self.invoke_search(package_name)
        pkg_rels = self.parse_search_output(package_name, output)
        return pkg_rels


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig()
    pip = Pip('pip')
    rels = pip.search_for_releases('six')
    print rels
