from deplint.analyzers.can_be_upgraded import CanBeUpgradedAnalyzer
from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList
from deplint.model.available_packages import AvailablePackages
from deplint.model.installed_packages import InstalledPackages
from deplint.model.package_installed import InstalledPackage
from deplint.model.package_releases import PackageReleases
from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt


def test_can_be_upgraded_analyzer():
    pkgs_available = AvailablePackages(
        packages=[
            PackageReleases(name='abc', versions=('8.5', '8.6')),
            PackageReleases(name='click', versions=('1.8', '1.9')),
            PackageReleases(name='coverage', versions=('3.5', '3.6', '4.0', '4.1')),
            PackageReleases(name='ply', versions=('0.5', '0.5.1')),
            PackageReleases(name='six', versions=('0.8', '0.9')),
        ],
    )

    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='abc', operator='<=', version='9.0'),
            PackageRequirement(name='click', operator=None, version=None),
            PackageRequirement(name='coverage', operator='<', version='4.0'),  # -> 4.1
            PackageRequirement(name='ply', operator='==', version='0.5'),  # -> 0.5.1
            PackageRequirement(name='six', operator='==', version='0.9'),
        ],
    )

    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='abc', version='8.5'),  # -> 8.6
            InstalledPackage(name='click', version='1.8'),  # -> 1.9
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
                    "Installed dependency 'abc-8.5' "
                    "can be updated to 'abc-8.6'"
                ),
            ),
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Installed dependency 'click-1.8' "
                    "can be updated to 'click-1.9'"
                ),
            ),
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
                    "can be updated to 'coverage-3.6'"
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
