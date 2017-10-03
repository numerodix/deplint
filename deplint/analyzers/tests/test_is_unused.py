from deplint.analyzers.is_unused import IsUnusedAnalyzer
from deplint.data_sources.site_packages.site_packages import SitePackages
from deplint.data_sources.source_code.git_grep import GitGrep
from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList
from deplint.model.installed_packages import InstalledPackages
from deplint.model.package_installed import InstalledPackage
from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt


def test_is_unused_analyzer():
    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='click', operator='==', version='1.8'),
            PackageRequirement(name='six', operator='==', version='3.5'),
        ],
    )

    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='click', version='1.8'),
            InstalledPackage(name='six', version='3.5'),
        ],
    )

    # mock: the top level of the package is the name of the package
    site_packages = SitePackages(
        python_path=None,
        installed_package_names=[],
    )
    site_packages.get_package_top_levels = lambda pkg_name: [pkg_name]

    # mock: grep says six is used, nothing else is
    git_grep = GitGrep(basedir=None)
    git_grep.package_is_imported = lambda pkg_name: (True if pkg_name == 'six' else False)

    analyzer = IsUnusedAnalyzer(
        requirements_txt=pkgs_reqs,
        installed_packages=pkgs_installed,
        site_packages=site_packages,
        grep=git_grep,
    )
    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'click==1.8' "
                    "is never imported (click)"
                ),
            ),
        ],
    )

    assert expected_advice_list == advice_list
