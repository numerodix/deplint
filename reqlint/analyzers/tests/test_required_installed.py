from reqlint.analyzers.required_installed import RequiredInstalledAnalyzer
from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList
from reqlint.model.installed_packages import InstalledPackages
from reqlint.model.package_installed import InstalledPackage
from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt


def test_required_installed_analyzer():
    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='<=', version='0.5'),
        ],
    )

    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='coverage', version='3.5'),  # ok
            InstalledPackage(name='parsimonious', version='0.5'),  # ok
        ],
    )

    analyzer = RequiredInstalledAnalyzer(
        requirements_txt=pkgs_reqs,
        installed_packages=pkgs_installed,
    )
    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='debug',
                message="Dependency 'coverage<3.6' is satisfied by 'coverage-3.5'",
            ),
            Advice(
                analyzer=analyzer,
                severity='debug',
                message="Dependency 'parsimonious<=0.5' is satisfied by 'parsimonious-0.5'",
            ),
        ],
    )

    assert expected_advice_list == advice_list
