from reqlint.analyzers.can_be_upgraded import CanBeUpgradedAnalyzer
from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList
from reqlint.model.available_packages import AvailablePackages
from reqlint.model.package_releases import PackageReleases
from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt


def test_can_be_upgraded_analyzer():
    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='==', version='0.5'),
            PackageRequirement(name='six', operator='==', version='0.9'),
        ],
    )

    pkgs_available = AvailablePackages(
        packages=[
            PackageReleases(name='coverage', versions=('3.5', '3.6', '3.7', '3.8')),
            PackageReleases(name='parsimonious', versions=('0.5', '0.5.1')),
            PackageReleases(name='six', versions=('0.8', '0.9')),
        ],
    )

    analyzer = CanBeUpgradedAnalyzer(
        requirements_txt=pkgs_reqs,
        available_packages=pkgs_available,
    )
    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'coverage<3.6' "
                    "can be upgraded to 'coverage-3.8'"
                ),
            ),
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'parsimonious==0.5' "
                    "can be upgraded to 'parsimonious-0.5.1'"
                ),
            ),
        ],
    )

    assert expected_advice_list == advice_list
