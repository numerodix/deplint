import logging
import re

from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt

_logger = logging.getLogger(__name__)


class RequirementsTxtParser(object):
    '''
    Parser for the requirements.txt file format.
    '''

    # comment at the beginning of line after whitespace
    rx_comment = re.compile('(?:^|\s+)#.*$')

    # cmd line flag to pip
    rx_flag = re.compile('^[-].*$')

    # https://www.python.org/dev/peps/pep-0508/
    pattern_name = '[A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9]'

    # shorter operators last to prevent greedy matching from incorrect parsing
    version_operators = PackageRequirement.VALID_OPERATORS
    version_operators_joined = '|'.join((re.escape(op) for op in version_operators))

    rx_name = re.compile(
        '^'
        '(?P<name>' + pattern_name + ')'
        '$'
    )

    rx_name_op_version = re.compile(
        '^'
        '(?P<name>' + pattern_name + ')'
        '(?P<operator>' + version_operators_joined + ')'
        '(?P<version>.*)'
        '$'
    )

    def __init__(self, fileobj):
        # XXX validate fileobj type

        self.fileobj = fileobj

    def strip_comment(self, line):
        return self.rx_comment.sub('', line)

    def strip_flag(self, line):
        return self.rx_flag.sub('', line)

    def parse(self):
        pkgs = []

        for line in self.fileobj:
            line = self.strip_comment(line)
            line = self.strip_flag(line)
            line = line.strip()

            # If the line was all comment or whitespace then skip it
            if not line:
                continue

            match = self.rx_name_op_version.match(line)
            if not match:
                match = self.rx_name.match(line)

            # Was unable to parse the line
            if not match or not len(match.groups()) in [1, 3]:
                _logger.warn('Unable to parse requirements line: %s', line)
                continue

            pkg = PackageRequirement(
                name=match.groupdict()['name'],
                operator=match.groupdict().get('operator'),
                version=match.groupdict().get('version'),
            )
            pkgs.append(pkg)

        reqs = RequirementsTxt(packages=pkgs)
        return reqs
