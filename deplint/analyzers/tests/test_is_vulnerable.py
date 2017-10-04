from safety.safety import Vulnerability

from deplint.analyzers.is_vulnerable import IsVulnerableAnalyzer
from deplint.data_sources.site_packages.site_packages import SitePackages
from deplint.data_sources.source_code.git_grep import GitGrep
from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList
from deplint.model.installed_packages import InstalledPackages
from deplint.model.package_installed import InstalledPackage
from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt


ADVISORY_EXAMPLE_TORNADO = (
    'CRLF injection vulnerability in the '
    'tornado.web.RequestHandler.set_header '
    'function in Tornado before 2.2.1 allows '
    'remote attackers to inject arbitrary HTTP '
    'headers and conduct HTTP response splitting '
    'attacks via crafted input.'
)


def mocked_check_func(packages, key, db_mirror, cached, ignore_ids):
    vulns = []

    for pkg in packages:
        if pkg.key == 'tornado' and pkg.version == '2.2.0':
            vulns.append(
                Vulnerability(
                    name=pkg.key,
                    spec='<2.2.1',
                    version=pkg.version,
                    advisory=ADVISORY_EXAMPLE_TORNADO.strip(),
                    vuln_id='26161',
                )
            )

    return vulns


def test_is_vulnerable_analyzer():
    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='click', version='1.8'),
            InstalledPackage(name='tornado', version='2.2.0'),
        ],
    )

    analyzer = IsVulnerableAnalyzer(
        installed_packages=pkgs_installed,
    )

    # mock checker
    analyzer.check_func = mocked_check_func

    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='warn',
                message=(
                    "Installed dependency 'tornado-2.2.0' "
                    "has a known vulnerability in 'tornado<2.2.1'\n"
                    "    CRLF injection vulnerability in the "
                    "tornado.web.RequestHandler.set_header function "
                    "in Tornado before 2.2.1 allows remote attackers "
                    "to inject arbitrary HTTP headers and conduct HTTP "
                    "response splitting attacks via crafted input."
                ),
            ),
        ],
    )

    assert expected_advice_list == advice_list
