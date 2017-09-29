import logging

from six import StringIO

from deplint.model.installed_packages import InstalledPackages
from deplint.model.package_installed import InstalledPackage
from deplint.parsers.requirements_txt import RequirementsTxtParser

_logger = logging.getLogger(__name__)


class PipFreezeParser(object):
    '''
    Parser for the `pip freeze` output format.
    '''

    def __init__(self, content):
        self.content = content

    def parse(self):
        # Re-use the RequirementsTxtParser because the data format is
        # compatible
        parser = RequirementsTxtParser(fileobj=StringIO(self.content))
        pkg_reqs = parser.parse()

        # Return 'installed' rather than 'required' domain objects
        pkgs = []
        for pkg_req in pkg_reqs.packages:
            pkg = InstalledPackage(
                name=pkg_req.name,
                version=pkg_req.version,
            )
            pkgs.append(pkg)

        pkgs_installed = InstalledPackages(
            packages=pkgs,
        )
        return pkgs_installed
