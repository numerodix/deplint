import logging
import subprocess

from reqlint.parsers.pip_freeze import PipFreezeParser
from reqlint.parsers.pip_search import PipSearchParser

_logger = logging.getLogger(__name__)


class Pip(object):
    def __init__(self, pip_path):
        self.pip_path = pip_path

    # Low level interface

    def invoke_freeze(self):
        args = [
            self.pip_path,
            'freeze',
        ]

        output_bytes = subprocess.check_output(args)
        output = output_bytes.decode('utf-8')
        return output

    def invoke_search(self, package_name):
        args = [
            self.pip_path,
            'search',
            package_name,
        ]

        output_bytes = subprocess.check_output(args)
        output = output_bytes.decode('utf-8')
        return output

    def parse_freeze_output(self, output):
        parser = PipFreezeParser(content=output)
        pkgs_installed = parser.parse()
        return pkgs_installed

    def parse_search_output(self, package_name, output):
        parser = PipSearchParser(content=output)
        pkg_rels = parser.parse(package_name=package_name)
        return pkg_rels

    # High level interface

    def list_installed_packages(self):
        output = self.invoke_freeze()
        pkgs_installed = self.parse_freeze_output(output)
        return pkgs_installed

    def search_for_releases(self, package_name):
        output = self.invoke_search(package_name)
        pkg_rels = self.parse_search_output(package_name, output)
        return pkg_rels


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    pip = Pip('pip')
    pkgs = pip.list_installed_packages()
    print pkgs
    rels = pip.search_for_releases('six')
    print rels
