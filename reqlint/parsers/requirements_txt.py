import logging
import re

from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt

_logger = logging.getLogger(__name__)


class RequirementsTxtParser(object):
    '''
    Parser for the requirements.txt file format.
    '''

    # comment at the beginning of line after whitespace
    rx_comment = re.compile('(?:^|\s+)#.*$')

    # shorter operators last to prevent greedy matching from incorrect parsing
    version_operators = PackageRequirement.VALID_OPERATORS
    version_operators_joined = '|'.join((re.escape(op) for op in version_operators))
    rx_name_op_version = re.compile(
        '^(?P<name>.*?)(?P<operator>' + version_operators_joined + ')(?P<version>.*)$'
    )

    def __init__(self, fileobj):
        # XXX validate fileobj type

        self.fileobj = fileobj

    def strip_comment(self, line):
        return self.rx_comment.sub('', line)

    def parse(self):
        pkgs = []

        for line in self.fileobj:
            line = self.strip_comment(line)
            line = line.strip()

            # If the line was all comment or whitespace then skip it
            if not line:
                continue

            match = self.rx_name_op_version.match(line)

            # Was unable to parse the line
            if not match or not len(match.groups()) == 3:
                _logger.warn('Unable to parse requirements line: %s', line)
                continue

            pkg = PackageRequirement(
                name=match.groupdict()['name'],
                operator=match.groupdict()['operator'],
                version=match.groupdict()['version'],
            )
            pkgs.append(pkg)

        reqs = RequirementsTxt(packages=pkgs)
        return reqs


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig()
    p = RequirementsTxtParser(open(sys.argv[1]))
    reqs = p.parse()
    for r in reqs.packages:
        print(r)
