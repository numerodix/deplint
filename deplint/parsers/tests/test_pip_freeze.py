from deplint.model.installed_packages import InstalledPackages
from deplint.model.package_installed import InstalledPackage
from deplint.parsers.pip_freeze import PipFreezeParser


PIP_FREEZE_EXAMPLE = '''
coverage==3.6
ipdb==0.8
ipython==1.1.0
'''


def test_pip_freeze_parser():
    pkgs_expected = InstalledPackages(
        packages=[
            InstalledPackage(name='coverage', version='3.6'),
            InstalledPackage(name='ipdb', version='0.8'),
            InstalledPackage(name='ipython', version='1.1.0'),
        ],
    )

    parser = PipFreezeParser(content=PIP_FREEZE_EXAMPLE)
    pkgs_installed = parser.parse()

    assert pkgs_expected == pkgs_installed
