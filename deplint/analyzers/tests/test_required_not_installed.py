from deplint.analyzers.required_not_installed import \
    RequiredNotInstalledAnalyzer
from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList
from deplint.model.installed_packages import InstalledPackages
from deplint.model.package_installed import InstalledPackage
from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt


def test_required_not_installed_analyzer():
    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='<=', version='0.5'),
            PackageRequirement(name='six', operator='>=', version='0.5'),
        ],
    )

    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='coverage', version='3.5'),  # ok
            # parsimonious missing
            InstalledPackage(name='six', version='0.4.9'),  # version too low
        ],
    )

    analyzer = RequiredNotInstalledAnalyzer(
        requirements_txt=pkgs_reqs,
        installed_packages=pkgs_installed,
    )
    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='error',
                message=(
                    "Required dependency 'parsimonious<=0.5' is not installed"
                ),
            ),
            Advice(
                analyzer=analyzer,
                severity='error',
                message=(
                    "Required dependency 'six>=0.5' "
                    "is not satisfied by installed 'six-0.4.9'"
                ),
            ),
        ],
    )

    assert expected_advice_list == advice_list
