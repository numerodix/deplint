from safety import safety

from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList


class DistributionStub(object):
    '''
    A stub class for pkg_resources.DistInfoDistribution expected by the safety
    tool.
    '''

    def __init__(self, pkg):
        self.key = pkg.name
        self.version = pkg.version


class IsVulnerableAnalyzer(object):
    '''
    Reports packages that are vulnerable to known security exploits.

    This analyzer is a bit fragile, because it relies on the 'safety' tool
    which is written as a tool, not a library, and we need to depend on an
    unofficial API that could change.
    '''

    def __init__(self, installed_packages, check_func=None):
        self.installed_packages = installed_packages
        self.check_func = check_func or safety.check

    def analyze(self):
        advice_list = []

        pkgs = [DistributionStub(pkg) for pkg in self.installed_packages.packages]
        vulns = self.check_func(
            packages=pkgs,
            key=None,
            db_mirror=None,
            cached=None,
            ignore_ids=[],
        )

        for vuln in vulns:
            message = (
                "Installed dependency '%s' has a known vulnerability in '%s'\n    %s"
            ) % (
                '%s-%s' % (vuln.name, vuln.version),
                '%s%s' % (vuln.name, vuln.spec),
                vuln.advisory,
            )

            advice = Advice(
                analyzer=self,
                severity='warn',
                message=message,
            )
            advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
