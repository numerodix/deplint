from reqlint.analyzers.can_be_upgraded import CanBeUpgradedAnalyzer
from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList
from reqlint.model.available_packages import AvailablePackages
from reqlint.model.installed_packages import InstalledPackages
from reqlint.model.package_installed import InstalledPackage
from reqlint.model.package_releases import PackageReleases
from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt


def test_can_be_upgraded_analyzer():
    pkgs_available = AvailablePackages(
        packages=[
            PackageReleases(name='coverage', versions=('3.5', '3.6', '4.0', '4.1')),
            PackageReleases(name='ply', versions=('0.5', '0.5.1')),
            PackageReleases(name='six', versions=('0.8', '0.9')),
        ],
    )

    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='4.0'),  # -> 4.1
            PackageRequirement(name='ply', operator='==', version='0.5'),  # -> 0.5.1
            PackageRequirement(name='six', operator='==', version='0.9'),
        ],
    )

    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='coverage', version='3.5'),  # -> 3.6
        ],
    )

    analyzer = CanBeUpgradedAnalyzer(
        requirements_txt=pkgs_reqs,
        installed_packages=pkgs_installed,
        available_packages=pkgs_available,
    )
    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'coverage<4.0' "
                    "can be upgraded to 'coverage-4.1'"
                ),
            ),
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Installed dependency 'coverage-3.5' "
                    "can be upgraded to 'coverage-3.6'"
                ),
            ),
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'ply==0.5' "
                    "can be upgraded to 'ply-0.5.1'"
                ),
            ),
        ],
    )

    assert expected_advice_list == advice_list
